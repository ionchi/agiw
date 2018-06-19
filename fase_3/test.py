#!/usr/bin/env python3
import sys
import json
import os
from collections import OrderedDict
from scrapely import Scraper

'''
Uso: ./test.py data_file.json train_folder output_folder
'''


def main():
    s = Scraper()
    data = json.load(open(sys.argv[1]), object_pairs_hook=OrderedDict)
    folderpath = "./" + sys.argv[3]
    iterator = 1
    for key, value in data.items():
        if(iterator<10):
            try:
                train_data = json.load(open(sys.argv[2] + "/" + key + ".json"), object_pairs_hook=OrderedDict)
                train_url = value[0]
                s.train(train_url, train_data)
                iterator = iterator + 1
            except Exception as e:
                data = str(e)
                print("other error: " + data + "domain: " + key)
                pass
        else:
            pass

    data = json.load(open(sys.argv[1]), object_pairs_hook=OrderedDict)
    for key, value in data.items():
        sitepath = os.path.join(folderpath, key)
        if not os.path.exists(sitepath):
            os.makedirs(sitepath)
        progressive = 1
        for url in value:
            filename = os.path.basename(str(progressive) + ".json")
            output = os.path.join(sitepath, filename)
            try:
                result = s.scrape(url)
                print(result[:10] + (result[10:] and '..'))
                with open(output, 'w') as f_handle:
                    json.dump(result, f_handle, sort_keys=True, indent=4)
                progressive = progressive + 1
            except Exception as e:
                data = str(e)
                print("other error: " + data)
                pass


main()
