import drone
import ops
import strategy
import state

width = 4
height = 8

def run_worker(args):
	start_x, end_x, start_y, end_y = args
	drone.goto(start_x, start_y)

	queue = []
	for y in range(start_y, end_y + 1):
		for x in range(start_x, end_x + 1):
			queue.append((x, y))

	while queue:
		new_queue = []
		for i in range(len(queue)):
			drone.goto(queue[i][0], queue[i][1])
			entity = get_entity_type()
			if entity == Entities.Pumpkin and can_harvest():
				continue
			if entity != Entities.Pumpkin:
				ops.safe_harvest()
				ops.safe_plant(Entities.Pumpkin)
			new_queue.append(queue[i])
		queue = new_queue

def run():
	args_list = []
	for start_x in range(0, state.grid_size, width):
		for start_y in range(0, state.grid_size, height):
			end_x = min(start_x + width - 1, state.grid_size - 1)
			end_y = min(start_y + height - 1, state.grid_size - 1)
			args_list.append((start_x, end_x, start_y, end_y))

	strategy.run_multiworker(run_worker, args_list, True)
	ops.safe_harvest()
