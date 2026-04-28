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
		dist = state.grid_size - 1
		while dist >= 2:
			flag = False
			for _ in range(dist):
				if measure() > measure(next_dir):
					swap(next_dir)
					flag = True
				go_forward()
			if not flag:
				return
			go_backward()
			dist -= 1

			flag = False
			for _ in range(dist):
				if measure(prev_dir) > measure():
					swap(prev_dir)
					flag = True
				go_backward()
			if not flag:
				return
			go_forward()
			dist -= 1

	for y in range(state.grid_size - 1, -1, -1):
		drone.goto(0, y)
		sort_line(drone.go_right, drone.go_left, get_pos_x, West, East)

	for x in range(state.grid_size - 1, -1, -1):
		drone.goto(x, 0)
		sort_line(drone.go_up, drone.go_down, get_pos_y, South, North)

	ops.safe_harvest()
