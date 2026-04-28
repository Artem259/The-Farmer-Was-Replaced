import ops
import strategy

placeholder = Entities.Grass

def run():
	def plant_action():
		x = get_pos_x()
		y = get_pos_y()
		if (x + y) % 2 == 0:
			ops.safe_plant(Entities.Tree)
		else:
			ops.safe_plant(placeholder)

	strategy.harvest_plant_all(
		ops.safe_harvest, 
		plant_action
	)
