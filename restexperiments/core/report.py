# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from glob import glob
from decimal import Decimal
import os
import re


def collect(root):
    data = defaultdict(dict)
    
    for level in os.listdir(root):
        level_data = defaultdict(dict)

        glob_str = os.path.join(root, level, "*.ab.txt")

        for filename in glob(glob_str):
            dirname = os.path.dirname(filename) + "/"
            case = filename[len(dirname):len(".ab.txt")*-1]
            with open(filename) as fh:
                for line in fh:
                    if "Requests per second:" in line:
                        key, value = line.split(":")
                        level_data[case]["rps"] = Decimal(value.strip().split(" ")[0])
                    elif "Time per request:" in line and "(mean," in line:
                        key, value = line.split(":")
                        level_data[case]["tpr"] = Decimal(value.strip().split(" ")[0])
        data[level] = level_data

    return dict(data)


def tocsv(data, metric_key, case_keys):
    levelpat = re.compile("n\d+c(\d+)")
    header = [['level'] + case_keys]
    table = []
    for level, cases in data.items():
        mat = levelpat.match(level)
        level_int = int(mat.group(1))
        row = [level_int]

        for case in case_keys:
            row.append(cases[case][metric_key])

        table.append(row)
    # sort table by level
    table.sort(key=lambda r: r[0])
    
    return header + table
