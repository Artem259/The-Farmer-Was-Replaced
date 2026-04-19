import state

def _move(direction, distance=1):
	for _ in range(distance):
		move(direction)

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
		_move(East, east_dist)
	else:
		_move(West, west_dist)
	
	y = get_pos_y()
	north_dist = (to_y - y) % n
	south_dist = (y - to_y) % n
	if north_dist <= south_dist:
		_move(North, north_dist)
	else:
		_move(South, south_dist)

def relative_goto(d_x, d_y):
	to_x = (get_pos_x() + d_x) % state.grid_size
	to_y = (get_pos_y() + d_y) % state.grid_size
	goto(to_x, to_y)

def go_up(distance=1):
	relative_goto(0, distance)

def go_down(distance=1):
	relative_goto(0, -distance)

def go_right(distance=1):
	relative_goto(distance, 0)

def go_left(distance=1):
	relative_goto(-distance, 0)
