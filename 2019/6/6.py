from collections import defaultdict


def collect_orbits(planet, edge_map, current):
    return sum(collect_orbits(next_planet, edge_map, current + 1) for next_planet in edge_map[planet]) + current


edges = [x.strip().split(')') for x in open('6.in').readlines()]

edge_map = defaultdict(list)
for a, b in edges:
    edge_map[a].append(b)

print(collect_orbits('COM', edge_map, 0))
