
from game import event
import random

class Sickness(event.Event):

    def __init__ (self):
        self.name = " a random crew member gets sick "

    def process (self, world):
        c = random.choice(world.get_ship().get_crew())
        c.set_sickness (True)
        result = {}
        result["message"] = c.get_name() + " has gotten sick"
        result["newevents"] = [ self, self ]
        return result