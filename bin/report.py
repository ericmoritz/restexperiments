# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from glob import glob
from decimal import Decimal
import os
import json


data = defaultdict(dict)

root = sys.argv[1]

for filename in glob(root+"*.ab.txt"):
    case = filename[len(root):len(".ab.txt")*-1]

    with open(filename) as fh:
        for line in fh:
            if "Requests per second:" in line:
                key, value = line.split(":")
                data[case]["rps"] = value.strip().split(" ")[0]
            elif "Time per request:" in line and "(mean," in line:
                key, value = line.split(":")
                data[case]["tpr"] = value.strip().split(" ")[0]
                


def print_table(key_label, value_label, control, items):
    
    key_lengths = [len(key) for key,val in items]
    val_lengths = [len(val) for key,val in items]
    lcol = max([len(key_label)]+key_lengths) + 1
    rcol = max([len(value_label)]+ val_lengths) + 1
    
    print "%s %s %s" % ("=" * lcol,
                        "=" * rcol,
                        "=" * rcol)
    print "%s  %s %s" % (key_label.ljust(lcol),
                          value_label.ljust(rcol),
                        "± control".rjust(rcol))
    print "%s %s %s" % ("=" * lcol,
                        "=" * rcol,
                        "=" * rcol)
    for key, value in items:
        diff = Decimal(control) - Decimal(value)
        diff = unicode(diff)
        print "%s %s %s" % (key.ljust(lcol),
                            value.rjust(rcol),
                            diff.rjust(rcol))

    print "%s %s %s" % ("=" * lcol,
                        "=" * rcol,
                        "=" * rcol)    

control = data['control']

result = {
    'type': os.path.basename(os.path.dirname(root)),
    'cases': data
}

print json.dumps(result)
sys.exit()

rps_result = [(case, d["rps"]) for case, d in data.items()]
rps_result.sort(key=lambda item: float(item[1]), reverse=True)

print_table("Case", "Requests per second", control['rps'], rps_result)

print

tpr_result = [(case, d["tpr"]) for case, d in data.items()]
tpr_result.sort(key=lambda item: float(item[1]))

print_table("Case", "Time(ms) per request", control['tps'], tps_report)

