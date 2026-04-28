import drone
import ops
import state

pumpkin_max_size = -1

if pumpkin_max_size == -1:
	pumpkin_size = state.grid_size
else:
	pumpkin_size = min(pumpkin_max_size, state.grid_size)

def run():
	drone.goto_upper_left()

	queue = []
	for y in range(get_pos_y(), get_pos_y() - pumpkin_size, -1):
		for x in range(get_pos_x(), get_pos_x() + pumpkin_size):
			queue.append((x, y))

	while queue:
		new_queue = []
		for i in range(len(queue)):
			drone.goto(queue[i][0], queue[i][1])
			if get_entity_type() == Entities.Pumpkin and can_harvest():
				continue
			ops.safe_harvest()
			ops.safe_plant(Entities.Pumpkin)
			new_queue.append(queue[i])
		queue = new_queue
	ops.safe_harvest()
