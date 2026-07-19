import mapper
import parameters
import state

cycles = 1

quick_print("--------------------")
quick_print("grid_size        =", state.grid_size)
quick_print("base_water_level =", state.base_water_level)
quick_print("min_water_level  =", state.min_water_level)
quick_print("--------------------")

targets = {}
for p in range(len(parameters.ITEMS)):
	config_tuple = parameters.ITEMS[p]
	item, quantity = config_tuple[0], config_tuple[1]
	if len(config_tuple) == 3:
		relative_quantity = config_tuple[2]
	else:
		relative_quantity = 0

	if quantity == -1:
		item_strategy = mapper.item_to_strategy(item)
		quantity = item_strategy.calc_target_quantity()

	if quantity != None and relative_quantity != 0:
		quantity = max(quantity, num_items(item) + relative_quantity)

	targets[item] = quantity
	quick_print(item, "=>", quantity)

set_world_size(state.grid_size)
clear()
cycle = cycles
while True:
	if cycle == cycles:
		strategy = None
		cycle = 0
		for p in range(len(parameters.ITEMS)):
			item = parameters.ITEMS[p][0]
			if len(parameters.ITEMS[p]) == 3:
				relative_quantity = True
			else:
				relative_quantity = False
			if quantity == -1:
				item_strategy = mapper.item_to_strategy(item)
				quantity = item_strategy.calc_target_quantity()
				if item not in cached_quantities or cached_quantities[item] != quantity:
					quick_print(item, "=>", quantity)
					cached_quantities[item] = quantity
			elif relative_quantity:
				quantity = num_items(item) + quantity
			if quantity == None or num_items(item) < quantity:
				if quantity == None:
					quantity = (10 ** 12) * num_items(item)
				strategy = mapper.item_to_strategy(item)
				break
		if strategy == None:
			quick_print("Target item not found!")
			break
		state.target_item = item
		state.target_quantity = quantity
		quick_print(strategy.__name__, "(", item, "=>", quantity, ")")

	start_time = get_time()
	strategy.run()
	cycle += 1
	run_seconds = get_time() - start_time
	run_minutes, run_seconds = run_seconds // 60, run_seconds % 60
	if run_minutes > 0:
		quick_print(cycle, "/", cycles, ",", run_minutes, "m", run_seconds, "s")
	else:
		quick_print(cycle, "/", cycles, ",", run_seconds, "s")
