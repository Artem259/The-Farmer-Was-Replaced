import eyes
import mapper
import state

def safe_harvest():
	if can_harvest():
		result = harvest()
		if result:
			state.after_action_hook()
		return result
	return False

def _plant_grass():
	return plant(Entities.Grass)

def _plant_bush():
	return plant(Entities.Bush)

def _plant_tree():
	return plant(Entities.Tree)

def _plant_carrot():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Carrot)

def safe_plant(entity):
	plant_action = mapper.entity_to_plant_action(entity)
	result = plant_action()
	if result:
		state.after_action_hook()
	return result
