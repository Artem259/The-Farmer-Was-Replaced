import grass_strategy
import bush_strategy
import carrot_strategy
import tree_strategy
import polyculture_strategy
import pumpkin_strategy
import cactus_strategy
import sunflower_strategy

strategies = (
	grass_strategy,
	bush_strategy,
	carrot_strategy,
	tree_strategy,
	polyculture_strategy,
	pumpkin_strategy,
	cactus_strategy,
	sunflower_strategy,
)
iterations = 1

clear()
for strategy in strategies:
	for iter in range(1, iterations + 1):
		quick_print(strategy.__name__, iter, "/", iterations)
		strategy.run()
quick_print("Completed.")
