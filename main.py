import mapper
import parameters
import state

quick_print("--------------------")
quick_print("grid_size =", state.grid_size)
quick_print("--------------------")

cycles = 1

clear()
cycle = cycles
while True:
	if cycle == cycles:
		cycle = 0
		entity = None
		for p in range(len(parameters.ITEMS)):
			item, quantity = parameters.ITEMS[p]
			if quantity == None or num_items(item) < quantity:
				entity = mapper.item_to_entity(item)
				break
		strategy = mapper.entity_to_strategy(entity)
		quick_print(strategy.__name__)

	strategy.run()
	cycle += 1
