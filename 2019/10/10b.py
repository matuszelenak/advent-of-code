import math
import heapq
from collections import defaultdict
from decimal import Decimal, ROUND_DOWN

field = [x.strip() for x in open('10.in').readlines()]
asteroids = []
for y in range(len(field)):
    for x in range(len(field[y])):
        if field[y][x] == '#':
            asteroids.append((x, y))

angles = [[0 for _ in range(len(asteroids))] for _ in range(len(asteroids))]
for a, (a_x, a_y) in enumerate(asteroids):
    for b, (b_x, b_y) in enumerate(asteroids):
        if a == b:
            continue

        angle = Decimal(math.atan2(b_y - a_y, b_x - a_x) * 180 / math.pi).quantize(Decimal('.0001'), rounding=ROUND_DOWN)
        if angle < 0:
            angle += 360
        angle += 90
        if angle >= 360:
            angle -= 360

        angles[a][b] = angle

station_index = max(map(lambda x: (len(set(x[1])), x[0]), enumerate(angles)))[1]
station_x, station_y = asteroids[station_index]

angle_bins = defaultdict(list)
for other_index, (other_x, other_y) in enumerate(asteroids):
    if other_index == station_index:
        continue

    distance_square = (other_y - station_y)**2 + (other_x - station_x)**2
    angle_bins[angles[station_index][other_index]].append((distance_square, other_index))

[heapq.heapify(b) for b in angle_bins.values()]
sorted_angles = sorted(set(angles[station_index]))
vaporized = []
while True:
    has_elements = False
    for angle in sorted_angles:
        if len(angle_bins[angle]) > 0:
            has_elements = True
            _, asteroid_index = heapq.heappop(angle_bins[angle])
            vaporized.append(asteroids[asteroid_index])
    if not has_elements:
        break

print(vaporized[199])
