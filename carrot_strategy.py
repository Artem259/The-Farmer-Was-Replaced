import ops
import strategy

def run():
	def plant_action():
		ops.safe_plant(Entities.Carrot)
	
	strategy.harvest_plant_all(
		ops.safe_harvest, 
		plant_action
	)
