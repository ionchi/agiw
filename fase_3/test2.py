#!/usr/bin/env python3
import sys
import json
import os
from collections import OrderedDict
from scrapely import Scraper

'''
Uso: ./multipleExtractions.py data_file.json template_folder output_folder
'''


def main():
    data = json.load(open(sys.argv[1]), object_pairs_hook=OrderedDict)
    folderpath = "./" + sys.argv[3]
    listfile = os.listdir(sys.argv[2])  #lista di train template
    lista=[]
    for key, value in data.items():
        sitepath = os.path.join(folderpath, key)
        if not os.path.exists(sitepath):
            os.makedirs(sitepath)
        progressive = 1

        for url in value:
            if os.path.isfile("./" + sys.argv[2] + "/" + key + ".json"):
                filename = os.path.basename(str(progressive) + ".json")
                output = os.path.join(sitepath, filename)
            else:
                if key not  in lista:
                    lista.append(key)


    dafare=open("dafare.txt","a")
    for i in lista:
        print(i)
        dafare.writelines(i +"\n")
    print(len(lista))
main()
