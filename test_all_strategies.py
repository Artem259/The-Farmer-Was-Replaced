import drone
import mapper
import state

clear()
drone.go_up(state.grid_size - 1)

entities = (
	Entities.Grass,
	Entities.Bush,
	Entities.Tree,
	Entities.Carrot,
)
iterations = 2

for entity in entities:
	for iter in range(1, iterations + 1):
		strategy = mapper.entity_to_strategy(entity)
		quick_print(strategy.__name__, iter, "/", iterations)
		strategy.run()
quick_print("Completed.")
