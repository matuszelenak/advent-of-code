from collections import defaultdict
from itertools import product
from copy import deepcopy

space = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
neighbor_deltas = set(product((1, 0, -1), repeat=3)) - {(0, 0, 0)}

with open('17.in') as f:
    for y, row in enumerate(list(f.readlines())):
        for x, cell in enumerate(row):
            space[0][y][x] = 1 if cell == '#' else 0

for _ in range(6):
    coordinates = set()
    for z, plane in space.items():
        for y, row in plane.items():
            for x, cell in row.items():
                for dx, dy, dz in neighbor_deltas:
                    coordinates.add((x + dx, y + dy, z + dz))

    next_space = deepcopy(space)
    for x, y, z in coordinates:
        active_neighbors = 0
        for dx, dy, dz in neighbor_deltas:
            nx, ny, nz = x + dx, y + dy, z + dz
            active_neighbors += space[nz][ny][nx]
        if space[z][y][x] == 0 and active_neighbors == 3:
            next_space[z][y][x] = 1
        elif space[z][y][x] == 1 and active_neighbors not in (2, 3):
            next_space[z][y][x] = 0

    space = next_space

active = 0
for z, plane in space.items():
    for y, row in plane.items():
        for x, cell in row.items():
            active += cell

print(active)
