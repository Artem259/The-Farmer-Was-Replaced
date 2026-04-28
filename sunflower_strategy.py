import drone
import ops
import strategy

min_petals = 7
max_petals = 15

def run():
	def harvest_action():
		while not ops.safe_harvest():
			pass
		return True

	buckets = []
	for _ in range(max_petals + 1):
		buckets.append([])

	def plant_action():
		ops.safe_plant(Entities.Sunflower)
		petals = measure()
		buckets[petals].append((get_pos_x(), get_pos_y()))

	strategy.iterate_grid((harvest_action, plant_action))
	
	for petals in range(max_petals, min_petals - 1, -1):
		queue = buckets[petals]
		for x, y in queue:
			drone.goto(x, y)
			harvest_action()
