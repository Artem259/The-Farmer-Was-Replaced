def adjacent_coords(grid, x, y):
	dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
	coords = []
	for dir in dirs:
		next_x = x + dir[0]
		next_y = y + dir[1]
		is_valid_next_x = (0 <= next_x < len(grid))
		is_valid_next_y = (0 <= next_y < len(grid[0]))
		if is_valid_next_x and is_valid_next_y:
			coords.append((next_x, next_y))
	return coords

def adjacent_values(grid, x, y):
	coords = adjacent_coords(grid, x, y)
	values = []
	for x, y in coords:
		values.append(grid[x][y])
	return values
