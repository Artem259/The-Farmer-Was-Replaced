import drone
import ops
import state
import tools
from weird_subs_strategy import calc_maze_quantity

iters_num = 300

def generate_grid():
	def generate_cell():
		return []
	grid = tools.generate_matrix(state.grid_size, generate_cell, True)
	return grid

def right_hand_traverse(grid):
	dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
	heading = 1
	x = 0
	y = 0
	while True:
		new_heading = (heading + 1) % 4
		while not drone.relative_goto(dirs[new_heading][0], dirs[new_heading][1], False):
			new_heading = (new_heading - 1) % 4
		if x == 0 and y == 0 and (dirs[new_heading] in grid[0][0]):
			break
		grid[x][y].append(dirs[new_heading])
		heading = new_heading
		x += dirs[heading][0]
		y += dirs[heading][1]

def bfs(to_x, to_y, grid):
	start_coords = (get_pos_x(), get_pos_y())

	path = {}
	visited = {start_coords}
	queue = [start_coords]
	i = 0
	while i < len(queue):
		x, y = queue[i]
		i += 1
		dirs = grid[x][y]
		for dir in dirs:
			next_x = x + dir[0]
			next_y = y + dir[1]
			next_coords = (next_x, next_y)
			if next_coords in visited:
				continue
			path[next_coords] = (x, y)
			visited.add(next_coords)
			queue.append(next_coords)
			if next_coords == (to_x, to_y):
				steps = []
				coords = (to_x, to_y)
				while coords != start_coords:
					next_coords = path[coords]
					d_x = coords[0] - next_coords[0]
					d_y = coords[1] - next_coords[1]
					steps.append((d_x, d_y))
					coords = next_coords
				return steps[::-1]
	return []

def run():
	drone.goto_bottom_left()

	while not ops.safe_plant(Entities.Bush):
		pass
	substance = calc_maze_quantity()
	use_item(Items.Weird_Substance, substance)

	grid = generate_grid()
	right_hand_traverse(grid)

	for i in range(iters_num):
		x, y = measure()
		path = bfs(x, y, grid)
		for d_x, d_y in path:
			drone.relative_goto(d_x, d_y, False)
		if i == iters_num - 1:
			ops.safe_harvest()
		else:
			use_item(Items.Weird_Substance, substance)
