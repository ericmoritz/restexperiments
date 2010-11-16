import sys
import json
from collections import defaultdict
import re

type_pat = re.compile("n(\d+)c(\d+)")

data = defaultdict(dict)
levels = {}
     
for line in sys.stdin:
    result = json.loads(line)
    for case, val in result['cases'].items():
        data[case][result['type']] = val
        levels[result['type']] = 1

# pull out the concurrency level out of the test type
levels = sorted(levels.keys())

concurrency = (m.group(2) for m in map(type_pat.match, levels))
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
    for level in levels:
        result = values.get(level, {})
        row.append(result.get(result_type, "0"))

    print ",".join(row)
