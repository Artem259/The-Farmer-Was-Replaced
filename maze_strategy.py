import drone
import ops
import state
import strategy
import tools
from weird_subs_strategy import calc_maze_quantity

block_width = 4
block_height = 8
iteration_seconds = 60

directions = ((0, 1, North), (1, 0, East), (0, -1, South), (-1, 0, West))

def generate_grid():
	def generate_cell(x, y):
		return [[], [False, False, False, False]]
	grid = tools.generate_matrix(state.grid_size, generate_cell, True)
	return grid

def copy_grid(grid):
	def copy_cell(x, y):
		cell = grid[x][y]
		return [cell[0][:], cell[1][:]]
	copied_grid = tools.generate_matrix(state.grid_size, copy_cell, True)
	return copied_grid

def get_available_dirs():
	available_dirs = []
	for i in range(4):
		if can_move(directions[i][2]):
			available_dirs.append(i)
	return available_dirs

def update_grid(x, y, dir_i, grid):
	if not grid[x][y][1][dir_i]:
		grid[x][y][0].append(dir_i)
		grid[x][y][1][dir_i] = True

		dir = directions[dir_i]
		x = x + dir[0]
		y = y + dir[1]
		if tools.is_valid_coords(x, y):
			dir_i = (dir_i + 2) % 4
			grid[x][y][0].append(dir_i)
			grid[x][y][1][dir_i] = True

def exploration_traverse(args):
	d_x, d_y, heading = args
	drone.relative_goto(d_x, d_y, False)

	start_x = get_pos_x()
	start_y = get_pos_y()
	x = start_x
	y = start_y
	cell_data = []
	child_workers = []
	while True:
		available_dirs = get_available_dirs()
		if not (x == 0 and y == 0):
			i = (heading + 2) % 4
			cell_data.append((x, y, i))
			available_dirs.remove(i)

		if len(available_dirs) == 0:
			break
		elif len(available_dirs) > 1:
			for dir_i in available_dirs[:-1]:
				dir = directions[dir_i]
				worker = None
				while worker == None:
					worker = spawn_drone(exploration_traverse, (dir[0], dir[1], dir_i))
				child_workers.append(worker)
		for dir_i in available_dirs:
			cell_data.append((x, y, dir_i))

		dir_i = available_dirs[-1]
		dir = directions[dir_i]
		drone.relative_goto(dir[0], dir[1], False)
		x += dir[0]
		y += dir[1]
		heading = dir_i
	return cell_data, child_workers

def add_new_available_dirs(x, y, new_grid, new_available_dirs):
	for dir_i in get_available_dirs():
		if not new_grid[x][y][1][dir_i]:
			update_grid(x, y, dir_i, new_grid)
			new_available_dirs.append((x, y, dir_i))

def bfs_check(start_x, start_y, end_x, end_y, old_grid, center_set):
	start_coords = (start_x, start_y)
	end_coords = (end_x, end_y)
	if start_coords in center_set:
		return start_coords == end_coords

	visited = {start_coords}
	queue = [start_coords]
	i = 0
	while i < len(queue):
		x, y = queue[i]
		i += 1
		dirs = old_grid[x][y][0]
		for dir_i in dirs:
			dir = directions[dir_i]
			next_x = x + dir[0]
			next_y = y + dir[1]
			next_coords = (next_x, next_y)
			if next_coords in visited:
				continue
			visited.add(next_coords)
			queue.append(next_coords)

			if next_coords in center_set:
				return next_coords == end_coords
	print("bfs_check", 0 / 0)

def bfs_goto(start_x, start_y, end_x, end_y, new_grid, new_available_dirs):
	start_coords = (start_x, start_y)
	end_coords = (end_x, end_y)
	if start_coords == end_coords:
		return

	path = {}
	visited = {start_coords}
	queue = [start_coords]
	i = 0
	while i < len(queue):
		x, y = queue[i]
		i += 1
		dirs = new_grid[x][y][0]
		for dir_i in dirs:
			dir = directions[dir_i]
			next_x = x + dir[0]
			next_y = y + dir[1]
			next_coords = (next_x, next_y)
			if next_coords in visited:
				continue
			path[next_coords] = (x, y)
			visited.add(next_coords)
			queue.append(next_coords)
			if next_coords == end_coords:
				coords = end_coords
				steps = []
				while coords != start_coords:
					next_coords = path[coords]
					d_x = coords[0] - next_coords[0]
					d_y = coords[1] - next_coords[1]
					steps.append((d_x, d_y))
					coords = next_coords
				x, y = start_coords
				for d_x, d_y in steps[::-1]:
					drone.relative_goto(d_x, d_y, False)
					x += d_x
					y += d_y
					add_new_available_dirs(x, y, new_grid, new_available_dirs)
				return

def exploitation_traverse(args):
	mid_x, mid_y, center_set, old_grid = args
	substance = calc_maze_quantity()
	new_grid = copy_grid(old_grid)

	start_time = get_time()
	new_available_dirs = []
	skip_treasure_coords = None
	stop_flag = False
	while True:
		treasure_coords = measure()
		if (
			treasure_coords == None or 
			len(treasure_coords) != 2 or 
			get_time() - start_time > iteration_seconds
		):
			break
		if treasure_coords == skip_treasure_coords:
			continue
		treasure_x, treasure_y = treasure_coords
		if bfs_check(treasure_x, treasure_y, mid_x, mid_y, old_grid, center_set):
			bfs_goto(get_pos_x(), get_pos_y(), treasure_x, treasure_y, new_grid, new_available_dirs)
			if stop_flag:
				ops.safe_harvest()
				break
			gold_before = num_items(Items.Gold)
			use_item(Items.Weird_Substance, substance)
			gold_after = num_items(Items.Gold)
			stop_flag = (gold_before == gold_after)
		else:
			skip_treasure_coords = treasure_coords
			bfs_goto(get_pos_x(), get_pos_y(), mid_x, mid_y, new_grid, new_available_dirs)	
	return stop_flag, new_available_dirs

def run():
	drone.goto_bottom_left()

	if not ops.safe_plant(Entities.Bush, False):
		print("ops.safe_plant", 0 / 0)
	substance = calc_maze_quantity()
	use_item(Items.Weird_Substance, substance)

	worker = strategy.spawn_workers(exploration_traverse, [(0, 0, 0)])
	root_result = strategy.join_workers(worker)[0]

	grid = generate_grid()
	results_stack = [root_result]
	while results_stack:
		cell_data, child_workers = results_stack.pop()
		for x, y, dir_i in cell_data:
			update_grid(x, y, dir_i, grid)
		child_results = strategy.join_workers(child_workers)
		for child_result in child_results:
			results_stack.append(child_result)

	subgrids = tools.generate_subgrids(state.grid_size, block_width, block_height)
	args_list = []
	center_set = set()
	for start_x, end_x, start_y, end_y in subgrids:
		mid_x = (start_x + end_x) // 2
		mid_y = (start_y + end_y) // 2
		center_set.add((mid_x, mid_y))
		args_list.append([mid_x, mid_y, center_set, None])

	while True: 
		for args in args_list:
			args[3] = grid
		results = strategy.run_multiworker(exploitation_traverse, args_list, len(args_list) // 2)
		for stop_flag, new_available_dirs in results:
			if stop_flag:
				return
			for x, y, dir_i in new_available_dirs:
				update_grid(x, y, dir_i, grid)
