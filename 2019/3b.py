def manhattan_from_zero(point):
	return abs(point[0]) + abs(point[1])

def load_path_points():
	instructions = input().split(',')
	x, y = 0, 0
	dirs = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}

	path_points = []
	for instruction in instructions:
		direction = dirs[instruction[0]]
		for step in range(int(instruction[1:])):
			x, y = x + direction[0], y + direction[1]
			path_points.append((x, y))

	return path_points

cable1 = load_path_points()
cable2 = load_path_points()

intersections = set(cable1).intersection(set(cable2))

least_steps = len(cable1) + len(cable2)
for intersect_point in intersections:
	steps_together = cable1.index(intersect_point) + cable2.index(intersect_point) + 2
	print(intersect_point, steps_together)
	least_steps = min(least_steps, steps_together)

print(least_steps)