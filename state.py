import parameters
import tools

if parameters.MAX_GRID_SIZE == -1:
	grid_size = get_world_size()
else:
	grid_size = min(parameters.MAX_GRID_SIZE, get_world_size())

grid_entities = tools.generate_matrix(grid_size, Entities.Grass)

def after_action_hook():
	x = get_pos_x()
	y = get_pos_y()
	grid_entities[x][y] = get_entity_type()
