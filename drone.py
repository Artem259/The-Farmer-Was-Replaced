def _move(direction, distance=1):
	for _ in range(distance):
		move(direction)

def go_up(distance=1):
	_move(North, distance)

def go_down(distance=1):
	_move(South, distance)

def go_right(distance=1):
	_move(East, distance)

def go_left(distance=1):
	_move(West, distance)
