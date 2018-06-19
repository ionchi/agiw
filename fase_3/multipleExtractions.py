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
    for key, value in data.items():
        sitepath = os.path.join(folderpath, key)
        if not os.path.exists(sitepath):
            os.makedirs(sitepath)
        progressive = 1
        second_progressive = 1
        for url in value:
            if os.path.isfile("./" + sys.argv[2] + "/" + key + ".json"):
                filename = os.path.basename(str(progressive) + ".json")
                output = os.path.join(sitepath, filename)
                try:
                    s = Scraper().fromfile(open("./" + sys.argv[2] + "/" + key + ".json"))
                    result = s.scrape(url)
                    print(result[:10] + (result[10:] and '..'))
                    with open(output, 'w') as f_handle:
                        json.dump(result, f_handle, sort_keys=True, indent=4)
                    progressive = progressive + 1
                except Exception as e:
                    data = str(e)
                    print("other error: " + data)
                    pass
            else:
                for file in listfile:
                    filename = os.path.basename(str(progressive)+"_"+str(second_progressive)+".json")
                    output = os.path.join(sitepath, filename)
                    try:
                        s = Scraper().fromfile(open(sys.argv[2] + "/" + file))
                        result = s.scrape(url)

                        temp = str(result)
                        if 10 < len(temp) < 3000:
                            data = json.loads(temp.replace("'", '"'))

                            print(result[:10] + (result[10:] and '..'))
                            with open(output, 'w') as f_handle:
                                json.dump(data, f_handle, sort_keys=True, indent=4)
                            second_progressive = second_progressive + 1
                    except Exception as e:
                        data = str(e)
                        print("other error: " + data)
                        pass
                progressive = progressive + 1


main()
