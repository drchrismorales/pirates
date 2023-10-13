
from game import event
import random
import game.config as config

class LuckyDay (event.Event):
    '''This event picks one pirate to have a lucky day, setting their "lucky" bool to True. By itself this has no effect, but a variety of things check lucky.'''
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
