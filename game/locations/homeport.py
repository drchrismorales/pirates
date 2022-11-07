
from game import location
from game.player import Player
from game.display import announce

class HomePort (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "destination"
        self.symbol = 'H'

    def enter (self, ship):
        Player.the_player.gameInProgress = False
        announce ("congratulations you've reached home and won")
