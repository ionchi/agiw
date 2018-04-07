#!/usr/bin/env python3
import aiohttp
import asyncio
import async_timeout
import os
from bs4 import BeautifulSoup
import json
import datetime
from collections import OrderedDict
import sys


async def download_coroutine(session, url, folder, resultfile, progressive):
    with async_timeout.timeout(30):
        async with session.get(url) as response:
            time = datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M:%S.%f")[:-3]
            filename = os.path.basename(str(progressive) + ".html")
            output = os.path.join(folder, filename)
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

    for key, value in data.items():
        sitepath = os.path.join(folderpath, key)
        resultfile = os.path.join(sitepath, "index.txt")
        if not os.path.exists(sitepath):
            os.makedirs(sitepath)
        async with aiohttp.ClientSession(loop=loop) as session:
            progressive = 1
            tasks = []
            for url in value:
                tasks.append(download_coroutine(session, url, sitepath, resultfile, progressive))
                progressive = progressive+1
            try:
                await asyncio.gather(*tasks)
            except:
                print("Eccezione di connessione")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))