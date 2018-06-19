#!/usr/bin/env python3
import aiohttp
import asyncio
import async_timeout
import os
import json
import datetime
from collections import OrderedDict
import sys

'''
Uso: ./webpagesValidator.py data_file.json nome_output_json [senza .json]
'''

async def download_coroutine(session, url, key, dict):
    with async_timeout.timeout(30):
        async with session.get(url) as response:
            time = datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M:%S.%f")[:-3]
            if str(response.status)[0] == "2":
                dict[key].append(url)
                print(url + "[ " + time + " ]")
            else:
                print(url + " \t" + str(response.status) + " [ " + time + " ]")
            return await response.release()


async def main(loop):
    data = json.load(open(sys.argv[1]), object_pairs_hook=OrderedDict)
    folderpath = "./valid_urls/"
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    resultfile = os.path.join(folderpath, sys.argv[2] + ".json")
    dict = {}
    for key, value in data.items():
        dict[key] = []
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = []
            for url in value:
                tasks.append(download_coroutine(session, url, key, dict))
            try:
                await asyncio.gather(*tasks)
            except Exception as e:
                time = datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M:%S.%f")[:-3]
                data = str(e)
                info = data[:25] + (data[25:] and '..')
                print("other error: " + info + " [ " + time + " ]")
                pass
    with open(resultfile, "a") as resultfile:
        json.dump(dict, resultfile, sort_keys=True, indent=2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
