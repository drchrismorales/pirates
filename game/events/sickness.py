
from game import event
import random
import game.config as config

class Sickness(event.Event):

    def __init__ (self):
        self.name = " a random crew member gets sick "

    def process (self, world):
        c = random.choice(config.the_player.get_pirates())
        c.set_sickness (True)
        result = {}
        result["message"] = c.get_name() + " has gotten sick"
        result["newevents"] = [ self, self ]
        return result