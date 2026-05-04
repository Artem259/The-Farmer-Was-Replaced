import drone
import ops
import state
import strategy
import tools

min_petals = 7
max_petals = 15
block_width = 4
block_height = 8

def run_plant_worker(args):
	start_x, end_x, start_y, end_y = args
	drone.goto(start_x, start_y)

	buckets = []
	for _ in range(max_petals - min_petals + 1):
		buckets.append([])
	
	def plant_action():
		ops.safe_plant(Entities.Sunflower)
		petals = measure() - min_petals
		buckets[petals].append((get_pos_x(), get_pos_y()))

	strategy.iterate_grid(
		(ops.waitfor_safe_harvest, plant_action), start_x, end_x, start_y, end_y
	)
	return buckets

def run_harvest_worker(args):
	queue = args[0]
	for x, y in queue:
		drone.goto(x, y)
		ops.waitfor_safe_harvest()

def run():
	plant_args = tools.generate_subgrids(state.grid_size, block_width, block_height)

	all_buckets = strategy.run_multiworker(run_plant_worker, plant_args, True)

	for petals in range(max_petals - min_petals, -1, -1):
		harvest_args = []
		for block_buckets in all_buckets:
			harvest_args.append([[]])
			for cell in block_buckets[petals]:
				harvest_args[-1][0].append(cell)
		
		strategy.run_multiworker(run_harvest_worker, harvest_args, True)
