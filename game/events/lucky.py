
from game import event
import random
import game.config as config

class LuckyDay (event.Event):
    #every event has event.Event parent class...

    def __init__ (self):
        self.name = " crew member has a lucky day"

    def process (self, world):
        # choose a lucky crew member
        
        c = random.choice(config.the_player.get_pirates())
        msg = c.get_name() + " is having a lucky day"
        c.lucky = True
        result = {}
        result["message"] = msg
        result["newevents"] = [ self ]
        return result
