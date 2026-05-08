import ops
import state
import strategy
import tools

block_width = 4
block_height = 8
entities = (Entities.Tree, Entities.Grass)

def run_worker(args):
	start_x, end_x, start_y, end_y = args

	def plant_action():
		x = get_pos_x()
		y = get_pos_y()
		ops.safe_plant(entities[(x + y) % 2])

	strategy.iterate_grid(
		(ops.waitfor_safe_harvest, plant_action), start_x, end_x, start_y, end_y
	)

def run():
	args_list = tools.generate_subgrids(state.grid_size, block_width, block_height)
	strategy.run_multiworker(run_worker, args_list, 0)
