import sys
from collections import defaultdict
from glob import glob
data = defaultdict(dict)

for filename in glob("results/*.ab.txt"):
    case = filename[len("results/"):len(".ab.txt")*-1]

    with open(filename) as fh:
        for line in fh:
            if "Requests per second:" in line:
                key, value = line.split(":")
                data[case]["rps"] = value.strip().split(" ")[0]

def print_table(key_label, value_label, items):
    lcol = len(key_label) + 10
    rcol = len(value_label) + 10
    
    print "%s %s" % ("=" * lcol,
                     "=" * rcol)
    print "%s  %s" % (key_label.ljust(lcol),
                     value_label.ljust(rcol))
    print "%s %s" % ("=" * lcol,
                     "=" * rcol)
    for key, value in items:
        print "%s %s" % (key.ljust(lcol),
                         value.rjust(rcol))
    print "%s %s" % ("=" * lcol,
                     "=" * rcol)

rps_result = [(case, d["rps"]) for case, d in data.items()]
rps_result.sort(key=lambda item: float(item[1]), reverse=True)

print_table("Case", "Requests per second", rps_result)
