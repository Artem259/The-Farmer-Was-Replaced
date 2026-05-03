import drone
import state

def iterate_grid(
	action_chain, 
	start_x=0, 
	end_x=state.grid_size - 1, 
	start_y=state.grid_size - 1, 
	end_y=0
):
	n = len(action_chain)
	for y in range(start_y, end_y - 1, -1):
		for x in range(start_x, end_x + 1):
			drone.goto(x, y)
			i = 0
			while i < n and action_chain[i]():
				i += 1

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
