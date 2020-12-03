with open('3a.in') as f:
    lines = [x.strip() for x in f.readlines()]
    m = 1
    for slope_y, slope_x in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        x_coord = 0
        y_coord = 0
        trees = 0
        while y_coord < len(lines):
            l = lines[y_coord]
            if l[x_coord % len(l)] == '#':
                trees += 1

            y_coord += slope_y
            x_coord += slope_x

        m *= trees

    print(m)
