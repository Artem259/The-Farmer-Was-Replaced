import parameters

if parameters.MAX_GRID_SIZE == -1:
	grid_size = get_world_size()
else:
	grid_size = min(parameters.MAX_GRID_SIZE, get_world_size())
