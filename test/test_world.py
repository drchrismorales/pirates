
import unittest
from game import world

class World_test (unittest.TestCase):

	def test_day_initialized (self):
		w = world.World(None)
		self.assertEqual (0, w.get_day())