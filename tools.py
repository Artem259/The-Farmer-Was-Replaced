import state

def generate_matrix(size, value, callable=False):
	matrix = []
	for _ in range(size):
		row = []
		for _ in range(size):
			if callable:
				val = value()
			else:
				val = value
			row.append(val)
		matrix.append(row)
	return matrix

def is_valid_coord(coord):
	return 0 <= coord < state.grid_size

def is_valid_coords(coord1, coord2):
	return is_valid_coord(coord1) and is_valid_coord(coord2)
