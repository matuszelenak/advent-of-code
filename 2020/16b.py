import re
from collections import defaultdict

with open('16.in') as f:
    # Rules
    rules = {}
    while True:
        l = f.readline().strip()
        if not l:
            break

        key, fs, fe, ss, se = re.match(r'^([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)$', l).groups()
        rules[key] = [(int(fs), int(fe)), (int(ss), int(se))]

    # My ticket
    f.readline()
    my_ticket = f.readline()
    f.readline()

    # Other tickets
    f.readline()
    column_candidates = defaultdict(lambda: set(rules.keys()))
    for ticket in list(f.readlines()) + [my_ticket]:
        ticket_values = [int(x) for x in ticket.strip().split(',')]
        for col_id, value in enumerate(ticket_values):
            cell_candidates = {key for key, ((fs, fe), (ss, se)) in rules.items() if fs <= value <= fe or ss <= value <= se}
            if len(cell_candidates) == 0:
                break
            column_candidates[col_id] &= cell_candidates

    while True:
        single_candidates_ids = []
        single_candidates = set
        all_single = True
        for index, candidates in column_candidates.items():
            if len(candidates) == 1:
                single_candidates_ids.append(index)
                single_candidates = single_candidates.union(candidates)
            else:
                all_single = False

        if all_single:
            break

        for key in column_candidates.keys():
            if key in single_candidates_ids:
                continue
            column_candidates[key] -= single_candidates

    acc = 1
    my_ticket = [int(x) for x in my_ticket.strip().split(',')]
    for col_id, candidates in column_candidates.items():
        if next(iter(candidates))[:9] == 'departure':
            acc *= my_ticket[col_id]

    print(acc)
