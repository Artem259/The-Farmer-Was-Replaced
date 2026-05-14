import drone
import eyes
import ops
import state
import tools

entity_priorities = [Entities.Carrot, Entities.Tree, Entities.Bush, Entities.Grass]
search_limit = 3
entities_limit_rate = 0.1

grid_size = state.grid_size ** 2

def check_plant_efficiency(entity, x, y, grid):
	if entity == Entities.Tree:
		return Entities.Tree not in eyes.adjacent_values(grid, x, y)
	return True

def check_plant(entity, x, y, grid):
	return (
		tools.is_valid_coords(x, y) and 
		grid[x][y] == None and 
		check_plant_efficiency(entity, x, y, grid)
	)

def run(before_harvest_hook=None):
	grid = tools.generate_matrix(state.grid_size, None)
	def find_closest_efficient(start_x, start_y, entity):
		dirs = ((1, -1), (-1, -1), (-1, 1), (1, 1))
		for offset in range(1, search_limit + 1):
			x = start_x
			y = start_y + offset
			for dir in dirs:
				for _ in range(offset):
					if check_plant(entity, x, y, grid):
						return x, y
					x = (x + dir[0]) % state.grid_size
					y = (y + dir[1]) % state.grid_size
		return None

	queue = []
	x = get_pos_x()
	y = get_pos_y()
	entity = entity_priorities[0]		
	while True:
		while True:
			drone.goto(x, y)
			ops.safe_harvest()
			if not ops.safe_plant(entity):
				unsuccessful_entity = entity
				for try_entity in entity_priorities:
					if check_plant(try_entity, x, y, grid) and ops.safe_plant(try_entity):
						entity = try_entity
						break
				if entity == unsuccessful_entity:
					break
			queue.append((x, y))
			grid[x][y] = entity
			entity, (x, y) = get_companion()
			if not check_plant(entity, x, y, grid):
				break
		if len(queue) > entities_limit_rate * grid_size:
			break
		for entity in entity_priorities:
			coords = find_closest_efficient(get_pos_x(), get_pos_y(), entity)
			if coords != None:
				break
		if coords == None:
			break
		x, y = coords

	for x, y in queue:
		drone.goto(x, y)
		if before_harvest_hook != None:
			before_harvest_hook()
		ops.waitfor_safe_harvest()
