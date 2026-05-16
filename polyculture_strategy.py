import drone
import eyes
import mapper
import ops
import state
import strategy
import tools

block_width = 4
block_height = 8
base_item_priorities = [Items.Wood, Items.Hay, Items.Carrot]
search_limit = 3
entities_limit_rate = 0.5

def run_worker(args):
	if len(args) == 5:
		start_x, end_x, start_y, end_y, before_harvest_hook = args
	else:
		start_x, end_x, start_y, end_y = args
		before_harvest_hook = None

	width = end_x - start_x + 1
	height = end_y - start_y + 1
	grid_size = width * height

	entity_priorities = []
	for item in ([state.target_item] + base_item_priorities):
		for entity in mapper.item_to_entities(item):
			if entity not in entity_priorities:
				entity_priorities.append(entity)

	def check_plant_efficiency(entity, x, y, grid):
		if entity == Entities.Tree:
			if x == start_x or x == end_x or y == start_y or y == end_y:
				return False
			return Entities.Tree not in eyes.adjacent_values(grid, x - start_x, y - start_y)
		return True

	def check_plant(entity, x, y, grid):
		return (
			tools.is_valid_coords(x, y, start_x, end_x, start_y, end_y) and 
			grid[x - start_x][y - start_y] == None and 
			check_plant_efficiency(entity, x, y, grid)
		)

	def find_closest_efficient(center_x, center_y, entity, grid):
		dirs = ((1, -1), (-1, -1), (-1, 1), (1, 1))
		for offset in range(1, search_limit + 1):
			x = center_x
			y = center_y + offset
			for dir in dirs:
				for _ in range(offset):
					if check_plant(entity, x, y, grid):
						return x, y
					x = x + dir[0]
					y = y + dir[1]
		return None

	while num_items(state.target_item) <= state.target_quantity:
		grid = tools.generate_matrix(max(width, height), None)
		drone.goto((start_x + end_x) // 2, (start_y + end_y) // 2)

		queue = []
		x = get_pos_x()
		y = get_pos_y()
		entity = entity_priorities[0]
		while num_items(state.target_item) <= state.target_quantity:
			while num_items(state.target_item) <= state.target_quantity:
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
				grid[x - start_x][y - start_y] = entity
				entity, (x, y) = get_companion()
				if not check_plant(entity, x, y, grid):
					break
			if len(queue) > entities_limit_rate * grid_size:
				break
			for entity in entity_priorities:
				coords = find_closest_efficient(get_pos_x(), get_pos_y(), entity, grid)
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

def run(before_harvest_hook=None):
	args_list = tools.generate_subgrids(state.grid_size, block_width, block_height, before_harvest_hook)
	strategy.run_multiworker(run_worker, args_list, 0)
