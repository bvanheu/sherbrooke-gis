#!/usr/bin/env python

import operator
import json
from os import listdir
from os.path import isfile, join

# You need to first run the `extract_objects.py` script. This will create around
# 70 000 files into the `output` directory.

stats = {}

if __name__ == "__main__":
    onlyfiles = [ f for f in listdir('./output/') if isfile(join('./output/',f)) ]

    for f in onlyfiles:
        with open('./output/' + f, 'r') as fi:
            try:
                j = json.loads(fi.read())
                if j['PROPRIETAIRE'] not in stats:
                    stats[j['PROPRIETAIRE']] = 0
                stats[j['PROPRIETAIRE']] += 1
            except:
                print("unable to json parse: " + f)

    stats_sorted = sorted(stats.items(), key=operator.itemgetter(1))
    stats_sorted.reverse()

    # Print top 25 building owner
    for i in range(25):
        print(stats_sorted[i])
