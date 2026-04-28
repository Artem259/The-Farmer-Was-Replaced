import ops

def item_to_entity(item):
	if item == Items.Hay:
		return Entities.Grass
	if item == Items.Wood:
		return Entities.Tree
	if item == Items.Carrot:
		return Entities.Carrot
	if item == Items.Pumpkin:
		return Entities.Pumpkin
	if item == Items.Cactus:
		return Entities.Cactus
	if item == Items.Power:
		return Entities.Sunflower
	print("item_to_entity", 0 / 0)

def entity_to_strategy(entity):
	if entity == Entities.Grass:
		import grass_strategy
		return grass_strategy
	if entity == Entities.Bush:
		import bush_strategy
		return bush_strategy
	if entity == Entities.Tree:
		import tree_strategy
		return tree_strategy
	if entity == Entities.Carrot:
		import polyculture_strategy
		return polyculture_strategy
	if entity == Entities.Pumpkin:
		import pumpkin_strategy
		return pumpkin_strategy
	if entity == Entities.Cactus:
		import cactus_strategy
		return cactus_strategy
	if entity == Entities.Sunflower:
		import sunflower_strategy
		return sunflower_strategy
	print("entity_to_strategy", 0 / 0)

def entity_to_plant_action(entity):
	if entity == Entities.Grass:
		return ops._plant_grass
	if entity == Entities.Bush:
		return ops._plant_bush
	if entity == Entities.Tree:
		return ops._plant_tree
	if entity == Entities.Carrot:
		return ops._plant_carrot
	if entity == Entities.Pumpkin:
		return ops._plant_pumpkin
	if entity == Entities.Cactus:
		return ops._plant_cactus
	if entity == Entities.Sunflower:
		return ops._plant_sunflower
	print("entity_to_plant_action", 0 / 0)
