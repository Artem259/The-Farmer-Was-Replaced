import state

def generate_matrix(size, value, callable=False):
	matrix = []
	for i in range(size):
		row = []
		for j in range(size):
			if callable:
				val = value(i, j)
			else:
				val = value
			row.append(val)
		matrix.append(row)
	return matrix

def is_valid_coord(coord):
	return 0 <= coord < state.grid_size

def is_valid_coords(coord1, coord2):
	return is_valid_coord(coord1) and is_valid_coord(coord2)

def generate_subgrids(grid_size, block_width, block_height, data=None):
	subgrids = []
	for start_x in range(0, grid_size, block_width):
		for start_y in range(0, grid_size, block_height):
			end_x = min(start_x + block_width - 1, grid_size - 1)
			end_y = min(start_y + block_height - 1, grid_size - 1)
			if data != None:
				subgrids.append((start_x, end_x, start_y, end_y, data))
			else:
				subgrids.append((start_x, end_x, start_y, end_y))
	return subgrids
