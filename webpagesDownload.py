#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import requests
import json
from collections import OrderedDict


def main():
    # variabile per scandire i file scaricati
    i = 1
    # apre il file passato come parametro allo script
    with open(sys.argv[1], 'r') as in_file:
        # orderDict per preservare l'ordine del json
        data = json.load(in_file, object_pairs_hook=OrderedDict)

        # itera le chiavi del json
        for key, value in data.items():
            # itera i valori (in questo caso url)
            for url in value:
                # nome file output
                output = "file_" + str(i) + ".html"
                # rende gli url nel giusto formato
                url = url.rstrip()
                try:
                    response = requests.get(url)
                    # funzione per sollevare un'eccezione http
                    response.raise_for_status()
                    # scaricare solo i siti con codice 200
                    if response.status_code == 200:
                        with open("results.txt", "a") as resultfile:
                            resultfile.write(url + " -> " + output + "\n")
                        # Download contenuto risposta http
                        soup = BeautifulSoup(response.content, "lxml")
                        # salvataggio file html (opzionale: prettify)
                        with open(output, 'a') as fp:
                            fp.write(soup.prettify())
                except requests.exceptions.HTTPError:
                    with open("results.txt", "a") as resultfile:
                        resultfile.write(url + " -> " + str(response.status_code)+"\n")
                    pass
                except requests.exceptions.RequestException as e:
                    data = str(e)
                    # eccezione diversa dai codici http
                    # accorciata a 25 caratteri sul file di output
                    info = data[:25] + (data[25:] and '..')
                    with open("results.txt", "a") as resultfile:
                        resultfile.write(url + " -> other error: " + info+"\n")
                    pass
                i = i + 1


main()

