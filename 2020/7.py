import re
from collections import defaultdict

with open('7.in') as f:
    carried_in = defaultdict(list)
    for rule in [x.strip() for x in f.readlines()]:
        carried = re.match(r'^([\w]+ [\w]+)', rule).groups()[0]
        for m in re.finditer(r'[\d]+ ([\w]+ [\w]+)', rule):
            carried_in[m.groups()[0]].append(carried)

    s = carried_in['shiny gold']
    c = set()
    while len(s) > 0:
        curr = s.pop()
        c.add(curr)
        s.extend(carried_in[curr])

    print(len(c))
