import drone
import mapper
import state

entities = (
	Entities.Grass,
	Entities.Bush,
	Entities.Tree,
	Entities.Carrot,
)
iterations = 2

clear()
for entity in entities:
	for iter in range(1, iterations + 1):
		strategy = mapper.entity_to_strategy(entity)
		drone.goto(0, state.grid_size - 1)
		quick_print(strategy.__name__, iter, "/", iterations)
		strategy.run()
quick_print("Completed.")
