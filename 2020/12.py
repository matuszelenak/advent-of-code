import math
import re


with open('12.in') as f:
    directions = {
        (0, -1): 'N',
        (0, 1): 'S',
        (-1, 0): 'W',
        (1, 0): 'E'
    }
    deltas = {v: k for k, v in directions.items()}
    x, y = 0, 0
    angle = 0
    direction = 'E'
    for line in f.readlines():
        command, value = re.match(r'([NSEWLRF])(\d+)', line).groups()
        value = int(value)
        if command in ('L', 'R'):
            value = -1 * value if command == 'L' else value
            angle += value * math.pi / 180
            dx, dy = round(math.cos(angle)), round(math.sin(angle))
            direction = directions[(dx, dy)]
            continue

        if command == 'F':
            dx, dy = deltas[direction]
        else:
            dx, dy = deltas[command]
        x = x + dx * value
        y = y + dy * value

    print(abs(x) + abs(y))