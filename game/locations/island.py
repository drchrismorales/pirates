
from game import location

class Island (location.Location):

	def __init__ (self, x, y, w):
		super().__init__(x, y, w)
		self.name = "island"
		self.symbol = 'I'

	def enter (self, ship):
		print ("arrived at an island")