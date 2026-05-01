import eyes
import polyculture_strategy
import state
import tools

def calc_maze_quantity():
	return state.grid_size * (2 ** (num_unlocked(Unlocks.Mazes) - 1)) 

def calc_target_quantity():
	return 2 * 300 * calc_maze_quantity()

def run():
	grid = tools.generate_matrix(state.grid_size, False)
	def before_harvest_hook():
		x = get_pos_x()
		y = get_pos_y()
		entity = get_entity_type()
		if entity != Entities.Bush and not grid[x][y]:
			if num_items(Items.Weird_Substance) > 0 and use_item(Items.Weird_Substance):
				grid[x][y] = not grid[x][y]
				for adj_x, adj_y in eyes.adjacent_coords(grid, x, y):
					grid[adj_x][adj_y] = not grid[adj_x][adj_y]
			else:
				use_item(Items.Fertilizer)
				grid[x][y] = not grid[x][y]

	polyculture_strategy.run(before_harvest_hook)
