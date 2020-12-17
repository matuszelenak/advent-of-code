from collections import defaultdict
from itertools import product
from copy import deepcopy

hyperspace = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0))))
neighbor_deltas = set(product((1, 0, -1), repeat=4)) - {(0, 0, 0, 0)}

with open('17.in') as f:
    for y, row in enumerate(list(f.readlines())):
        for x, cell in enumerate(row):
            hyperspace[0][0][y][x] = 1 if cell == '#' else 0

for _ in range(6):
    coordinates = set()
    for w, space in hyperspace.items():
        for z, plane in space.items():
            for y, row in plane.items():
                for x, cell in row.items():
                    for dx, dy, dz, dw in neighbor_deltas:
                        coordinates.add((x + dx, y + dy, z + dz, w + dw))

    next_space = deepcopy(hyperspace)
    for x, y, z, w in coordinates:
        active_neighbors = 0
        for dx, dy, dz, dw in neighbor_deltas:
            nx, ny, nz, nw = x + dx, y + dy, z + dz, w + dw
            active_neighbors += hyperspace[nw][nz][ny][nx]
        if hyperspace[w][z][y][x] == 0 and active_neighbors == 3:
            next_space[w][z][y][x] = 1
        elif hyperspace[w][z][y][x] == 1 and active_neighbors not in (2, 3):
            next_space[w][z][y][x] = 0

    hyperspace = next_space

active = 0
for w, space in hyperspace.items():
    for z, plane in space.items():
        for y, row in plane.items():
            for x, cell in row.items():
                active += cell

print(active)
