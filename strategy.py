import drone
import state

def iterate_grid(
	action_chain, 
	start_x=0, 
	end_x=state.grid_size - 1, 
	start_y=0, 
	end_y=state.grid_size - 1
):
	n = len(action_chain)
	for y in range(end_y, start_y - 1, -1):
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

def run_multiworker(run_function, args_list, this_index=None):
	if this_index != None:
		other_args = []
		for index in range(len(args_list)):
			if index == this_index:
				this_args = args_list[index]
			else:
				other_args.append(args_list[index])
		workers = spawn_workers(run_function, other_args)
		this_result = run_function(this_args)
	else:
		workers = spawn_workers(run_function, args_list)
	results = join_workers(workers)
	if this_index != None:
		results.insert(this_index, this_result)
	return results
