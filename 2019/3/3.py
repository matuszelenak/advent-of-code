def manhattan_from_zero(point):
    return abs(point[0]) + abs(point[1])


def load_path_points():
    instructions = input().split(',')
    x, y = 0, 0
    dirs = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}

    path_points = set()
    for instruction in instructions:
        direction = dirs[instruction[0]]
        for step in range(int(instruction[1:])):
            x, y = x + direction[0], y + direction[1]
            path_points.add((x, y))

    return path_points


cable1 = load_path_points()
cable2 = load_path_points()

print(sorted(list(map(manhattan_from_zero, cable1.intersection(cable2))))[0])
