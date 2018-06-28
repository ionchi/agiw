#!/usr/bin/env python3
import aiohttp
import asyncio
import async_timeout
import os
import subprocess
from bs4 import BeautifulSoup
import json
import datetime
from collections import OrderedDict
import sys


async def download_coroutine(session, url, folder,folder2, resultfile, progressive):
    with async_timeout.timeout(3000):
        async with session.get(url) as response:
            time = datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M:%S.%f")[:-3]
            filename = os.path.basename(str(progressive) + ".html")
            output = os.path.join(folder, filename)
            bashCommand = "python2.7 -m src.model.specificationextractor %s %s" % (str(url),folder2+"/"+str(progressive))
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if str(response.status)[0] == "2":
                with open(output, 'wb') as f_handle:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f_handle.write(chunk)
                with open(resultfile, "a") as resultfile:
                    resultfile.write(url + " \t " + output + "\n")
                print(url + " \t " + output + " [ " + time + " ]")
            else:
                with open(resultfile, "a") as resultfile:
                    resultfile.write(url + " \t" + str(response.status) + "\n")
                print(url + " \t" + str(response.status) + " [ " + time + " ]")
            return await response.release()


async def main(loop):
    data = json.load(open(sys.argv[1]), object_pairs_hook=OrderedDict)
    folderpath = "./" + sys.argv[2]
    folderpath2="./toilette_extr"

    for key, value in data.items():
        sitepath = os.path.join(folderpath, key)
        sitepath2 = os.path.join(folderpath2, key)
        resultfile = os.path.join(sitepath, "index.txt")
        if not os.path.exists(sitepath):
            os.makedirs(sitepath)
        if not os.path.exists(sitepath2):
            os.makedirs(sitepath2)
        async with aiohttp.ClientSession(loop=loop) as session:
            progressive = 1
            tasks = []
            for url in value:
                tasks.append(download_coroutine(session, url, sitepath,sitepath2 ,resultfile, progressive))
                progressive = progressive+1
            try:
                await asyncio.gather(*tasks)
            except:
                print("Eccezione di connessione")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
