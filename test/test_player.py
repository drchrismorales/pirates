import unittest
from game import player

class Player_test (unittest.TestCase):

	def test_notdone_initialized (self):
		p = player.Player (None, None)
		self.assertEqual (True, p.notdone())