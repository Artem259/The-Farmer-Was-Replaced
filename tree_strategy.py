import eyes
import ops
import strategy

placeholder = Entities.Grass

def run():
	def plant_action():
		adjacent_entities = eyes.drone_adjacent_entities()
		if Entities.Tree not in adjacent_entities:
			ops.safe_plant(Entities.Tree)
		else:
			ops.safe_plant(placeholder)

	strategy.harvest_plant_all(
		ops.safe_harvest, 
		plant_action
	)
