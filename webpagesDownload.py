#!/usr/bin/env python3
import sys
import os
from bs4 import BeautifulSoup
import requests
import json
import datetime
from collections import OrderedDict


def main():
    folderpath = "./"+sys.argv[2]
    # apre il file passato come parametro allo script
    with open(sys.argv[1], 'r') as in_file:
        # orderDict per preservare l'ordine del json
        data = json.load(in_file, object_pairs_hook=OrderedDict)

        # itera le chiavi del json
        for key, value in data.items():
            # variabile per scandire i file scaricati
            i = 1
            sitepath = os.path.join(folderpath, key)
            if not os.path.exists(sitepath):
                os.makedirs(sitepath)
            # itera i valori (in questo caso url)
            for url in value:
                time = datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M:%S.%f")[:-3]
                # nome file output
                output = os.path.join(sitepath, str(i) + ".html")
                resultfilepath = os.path.join(sitepath, "index.txt")
                # rende gli url nel giusto formato
                url = url.rstrip()
                try:
                    response = requests.get(url)
                    # funzione per sollevare un'eccezione http
                    response.raise_for_status()
                    # scaricare solo i siti con codice 200
                    if response.status_code == 200:
                        with open(resultfilepath, "a") as resultfile:
                            resultfile.write(url + " \t " + output + "\n")
                        print(url + " \t " + output + " [ " + time + " ]")
                        # Download contenuto risposta http
                        soup = BeautifulSoup(response.content, "lxml")
                        # salvataggio file html (opzionale: prettify)
                        with open(output, 'a') as fp:
                            fp.write(soup.prettify())
                        i = i + 1
                except requests.exceptions.HTTPError:
                    with open(resultfilepath, "a") as resultfile:
                        resultfile.write(url + " \t" + str(response.status_code)+"\n")
                    print(url + " \t" + str(response.status_code) + " [ " + time + " ]")
                    pass
                except requests.exceptions.Timeout:
                    with open(resultfilepath, "a") as resultfile:
                        resultfile.write(url + " \t timeout\n")
                    print(url + " \t timeout\n" + " [ " + time + " ]")
                    pass
                except requests.exceptions.TooManyRedirects:
                    with open(resultfilepath, "a") as resultfile:
                        resultfile.write(url + " \t tooManyRedirects\n")
                    print(url + " \t tooManyRedirects\n" + " [ " + time + " ]")
                    pass
                except requests.exceptions.RequestException as e:
                    data = str(e)
                    # eccezione diversa dai codici http
                    # accorciata a 25 caratteri sul file di output
                    info = data[:25] + (data[25:] and '..')
                    with open(resultfilepath, "a") as resultfile:
                        resultfile.write(url + " \t other error: " + info+"\n")
                    print(url + " \t other error: " + info + " [ " + time + " ]")
                    pass


main()

