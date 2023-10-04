
from game import event
import random
import game.config as config

class Sickness(event.Event):

    def __init__ (self):
        self.name = " a random crew member gets sick "

    def process (self, world):
        c = random.choice(config.the_player.get_pirates())
        result = {}
        if (c.sick == True):
            c.set_sickness (True)
            if (c.isLucky() == True):
                damage = 1
                deathcause = "died of their illness"
            else:
                damage = 10
                deathcause = "died of their worsening illness"
            died = c.inflict_damage (damage, deathcause)
            if(died == True):
                result["message"] = c.get_name() + " took a turn for the worse and has died of their illness"
                result["newevents"] = [ self, self, self ]
            else:
                result["message"] = c.get_name() + " has taken a turn for the worse"
                result["newevents"] = [ self, self ]
        elif (c.isLucky() == False):
            c.set_sickness (True)
            result["message"] = c.get_name() + " has gotten sick"
            result["newevents"] = [ self, self ]
        else:
            result["message"] = c.get_name() + " felt a bit sick"
            result["newevents"] = [ self ]
        return result
