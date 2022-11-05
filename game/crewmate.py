
import random


class CrewMate:

	possible_names = ['alice', 'bob', 'charlie', 'darren', 'eliza', 'francine', 'gale', 'hope']

	def __init__ (self):
		self.name = random.choice (CrewMate.possible_names)
		CrewMate.possible_names.remove (self.name)
		self.max_health = 100
		self.health = self.max_health
		self.sick = False

	def get_name (self):
		return self.name

	def get_health (self):
		return self.health

	def receive_medicine (self, num):
		if (num > 0):
			self.sick = False

	def inflict_damage (self, num):
		self.health = self.health - num

	def get_hunger (self):

		if (self.sick):
			return 3
		return 1

	def set_sickness (self, flag):
		self.sick = flag

	def start_day (self, ship):
		if (self.sick):
			ship.take_food (3)
			self.health = self.health - 1
			if (random.randint(1,10) == 1):
				self.sick = False
		else:
			ship.take_food (1)

	def print (self):
		if (self.sick):
			print ("   " + self.name + " Health: " + str(self.health) + " --Sick")
		else:
			print ("   " + self.name + " Health: " + str(self.health))