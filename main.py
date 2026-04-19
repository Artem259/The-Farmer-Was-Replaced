import drone
import mapper
import ops
import state

quick_print("--------------------")
quick_print("grid_size =", state.grid_size)
quick_print("allow_teleport =", state.allow_teleport)
quick_print("--------------------")

items_quantity = [
	(Items.Hay, 2000),
	(Items.Wood, 2000),
	(Items.Carrot, None),
]
priorities = [1, 0, 2]
cycles = 1

clear()
drone.go_up(state.grid_size - 1)

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

	strategy.run()
	cycle += 1
