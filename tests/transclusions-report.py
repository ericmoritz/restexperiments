# -*- coding: utf-8 -*-
import sys
import os
from restexperiments.core.report import collect, tocsv
from collections import defaultdict
from glob import glob
from decimal import Decimal
import re
import json
import csv

root = os.path.abspath("./data/trans/phase1")
data = collect(os.path.join(root))

newdata = defaultdict(dict)
for level, value in data.items():
    newdata[level]['direct'] = value['direct-family']

    tpr = value['template']['tpr'] + value['spouse']['tpr'] + value['children']['tpr']
    rps = 1 / tpr * 1000

    newdata[level]['xSI'] = {
        'tpr': tpr,
        'rps': rps
        }

for datapoint in "rps", "tpr":
    # Create a table out of the data
    table = tocsv(newdata, datapoint,  ["xSI", "direct"])
    # rotate table
    table = map(list, map(None, *table))

    # set the col1 label from level to case
    table[0][0] = "Case"

    out_root = os.path.abspath("./docs/source/_static/data/trans/")
    with open(os.path.join(out_root, "phase1_%s.csv" % (datapoint)), "w") as fh:
        writer = csv.writer(fh)
        writer.writerows(table)
