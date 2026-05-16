import mapper
import parameters
import state

def safe_harvest(use_fertilizer=True):
	use_fertilizer = (use_fertilizer and parameters.USE_FERTILIZER)
	if get_entity_type() == None:
		return True
	if use_fertilizer:
		while (
			num_items(Items.Fertilizer) > 10 and 
			not can_harvest()
		):
			if not use_item(Items.Fertilizer):
				break
	if can_harvest():
		return harvest()
	return False

def waitfor_safe_harvest():
	while not safe_harvest():
		pass
	return True

def clean_harvest():
	waitfor_safe_harvest()
	if get_ground_type() != Grounds.Soil:
		till()

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

def _plant_sunflower():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Sunflower)

def safe_plant(entity, use_water=True):
	use_water = (use_water and parameters.USE_WATER)
	plant_action = mapper.entity_to_plant_action(entity)
	if not plant_action():
		return False
	if use_water:
		while (
			num_items(Items.Water) > 100 and 
			get_water() < state.min_water_level
		):
			if not use_item(Items.Water):
				break
	return True
