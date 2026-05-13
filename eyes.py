def adjacent_coords(grid, x, y, return_invalid=False):
	dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
	coords = []
	for dir in dirs:
		next_x = x + dir[0]
		next_y = y + dir[1]
		is_valid_next_x = (0 <= next_x < len(grid))
		is_valid_next_y = (0 <= next_y < len(grid[0]))
		if is_valid_next_x and is_valid_next_y:
			coords.append((next_x, next_y))
		elif return_invalid:
			coords.append(None)
	return coords

def adjacent_values(grid, x, y, return_invalid=False):
	coords = adjacent_coords(grid, x, y, return_invalid)
	values = []
	for coord in coords:
		if coord == None:
			values.append(None)
		else:
			x, y = coord
			values.append(grid[x][y])
	return values
