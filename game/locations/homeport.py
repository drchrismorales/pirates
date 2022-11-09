
from game import location
import game.config as config
from game.display import announce

class HomePort (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "destination"
        self.symbol = 'H'

    def enter (self, ship):
        config.the_player.gameInProgress = False
        announce ("congratulations you've reached home and won")
