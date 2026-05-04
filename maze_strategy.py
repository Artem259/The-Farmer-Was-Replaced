import drone
import ops
import state
import strategy
import tools
from weird_subs_strategy import calc_maze_quantity

block_width = 4
block_height = 8
iteration_seconds = 120

directions = ((0, 1, North), (1, 0, East), (0, -1, South), (-1, 0, West))

def generate_grid():
	def generate_cell(x, y):
		return [[], [False, False, False, False]]
	grid = tools.generate_matrix(state.grid_size, generate_cell, True)
	return grid

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

def add_new_available_dirs(x, y, grid, new_available_dirs):
	for dir_i in get_available_dirs():
		if not grid[x][y][1][dir_i]:
			update_grid(x, y, dir_i, grid)
			new_available_dirs.append((x, y, dir_i))

def bfs_goto(to_x, to_y, grid, new_available_dirs):
	start_coords = (get_pos_x(), get_pos_y())
	if start_coords == (to_x, to_y):
		return

	path = {}
	visited = {start_coords}
	queue = [start_coords]
	i = 0
	while i < len(queue):
		x, y = queue[i]
		i += 1
		dirs = grid[x][y][0]
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
			if next_coords == (to_x, to_y):
				coords = (to_x, to_y)
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
					add_new_available_dirs(x, y, grid, new_available_dirs)
				return

def exploitation_traverse(args):
	start_x, end_x, start_y, end_y, grid = args
	mid_x = (start_x + end_x) // 2
	mid_y = (start_y + end_y) // 2
	substance = calc_maze_quantity()
	
	start_time = get_time()
	new_available_dirs = []
	stop_flag = False
	while True:
		value = measure()
		if (
			value == None or 
			len(value) != 2 or 
			get_time() - start_time > iteration_seconds
		):
			break
		x, y = value
		if not (start_x <= x <= end_x and start_y <= y <= end_y):
			bfs_goto(mid_x, mid_y, grid, new_available_dirs)
			continue
		bfs_goto(x, y, grid, new_available_dirs)
		if stop_flag:
			ops.safe_harvest()
			break

		gold_before = num_items(Items.Gold)
		use_item(Items.Weird_Substance, substance)
		gold_after = num_items(Items.Gold)
		stop_flag = (gold_before == gold_after)
	return stop_flag, new_available_dirs

def run():
	drone.goto_bottom_left()

	while not ops.safe_plant(Entities.Bush):
		pass
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

	while True:
		args_list = tools.generate_subgrids(state.grid_size, block_width, block_height, grid)
		results = strategy.run_multiworker(exploitation_traverse, args_list, True)
		for stop_flag, new_available_dirs in results:
			if stop_flag:
				return
			for x, y, dir_i in new_available_dirs:
				update_grid(x, y, dir_i, grid)
