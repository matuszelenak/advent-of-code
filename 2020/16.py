import re

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
    f.readline()
    f.readline()

    # Other tickets
    f.readline()
    err = 0
    for ticket in f.readlines():
        ticket_values = [int(x) for x in ticket.strip().split(',')]
        for value in ticket_values:
            if not any((fs <= value <= fe or ss <= value <= se for (fs, fe), (ss, se) in rules.values())):
                err += value

    print(err)
