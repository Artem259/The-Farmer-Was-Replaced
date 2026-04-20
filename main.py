import drone
import mapper
import state

quick_print("--------------------")
quick_print("grid_size =", state.grid_size)
quick_print("--------------------")

items_quantity = [
	(Items.Hay, 10000),
	(Items.Wood, 10000),
	(Items.Carrot, 10000),
	(Items.Pumpkin, None),
]
priorities = [1, 0, 2, 3]
cycles = 1

cycle = cycles
while True:
	if cycle == cycles:
		cycle = 0
		entity = None
		for p in priorities:
			item = items_quantity[p][0]
			quantity = items_quantity[p][1]
			if quantity == None or num_items(item) < quantity:
				entity = mapper.item_to_entity(item)
				break
		strategy = mapper.entity_to_strategy(entity)
		quick_print(strategy.__name__)

	drone.goto(0, state.grid_size - 1)
	strategy.run()
	cycle += 1
