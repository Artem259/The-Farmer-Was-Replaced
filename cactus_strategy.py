import drone
import ops
import state
import strategy

def run():
	def harvest_action():
		while not ops.safe_harvest():
			pass
		return True

	def plant_action():
		ops.safe_plant(Entities.Cactus)

	strategy.iterate_grid((harvest_action, plant_action))

	def sort_line(go_forward, go_backward, get_pos, prev_dir, next_dir):
		start = 0
		end = state.grid_size - 1
		while start < end:
			last_swap = 0
			for step in range(end - start):
				if measure() > measure(next_dir):
					swap(next_dir)
					last_swap = step
				go_forward()
			end = start + last_swap
			go_backward(get_pos() - end)

			last_swap = 0
			for step in range(end - start):
				if measure(prev_dir) > measure():
					swap(prev_dir)
					last_swap = step
				go_backward()
			start = end - last_swap
			go_forward(start - get_pos())

	for y in range(state.grid_size - 1, -1, -1):
		drone.goto(0, y)
		sort_line(drone.go_right, drone.go_left, get_pos_x, West, East)

	for x in range(state.grid_size - 1, -1, -1):
		drone.goto(x, 0)
		sort_line(drone.go_up, drone.go_down, get_pos_y, South, North)

	ops.safe_harvest()
