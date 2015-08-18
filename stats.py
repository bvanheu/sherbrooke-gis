#!/usr/bin/env python

import operator
import json
from os import listdir
from os.path import isfile, join

# You need to first run the `extract_objects.py` script. This will create around
# 70 000 files into the `output` directory.

data = {}
stats = {}
stats_value = {}

if __name__ == "__main__":
    onlyfiles = [ f for f in listdir('./output/') if isfile(join('./output/',f)) ]

    for f in onlyfiles:
        with open('./output/' + f, 'r') as fi:
            try:
                j = json.loads(fi.read())
                if j['NUMERO_DE_LOT'] not in stats:
                    data[j['NUMERO_DE_LOT']] = {'proprietaire' : '', 'valeur_propriete': 0}
                data[j['NUMERO_DE_LOT']]['proprietaire'] = j['PROPRIETAIRE']
                if j['VALEUR_PROPRIETE'] is not None:
                    data[j['NUMERO_DE_LOT']]['valeur_propriete'] = int(j['VALEUR_PROPRIETE'])
            except:
                print("unable to json parse: " + f)

    for lot in data:
        if data[lot]['proprietaire'] not in stats:
            stats[data[lot]['proprietaire']] = 0
            stats_value[data[lot]['proprietaire']] = 0

        stats[data[lot]['proprietaire']] += 1
        stats_value[data[lot]['proprietaire']] += data[lot]['valeur_propriete']

    print("Sorting...")
    stats_sorted = sorted(stats_value.items(), key=operator.itemgetter(1))
    stats_sorted.reverse()
    print("ok")

    #print(stats_sorted)

    # Print top 25 building owner
    for i in range(100):
        print("{: >40} {: >20} {: >20}$".format(stats_sorted[i][0], stats[stats_sorted[i][0]], format(stats_sorted[i][1], ',').replace(',', ' ').replace('.', ',')))
