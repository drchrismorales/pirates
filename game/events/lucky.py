
from game import event
import random

class LuckyDay (event.Event):

    def __init__ (self):
        self.name = " crew member has a lucky day"

    def process (self, world):
        # choose a lucky crew member
        
        c = random.choice(world.get_ship().get_crew())
        msg = c.get_name() + " is having a lucky day"
        result = {}
        result["message"] = msg
        result["newevents"] = [ self ]
        return result
