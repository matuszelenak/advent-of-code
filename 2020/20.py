import math
from collections import defaultdict
from typing import Dict, List, Set
import re
import copy


def iterate_placements(tile):
    def iterate_rotations(flip_placement):
        rotated = copy.deepcopy(flip_placement)
        for _ in range(4):
            yield rotated
            rotated = list(zip(*rotated[::-1]))

    yield from iterate_rotations(tile)
    yield from iterate_rotations([row[::-1] for row in tile])


def get_border(tile, side) -> str:
    if side == 'top':
        s = tile[0][::]
    elif side == 'left':
        s = [row[0] for row in tile]
    elif side == 'right':
        s = [row[-1] for row in tile]
    elif side == 'bottom':
        s = tile[-1][::]
    else:
        s = None
    if s:
        return ''.join(s)


def fill_into_grid(grid, tile, x, y):
    for row_id, row in enumerate(tile):
        for cell_id, cell in enumerate(row):
            grid[y * len(tile) + row_id][x * len(tile) + cell_id] = cell


def extend(start_tile_id, start_tile, axis, neighbors, tiles):
    previous_tile_id, previous_tile = start_tile_id, start_tile
    if axis == 'horizontal':
        first, second = 'right', 'left'
    else:
        first, second = 'bottom', 'top'
    while True:
        aligning_to = get_border(previous_tile, first)
        found_alignment = False
        for neighbor_id, _ in neighbors[previous_tile_id]:
            for placement in iterate_placements(tiles[neighbor_id]):
                if aligning_to == get_border(placement, second):
                    yield neighbor_id, placement
                    previous_tile_id = neighbor_id
                    previous_tile = placement
                    found_alignment = True
                    break
        if not found_alignment:
            break


def print_grid(grid, tile_size, monster_coords=None):
    monster_coords = monster_coords or set()
    for row_id, row in enumerate(grid):
        for col_id, cell in enumerate(row):
            if (row_id, col_id) in monster_coords:
                print('O', end='')
            else:
                print(cell or '', end='')
            if (col_id + 1) % tile_size == 0:
                print(' ', end='')

        if (row_id + 1) % tile_size == 0:
            print()

        print()


def trim_borders(tile):
    return [row[1:-1] for row in tile[1:-1]]


def find_monsters(grid):
    def two_dim_slice(area, sx, ex, sy, ey):
        return [row[sx:ex] for row in area[sy:ey]]

    monster = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]
    monster = [[x for x in row] for row in monster]
    m_h, m_w = len(monster), len(monster[0])

    def check_area(area_x, area_y):
        area = two_dim_slice(grid, area_x, area_x + m_w, area_y, area_y + m_h)
        has_monster = True
        potential_monster = set()
        for row_id, (area_row, monster_row) in enumerate(zip(area, monster)):
            for col_id, (area_cell, monster_cell) in enumerate(zip(area_row, monster_row)):
                if (area_cell, monster_cell) == ('.', '#'):
                    has_monster = False
                elif (area_cell, monster_cell) == ('#', '#'):
                    potential_monster.add((area_y + row_id, area_x + col_id))

        if not has_monster:
            potential_monster.clear()

        return potential_monster

    monster_coords = set()
    for y in range(len(grid) - m_h):
        for x in range(len(grid[0]) - m_w):
            m = check_area(x, y)
            monster_coords |= m

    if len(monster_coords) != 0:
        print_grid(grid, 8, monster_coords)

    return sum(sum([1 for cell in row if cell == '#']) for row in grid) - len(monster_coords)


