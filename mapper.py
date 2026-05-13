import ops

def item_to_strategy(item):
	if item == Items.Hay:
		import grass_strategy
		return grass_strategy
	if item == Items.Wood:
		import tree_strategy
		return tree_strategy
	if item == Items.Carrot:
		import polyculture_strategy
		return polyculture_strategy
	if item == Items.Pumpkin:
		import pumpkin_strategy
		return pumpkin_strategy
	if item == Items.Cactus:
		import cactus_strategy
		return cactus_strategy
	if item == Items.Power:
		import sunflower_strategy
		return sunflower_strategy
	if item == Items.Weird_Substance:
		import weird_subs_strategy
		return weird_subs_strategy
	if item == Items.Gold:
		import maze_strategy
		return maze_strategy
	if item == Items.Bone:
		import dinosaur_strategy
		return dinosaur_strategy
	print("item_to_strategy", 0 / 0)

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
