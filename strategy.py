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

def spawn_workers(run_function, args_list):
	workers = []
	for args in args_list:
		worker = spawn_drone(run_function, args)
		if worker == None:
			print("spwan_workers", 0 / 0)
		workers.append(worker)
	return workers

def join_workers(workers):
	results = []
	for worker in workers:
		results.append(wait_for(worker))
	return results

def run_multiworker(run_function, args_list, use_this):
	if use_this:
		workers = spawn_workers(run_function, args_list[:-1])
		this_result = run_function(args_list[-1])
	else:
		workers = spawn_workers(run_function, args_list)
	results = join_workers(workers)
	if use_this:
		results.append(this_result)
	return results
