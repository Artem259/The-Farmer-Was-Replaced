import drone
import state

def iterate_grid(action_chain):
	drone.goto_upper_left()
	n = len(action_chain)
	for row in range(state.grid_size):
		for col in range(state.grid_size):
			i = 0
			while i < n and action_chain[i]():
				i += 1
			drone.go_right()
		drone.go_down()

def harvest_plant_all(harvest_action, plant_action):
	iterate_grid((harvest_action, plant_action))
