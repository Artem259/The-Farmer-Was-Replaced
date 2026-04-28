import mapper

def safe_harvest():
	if can_harvest():
		return harvest()
	return get_entity_type() == None

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

def _plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Pumpkin)

def _plant_cactus():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Cactus)

def safe_plant(entity):
	plant_action = mapper.entity_to_plant_action(entity)
	return plant_action()
