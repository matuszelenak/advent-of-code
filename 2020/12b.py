import math
import re


def rotate_point(pivot, point, a):
    ss = math.sin(a)
    cc = math.cos(a)

    x, y = point
    x -= pivot[0]
    y -= pivot[1]

    nx = x * cc - y * ss
    ny = x * ss + y * cc

    nx += pivot[0]
    ny += pivot[1]

    return nx, ny


with open('12.in') as f:
    directions = {
        (0, -1): 'N',
        (0, 1): 'S',
        (-1, 0): 'W',
        (1, 0): 'E'
    }
    deltas = {v: k for k, v in directions.items()}
    wp_x, wp_y = 10, -1
    ship_x, ship_y = 0, 0
    for line in f.readlines():
        command, value = re.match(r'([NSEWLRF])(\d+)', line).groups()
        value = int(value)
        if command in ('L', 'R'):
            value = -1 * value if command == 'L' else value
            angle = value * math.pi / 180
            wp_x, wp_y = rotate_point((ship_x, ship_y), (wp_x, wp_y), angle)
            continue

        if command == 'F':
            dx, dy = wp_x - ship_x, wp_y - ship_y
            ship_x += dx * value
            ship_y += dy * value
            wp_x += dx * value
            wp_y += dy * value

        else:
            dx, dy = deltas[command]
            wp_x += dx * value
            wp_y += dy * value

    print(abs(ship_x) + abs(ship_y))