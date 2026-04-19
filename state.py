import parameters

if parameters.MAX_GRID_SIZE == -1:
	grid_size = get_world_size()
else:
	# TODO min(parameters.MAX_GRID_SIZE, get_world_size())
	grid_size = parameters.MAX_GRID_SIZE

allow_teleport = False
if grid_size == get_world_size():
	allow_teleport = True

grid_entities = []
for _ in range(grid_size):
	row = []
	for _ in range(grid_size):
		row.append(Entities.Grass)
	grid_entities.append(row)

def after_action_hook():
	x = get_pos_x()
	y = get_pos_y()
	grid_entities[x][y] = get_entity_type()
