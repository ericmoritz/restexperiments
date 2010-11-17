# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from glob import glob
from decimal import Decimal
import os
import json


data = defaultdict(dict)

root = sys.argv[1]

glob_str = os.path.join(root,"*.ab.txt")
for filename in glob(glob_str):
    dirname = os.path.dirname(filename) + "/"
    case = filename[len(dirname):len(".ab.txt")*-1]
    with open(filename) as fh:
        for line in fh:
            if "Requests per second:" in line:
                key, value = line.split(":")
                data[case]["rps"] = value.strip().split(" ")[0]
            elif "Time per request:" in line and "(mean," in line:
                key, value = line.split(":")
                data[case]["tpr"] = value.strip().split(" ")[0]
                

# Calculate the AJAX value
control_tpr = Decimal(data['control']['tpr'])
spouse_tpr = Decimal(data['spouse']['tpr'])
children_tpr = Decimal(data['children']['tpr'])

data['ajax'] = {}
data['ajax']['tpr'] = control_tpr + spouse_tpr + children_tpr
data['ajax']['rps'] = 1 / data['ajax']['tpr'] * 1000


result = {
    'type': os.path.basename(os.path.dirname(root)),
    'cases': data
}


print json.dumps(result, default=unicode)

