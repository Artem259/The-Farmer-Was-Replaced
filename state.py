import parameters

if parameters.MAX_GRID_SIZE == -1:
	grid_size = get_world_size()
else:
	grid_size = min(parameters.MAX_GRID_SIZE, get_world_size())

# (s ** 2) * 0.01 * x = 0.25 * 0.1 * (2 ** (l - 1))
base_water_level = min(
	(2.5 * (2 ** (num_unlocked(Unlocks.Watering) - 1))) / (grid_size ** 2),
	1.0
)

min_water_level = base_water_level - (0.25 / 2)
