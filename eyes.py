import state

def any_adjacent_coords(x, y):
	dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
	adjacent_coords = []
	for dir in dirs:
		next_x = x + dir[0]
		next_y = y + dir[1]
		is_valid_next_x = (0 <= next_x < state.grid_size)
		is_valid_next_y = (0 <= next_y < state.grid_size)
		if is_valid_next_x and is_valid_next_y:
			adjacent_coords.append((next_x, next_y))
	return adjacent_coords

def drone_adjacent_coords():
	return any_adjacent_coords(get_pos_x(), get_pos_y())

def any_adjacent_entities(x, y):
	adjacent_cells = any_adjacent_coords(x, y)
	adjacent_entities = []
	for x, y in adjacent_cells:
		adjacent_entities.append(state.grid_entities[x][y])
	return adjacent_entities

def drone_adjacent_entities():
	return any_adjacent_entities(get_pos_x(), get_pos_y())
