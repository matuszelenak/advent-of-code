from collections import defaultdict

edges = [x.strip().split(')') for x in open('6.in').readlines()]

edge_map = defaultdict(list)
for a, b in edges:
    edge_map[a].append(b)
    edge_map[b].append(a)

current_layer = ['YOU']
current_dist = 0
processed = []
while True:
    processed += current_layer
    next_layer = [neighbor for current_node in current_layer for neighbor in edge_map[current_node] if neighbor not in processed]
    current_dist += 1
    if 'SAN' in next_layer:
        print(current_dist - 2)
        break
    current_layer = next_layer
