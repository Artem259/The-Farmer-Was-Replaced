import mapper
import parameters
import state

quick_print("--------------------")
quick_print("grid_size        =", state.grid_size)
quick_print("base_water_level =", state.base_water_level)
quick_print("min_water_level  =", state.min_water_level)
quick_print("--------------------")

cycles = 1

set_world_size(state.grid_size)
clear()
cached_quantities = {}
cycle = cycles
while True:
	if cycle == cycles:
		strategy = None
		cycle = 0
		for p in range(len(parameters.ITEMS)):
			item, quantity = parameters.ITEMS[p]
			if quantity == -1:
				item_strategy = mapper.item_to_strategy(item)
				quantity = item_strategy.calc_target_quantity()
				if item not in cached_quantities or cached_quantities[item] != quantity:
					quick_print(item, "=>", quantity)
					cached_quantities[item] = quantity
			if quantity == None or num_items(item) < quantity:
				strategy = mapper.item_to_strategy(item)
				break
		if strategy == None:
			quick_print("Target item not found!")
			break
		quick_print(strategy.__name__, "...")

	start_time = get_time()
	strategy.run()
	cycle += 1
	run_seconds = get_time() - start_time
	run_minutes, run_seconds = run_seconds // 60, run_seconds % 60
	if run_minutes > 0:
		quick_print(cycle, "/", cycles, ",", run_minutes, "m", run_seconds, "s")
	else:
		quick_print(cycle, "/", cycles, ",", run_seconds, "s")
