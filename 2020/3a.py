with open('3a.in') as f:
    x_coord = 0
    trees = 0
    for line in [x.strip() for x in f.readlines()]:
        if line[x_coord % len(line)] == '#':
            trees += 1
        x_coord += 3

    print(trees)
