import drone
import eyes
import ops
import state
import tools

base_entity = Entities.Carrot
fallback_entity = Entities.Grass
search_limit = state.grid_size
entities_limit_rate = 0.1

grid_size = state.grid_size ** 2

def run(before_harvest_hook=None):
	grid = tools.generate_matrix(state.grid_size, None)
	def find_closest_empty(start_x, start_y):
		dirs = ((1, -1), (-1, -1), (-1, 1), (1, 1))
		for offset in range(1, search_limit):
			x = start_x
			y = start_y + offset
			for dir in dirs:
				for _ in range(offset):
					if (
						tools.is_valid_coords(x, y) and 
						grid[x][y] == None
					):
						return x, y
					x = (x + dir[0]) % get_world_size()
					y = (y + dir[1]) % get_world_size()
		return None

	queue = []
	while True:
		x = get_pos_x()
		y = get_pos_y()
		entity = base_entity
		while True:
			drone.goto(x, y)
			ops.safe_harvest()
			if not ops.safe_plant(entity):
				ops.safe_plant(fallback_entity)
			queue.append((x, y))
			grid[x][y] = entity
			entity, (x, y) = get_companion()
			if (
				not tools.is_valid_coords(x, y) or 
				grid[x][y] != None or 
				(
					entity == Entities.Tree and 
					Entities.Tree in eyes.adjacent_values(grid, x, y)
				)
			):
				break
		if len(queue) > entities_limit_rate * grid_size:
			break
		coords = find_closest_empty(get_pos_x(), get_pos_y())
		if coords == None:
			break
		drone.goto(coords[0], coords[1])

	for x, y in queue:
		drone.goto(x, y)
		if before_harvest_hook != None:
			before_harvest_hook()
		while not ops.safe_harvest():
			pass
