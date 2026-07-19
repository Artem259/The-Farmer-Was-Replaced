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
search_limit = 2
queue_global_limit = 8
queue_local_limit_rate = 0.5

def harvest_worker(args):
	start_x, end_x, start_y, end_y, _ = args
	strategy.iterate_grid(
		(ops.clean_harvest,), start_x, end_x, start_y, end_y
	)

def polyculture_worker(args):
	start_x, end_x, start_y, end_y, (before_harvest_hook,) = args

	width = end_x - start_x + 1
	height = end_y - start_y + 1
	max_queue_size = width * height

	entity_priorities = []
	for item in ([state.target_item] + base_item_priorities):
		for entity in mapper.item_to_entities(item):
			if entity not in entity_priorities:
				entity_priorities.append(entity)

	def check_plant_inner(entity, x, y, grid):
		if grid[x - start_x][y - start_y] != None:
			return False
		if entity == Entities.Tree:
			return Entities.Tree not in eyes.adjacent_values(grid, x - start_x, y - start_y)
		return True

	def check_plant_outer(entity, x, y):
		return True

	def check_plant(entity, x, y, grid):
		if tools.is_valid_coords(x, y, start_x, end_x, start_y, end_y):
			return check_plant_inner(entity, x, y, grid)
		if tools.is_valid_coords(x, y):
			return check_plant_outer(entity, x, y)
		return False

	def find_closest_inner_plant(center_x, center_y, entity, grid):
		dirs = ((1, -1), (-1, -1), (-1, 1), (1, 1))
		for offset in range(1, search_limit + 1):
			x = center_x % state.grid_size
			y = (center_y + offset) % state.grid_size
			for dir in dirs:
				for _ in range(offset):
					if (
						tools.is_valid_coords(x, y, start_x, end_x, start_y, end_y) and 
						check_plant_inner(entity, x, y, grid)
					):
						return x, y
					x = (x + dir[0]) % state.grid_size
					y = (y + dir[1]) % state.grid_size
		return None

	def try_plant_entity(entity):
		if get_entity_type() != None:
			return False
		return ops.safe_plant(entity)

	def check_target_reached():
		return num_items(state.target_item) >= state.target_quantity

	while not check_target_reached():
		grid = tools.generate_matrix(max(width, height), None)
		drone.goto((start_x + end_x) // 2, (start_y + end_y) // 2)

		queue = []
		x = get_pos_x()
		y = get_pos_y()
		entity = entity_priorities[0]
		while not check_target_reached():
			while not check_target_reached():
				drone.goto(x, y)
				if not try_plant_entity(entity):
					fail_flag = True
					for entity in entity_priorities:
						if check_plant(entity, x, y, grid) and try_plant_entity(entity):
							fail_flag = False
							break
					if fail_flag:
						break
				if len(queue) > 0:
					queue[-1][2] = True
				queue.append([(x, y), entity, False])
				if tools.is_valid_coords(x, y, start_x, end_x, start_y, end_y):
					grid[x - start_x][y - start_y] = entity
				entity, (x, y) = get_companion()
				if not check_plant(entity, x, y, grid) or len(queue) >= queue_global_limit:
					break
			if len(queue) > queue_local_limit_rate * max_queue_size or len(queue) >= queue_global_limit:
				break
			for entity in entity_priorities:
				center_x = max(start_x, min(get_pos_x(), end_x))
				center_y = max(start_y, min(get_pos_y(), end_y))
				coords = find_closest_inner_plant(center_x, center_y, entity, grid)
				if coords != None:
					break
			if coords == None:
				break
			x, y = coords

		for i in range(len(queue)):
			(x, y), entity, has_companion = queue[i]
			drone.goto(x, y)
			if before_harvest_hook != None:
				before_harvest_hook()
			if i < len(queue) - 1 and entity == entity_priorities[0] and has_companion:
				ops.waitfor_safe_harvest(False)
			else:
				ops.waitfor_safe_harvest()

def run(before_harvest_hook=None):
	args_list = tools.generate_subgrids(state.grid_size, block_width, block_height, (before_harvest_hook,))
	strategy.run_multiworker(harvest_worker, args_list, 0)
	strategy.run_multiworker(polyculture_worker, args_list, 0)
