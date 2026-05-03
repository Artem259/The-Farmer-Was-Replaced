import state
import tools

def _move(direction, distance=1):
	for _ in range(distance):
		if not move(direction):
			return False
	return True

def goto(to_x, to_y):
	n = get_world_size()
	if to_x < 0 or to_y < 0:
		print("goto_1", 0 / 0)
	if to_x >= n or to_y >= n:
		print("goto_2", 0 / 0)
	if to_x >= state.grid_size or to_y >= state.grid_size:
		print("goto_3", 0 / 0)
	
	x = get_pos_x()
	east_dist = (to_x - x) % n
	west_dist = (x - to_x) % n
	if east_dist <= west_dist:
		result = _move(East, east_dist)
	else:
		result = _move(West, west_dist)
	if not result:
		return False
	
	y = get_pos_y()
	north_dist = (to_y - y) % n
	south_dist = (y - to_y) % n
	if north_dist <= south_dist:
		result = _move(North, north_dist)
	else:
		result = _move(South, south_dist)
	return result

def relative_goto(d_x, d_y, teleport=True):
	if teleport:
		to_x = (get_pos_x() + d_x) % state.grid_size
		to_y = (get_pos_y() + d_y) % state.grid_size
	else:
		to_x = get_pos_x() + d_x
		to_y = get_pos_y() + d_y
		if not tools.is_valid_coords(to_x, to_y):
			return False
	return goto(to_x, to_y)

def go_up(distance=1):
	return relative_goto(0, distance)

def go_down(distance=1):
	return relative_goto(0, -distance)

def go_right(distance=1):
	return relative_goto(distance, 0)

def go_left(distance=1):
	return relative_goto(-distance, 0)

def goto_upper_left():
	return goto(0, state.grid_size - 1)

def goto_bottom_left():
	return goto(0, 0)

def goto_center():
	return goto(state.grid_size // 2, state.grid_size // 2)
