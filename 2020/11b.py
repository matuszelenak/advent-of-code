import itertools
import copy


with open('11.in') as f:
    grid = [[x for x in line.strip()] for line in f.readlines()]
    adj_deltas = set(itertools.product((-1, 0, 1), repeat=2)) - {(0, 0)}
    occupied = 0
    while True:
        new_grid = copy.deepcopy(grid)
        changed = False
        for ri, row in enumerate(grid):
            for si, seat in enumerate(row):
                if seat == '.':
                    continue

                adj_occupied = 0
                for dx, dy in adj_deltas:
                    y, x = ri, si
                    while True:
                        y, x = y + dy, x + dx
                        if y < 0 or x < 0:
                            break
                        try:
                            if grid[y][x] == 'L':
                                break
                            if grid[y][x] == '#':
                                adj_occupied += 1
                                break
                        except IndexError:
                            break

                if seat == '#':
                    if adj_occupied >= 5:
                        new_grid[ri][si] = 'L'
                        occupied -= 1
                        changed = True
                elif adj_occupied == 0:
                    new_grid[ri][si] = '#'
                    occupied += 1
                    changed = True

        if not changed:
            break
        grid = new_grid

    print(occupied)
