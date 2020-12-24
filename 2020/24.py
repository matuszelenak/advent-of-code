from collections import defaultdict
from copy import deepcopy
from typing import Tuple, Generator

deltas = {
    'e': (1, 0, -1),
    'w': (-1, 0, +1),
    'se': (0, +1, -1),
    'sw': (-1, +1, 0),
    'ne': (+1, -1, 0),
    'nw': (0, -1, +1)
}


def parse_directions(line) -> Generator[Tuple[int, int, int], None, None]:
    i = iter(line)
    while True:
        try:
            c = next(i)
            yield deltas[c] if c in ('e', 'w') else deltas[c + next(i)]
        except StopIteration:
            break


def iterate_grid(g) -> Generator[Tuple[Tuple[int, int, int], bool], None, None]:
    for x, plane in g.items():
        for y, row in plane.items():
            for z, tile in row.items():
                yield (x, y, z), tile


def iterate_neighbors(x, y, z) -> Generator[Tuple[int, int, int], None, None]:
    for dx, dy, dz in deltas.values():
        yield x + dx, y + dy, z + dz


def count_black(g):
    return sum(1 if t else 0 for _, t in iterate_grid(g))


def solve():
    grid = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: False)))

    with open('24.in') as f:
        for line in f.readlines():
            x, y, z = 0, 0, 0
            for dx, dy, dz in parse_directions(line.strip()):
                x += dx
                y += dy
                z += dz
            grid[x][y][z] = not grid[x][y][z]

    print(count_black(grid))

    for _ in range(100):
        current_coords = set()
        for (x, y, z), _ in iterate_grid(grid):
            current_coords.add((x, y, z))

        new_coords = deepcopy(current_coords)
        for x, y, z in current_coords:
            for nx, ny, nz in iterate_neighbors(x, y, z):
                if (nx, ny, nz) not in current_coords:
                    new_coords.add((nx, ny, nz))

        new_grid = deepcopy(grid)

        for x, y, z in new_coords:
            adjacent_black = sum(1 if grid[nx][ny][nz] else 0 for nx, ny, nz in iterate_neighbors(x, y, z))

            if (grid[x][y][z] and (adjacent_black == 0 or adjacent_black > 2)) or (not grid[x][y][z] and adjacent_black == 2):
                new_grid[x][y][z] = not grid[x][y][z]

        grid = new_grid

    print(count_black(grid))


solve()