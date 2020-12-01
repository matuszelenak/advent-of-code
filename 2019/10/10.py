import math
from decimal import Decimal, ROUND_DOWN

field = [x.strip() for x in open('10.in').readlines()]
asteroids = []
for y in range(len(field)):
    for x in range(len(field[y])):
        if field[y][x] == '#':
            asteroids.append((x, y))

angles = [set() for _ in range(len(asteroids))]
for a, (a_x, a_y) in enumerate(asteroids):
    for b, (b_x, b_y) in enumerate(asteroids):
        angle = Decimal(math.atan2(b_y - a_y, b_x - a_x)).quantize(Decimal('.0001'), rounding=ROUND_DOWN)
        angles[a].add(angle)

print(max(map(len, angles)))
