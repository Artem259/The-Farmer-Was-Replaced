import drone
import eyes
import ops
import state
import strategy
import tools

block_width = 4
block_height = 8
shortcuts_limit_ratio = 0.4
tail_dist_limit = 3

grid_size = state.grid_size ** 2
last_id = grid_size - 1
directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

def harvest_worker(args):
	start_x, end_x, start_y, end_y = args
	strategy.iterate_grid(
		(ops.clean_harvest,), start_x, end_x, start_y, end_y
	)

def precompute_grid():
	if state.grid_size % 2 == 1:
		print("generate_grid", 0 / 0)

	def generate_cell(row, col):
		y = state.grid_size - 1 - row
		x = col
		if x == 0:
			return [last_id - y, None, []]
		full_rows = (state.grid_size - 1) * y - 1
		if y % 2 == 0:
			this_row = x
		else:
			this_row = state.grid_size - x
		return [full_rows + this_row, None, []]

	grid = tools.generate_matrix(state.grid_size, generate_cell, True)
	for x in range(state.grid_size):
		for y in range(state.grid_size):
			id = grid[x][y][0]
			adjacent = eyes.adjacent_values(grid, x, y, True)

			for dir_i in range(4):
				dir = dir_i
				adj = adjacent[dir_i]
				if adj == None:
					continue
				adj_id = adj[0]
				if adj_id == id + 1 or (adj_id == 0 and id == last_id):
					grid[x][y][1] = dir_i
				elif adj_id + 1 != id and not (adj_id == last_id and id == 0):
					grid[x][y][2].append((dir_i, adj_id))
	return grid

grid = precompute_grid()

def check_shortcut_efficiency(id, shortcut_id, apple_id, tail_id):
	next_id = (id + 1) % grid_size
	base_path = (apple_id - next_id) % grid_size
	shortcut_path = (apple_id - shortcut_id) % grid_size
	if shortcut_path >= base_path:
		return False, shortcut_path

	shortcut_dist = (shortcut_id - id) % grid_size
	tail_dist = (tail_id - id) % grid_size
	return shortcut_dist < tail_dist - tail_dist_limit, shortcut_path

def run():
	args_list = tools.generate_subgrids(state.grid_size, block_width, block_height)
	strategy.run_multiworker(harvest_worker, args_list, 0)

	drone.goto_center()
	change_hat(Hats.Dinosaur_Hat)

	x = get_pos_x()
	y = get_pos_y()
	stop_flag = False
	snake_len = 1
	tail_x, tail_y = x, y
	snake_grid = tools.generate_matrix(state.grid_size, None)
	while snake_len < grid_size and not stop_flag:
		apple_x, apple_y = measure()
		apple_id = grid[apple_x][apple_y][0]
		eaten = True
		while not (x == apple_x and y == apple_y):
			id, base_dir_i, shortcuts = grid[x][y]
			tail_id = grid[tail_x][tail_y][0]

			dir = None
			if snake_len <= shortcuts_limit_ratio * grid_size:
				best_shortcut_length = grid_size
				for dir_i, adj_id in shortcuts:
					d = directions[dir_i]
					is_valid_shortcut, shortcut_length = check_shortcut_efficiency(
						id, adj_id, apple_id, tail_id
					)
					if is_valid_shortcut and shortcut_length < best_shortcut_length:
						dir = d
						best_shortcut_length = shortcut_length
			if dir == None:
				dir = directions[base_dir_i]

			goto_result = drone.relative_goto(dir[0], dir[1], False)
			snake_grid[x][y] = dir
			x += dir[0]
			y += dir[1]
			if eaten:
				snake_len += 1
			else:
				tail_dir = snake_grid[tail_x][tail_y]
				tail_x += tail_dir[0]
				tail_y += tail_dir[1]
			if not goto_result:
				if snake_len < grid_size:
					stop_flag = True
				break
			eaten = False

	change_hat(Hats.Straw_Hat)
