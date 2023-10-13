from game import event
import random
from game.combat import Combat
from game.combat import Macaque
from game.display import announce
import game.config as config

class ManEatingMonkeys (event.Event):
    '''
    A combat encounter with a troop of man eating monkies.
    When the event is drawn, creates a combat encounter with 4 to 8 monkies, kicks control over to the combat code to resolve the fight.
    The monkies are "edible", which is modeled by increasing the ship's food by 3 per monkey appearing and adding an apropriate message to the result.
        Since food is good, the event only has a 50% chance to add itself to the result.
    '''

    def __init__ (self):
        self.name = " monkey attack"

    def process (self, world):
        result = {}
        result["message"] = "the macaques are defeated! ...Those look pretty tasty!"
        monsters = []
        n_appearing = random.randrange(4,8)
        n = 1
        while n <= n_appearing:
            monsters.append(Macaque("Man-eating Macaque "+str(n)))
            n += 1
        announce ("The crew is attacked by a troop of man-eating macaques!")
        Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += n_appearing*3

        return result
