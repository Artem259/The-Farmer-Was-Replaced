import drone
import ops
import strategy
import state
import tools

block_width = 4
block_height = 8

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
	args_list = tools.generate_subgrids(state.grid_size, block_width, block_height)
	strategy.run_multiworker(run_worker, args_list, True)
	ops.safe_harvest()