def solve():
    image_data = open('20.in').readlines()
    tiles: Dict[int, List[List[str]]] = {}
    current_tile_id = 0
    current_tile = []
    for line in image_data:
        line = line.strip()
        if not line:
            tiles[current_tile_id] = current_tile
            current_tile = []
            continue

        m = re.match(r'Tile (\d+):', line)
        if m:
            current_tile_id = int(m.groups()[0])
            continue
        current_tile.append([c for c in line])

    borders: Dict[str, Set[int]] = defaultdict(set)
    for tile_id, tile in tiles.items():
        for placement in iterate_placements(tile):
            for border_side in ('left', 'right', 'top', 'bottom'):
                borders[get_border(placement, border_side)].add(tile_id)

    deleted = set()
    for b in set(borders.keys()):
        if b in deleted:
            continue
        rb = b[::-1]
        if rb in borders:
            borders.pop(rb)
            deleted.add(rb)

    neighbors = defaultdict(list)
    for border, tile_set in borders.items():
        if len(tile_set) == 2:
            tile_a, tile_b = list(tile_set)
            neighbors[tile_a].append((tile_b, border))
            neighbors[tile_b].append((tile_a, border))

    m = 1
    corner_tiles = []
    for tile_id, neighbor_list in neighbors.items():
        if len(neighbor_list) == 2:
            m *= tile_id
            corner_tiles.append(tile_id)
    print(m)

    grid_side_size = int(math.sqrt(len(tiles)))
    id_grid = [[None for _ in range(grid_side_size)] for _ in range(grid_side_size)]
    grid = [[None for _ in range(grid_side_size * 8)] for _ in range(grid_side_size * 8)]

    # Orient the starting tile
    starting_tile_id = corner_tiles[0]
    starting_tile_shared_sides = set(
        [''.join(border) for n, border in neighbors[starting_tile_id]] + [''.join(border[::-1]) for n, border in
                                                                          neighbors[starting_tile_id]]
    )

    adjusted_starting_tile = None
    for tile_placement in iterate_placements(tiles[starting_tile_id]):
        bottom, right = get_border(tile_placement, 'bottom'), get_border(tile_placement, 'right')
        if bottom in starting_tile_shared_sides and right in starting_tile_shared_sides:
            adjusted_starting_tile = tile_placement
            break

    diagonal_tile = adjusted_starting_tile
    diagonal_tile_id = starting_tile_id

    for diagonal_id in range(grid_side_size - 1):
        id_grid[diagonal_id][diagonal_id] = diagonal_tile_id
        fill_into_grid(grid, trim_borders(diagonal_tile), diagonal_id, diagonal_id)

        first_horizontal, first_vertical = None, None
        horizontal_extension = extend(diagonal_tile_id, diagonal_tile, 'horizontal', neighbors, tiles)
        vertical_extension = extend(diagonal_tile_id, diagonal_tile, 'vertical', neighbors, tiles)

        for extension_id, (_id, extending_tile) in enumerate(horizontal_extension):
            first_horizontal = first_horizontal or (_id, extending_tile)
            fill_into_grid(grid, trim_borders(extending_tile), diagonal_id + extension_id + 1, diagonal_id)
            id_grid[diagonal_id][diagonal_id + extension_id + 1] = _id

        for extension_id, (_id, extending_tile) in enumerate(vertical_extension):
            first_vertical = first_vertical or (_id, extending_tile)
            fill_into_grid(grid, trim_borders(extending_tile), diagonal_id, diagonal_id + extension_id + 1)
            id_grid[diagonal_id + extension_id + 1][diagonal_id] = _id

        r = get_border(first_vertical[1], 'right')
        b = get_border(first_horizontal[1], 'bottom')
        diagonal_tile_id = next(iter(
            {neighbor_id for neighbor_id, _ in neighbors[first_horizontal[0]]} &
            {neighbor_id for neighbor_id, _ in neighbors[first_vertical[0]]} -
            {diagonal_tile_id}
        ))

        for placement in iterate_placements(tiles[diagonal_tile_id]):
            if get_border(placement, 'top') == b or get_border(placement, 'left') == r:
                diagonal_tile = placement

    id_grid[-1][-1] = diagonal_tile_id
    fill_into_grid(grid, trim_borders(diagonal_tile), grid_side_size - 1, grid_side_size - 1)

    print(min(find_monsters(placement) for placement in iterate_placements(grid)))


solve()
