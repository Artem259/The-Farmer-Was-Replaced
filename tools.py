import state

def generate_matrix(size, value):
	matrix = []
	for _ in range(size):
		row = []
		for _ in range(size):
			row.append(value)
		matrix.append(row)
	return matrix

def is_valid_coord(coord):
	return 0 <= coord < state.grid_size

def is_valid_coords(coord1, coord2):
	return is_valid_coord(coord1) and is_valid_coord(coord2)
