import re
from collections import defaultdict


def traverse(d, curr):
    return sum([cc + cc * traverse(d, bag) for cc, bag in d[curr]])


with open('7.in') as f:
    contains = defaultdict(list)
    for rule in [x.strip() for x in f.readlines()]:
        carrying = re.match(r'^([\w]+ [\w]+)', rule).groups()[0]
        for m in re.finditer(r'([\d]+) ([\w]+ [\w]+)', rule):
            contains[carrying].append((int(m.groups()[0]), m.groups()[1]))

    print(traverse(contains, 'shiny gold'))
