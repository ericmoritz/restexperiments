import sys
import json
from collections import defaultdict
import re

type_pat = re.compile("n(\d+)c(\d+)")

data = defaultdict(dict)
levels = set()
     
for line in sys.stdin:
    result = json.loads(line)
    for case, val in result['cases'].items():
        data[case][result['type']] = val
        type_key = result['type']
        m = type_pat.match(type_key)
        concurrency = m.group(2)
        levels.add((type_key, int(concurrency)))

# pull out the concurrency level out of the test type
levels = sorted(levels, key=lambda x: x[1])
concurrency = (unicode(l[1]) for l in levels)
print "Case, " + ",".join(concurrency)

if len(sys.argv) == 1:
    print "First argv is the key to use for the CSV file"
    print "Reference:"
    print data
    sys.exit(1)
else:
    result_type = sys.argv[1]

for case, values in data.items():
    row = [case]
    for key, concurrency in levels:
        result = values.get(key, {})
        row.append(result.get(result_type, "0"))

    print ",".join(row)
