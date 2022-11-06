
''' A place of danger for the ship, player decides whether to face danger '''

from game import location
from game.context import Context
from game.player import Player

import random

class Whirlpool (Context, location.Location):

	def __init__ (self, x, y, w):
		Context.__init__(self)
		location.Location.__init__(self, x, y, w)
		self.verbs['flee'] = self
		self.verbs['stay'] = self
		self.name = "whirlpool"
		self.ship = None
		self.symbol = "?"

	def enter (self, ship):
		self.symbol = "W"
		self.ship = ship
		self.go = False
		while (self.go == False):
			print ("you have found a whirlpool, what is your command?")
			Player.get_interaction ([self])


	def process_verb (self, verb, cmd_list, nouns):

		if (verb == "flee"):
			''' moved to a random location in the area '''
			destx = random.randrange (-2,3) + self.x
			desty = random.randrange (-2,3) + self.y
			if (destx < 0):
				destx = 0
			if (destx >= self.world.worldsize):
				destx = self.world.worldsize - 1
			if (desty < 0):
				desty = 0
			if (desty >= self.world.worldsize):
				desty = self.world.worldsize - 1

			new_loc = self.world.get_loc (destx, desty)
			self.ship.set_loc (new_loc)
			s = self.ship
			self.ship = None
			new_loc.enter (s)
			self.go = True

		elif (verb == "stay"):
			if (random.randint(1,2) == 1):
				Player.the_player.gameInProgress = False
				print ("the ship was destroyed in the whirlpool")
			else:
				print ("the ship is somehow holding together")
			self.go = True
	
	def start_day (self):
		if (self.ship != None):
			self.go = False
			while (self.go == False):
				print ("you are still at the whirlpool, what is your command?")
				Player.get_interaction ([self])
