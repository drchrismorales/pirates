from game import event

class Nothing (event.Event):

	def __init__ (self):
		self.name = " nothing happened"

	def process (self, world):
		result = {}
		result["message"] = "nothing happened"
		result["newevents"] = [ self ]
		return result