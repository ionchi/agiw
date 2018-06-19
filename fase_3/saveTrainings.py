#!/usr/bin/env python3
import sys
import json
import os
from collections import OrderedDict
from scrapely import Scraper

'''
Uso: ./saveTrainings.py data_file.json train_folder output_folder
'''


def main():
    data = json.load(open(sys.argv[1]), object_pairs_hook=OrderedDict)
    folderpath = "./" + sys.argv[3]
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    for key, value in data.items():
        filename = os.path.basename(key + ".json")
        output = os.path.join(folderpath, filename)
        s = Scraper()
        try:
            train_data = json.load(open("./" + sys.argv[2] + "/" + key + ".json"), object_pairs_hook=OrderedDict)
            train_url = value[0]
            s.train(train_url, train_data)
            s.tofile(open(output, 'w'))
        except Exception as e:
            data = str(e)
            print("other error: " + data + "on site:" + key)
            pass


main()
