from game import event
import random
from game.combat import Combat
from game.combat import Drowned
from game.display import announce

class DrownedPirates (event.Event):

    def __init__ (self):
        self.name = " drowed pirate attack"

    def process (self, world):
        result = {}
        result["message"] = "the drowned pirates are defeated!"
        monsters = []
        if random.randrange(2) == 0:
            monsters.append(Drowned("Pirate captain"))
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(1,5)
        n = 1
        while n <= n_appearing:
            monsters.append(Drowned("Drowned pirate "+str(n)))
            n += 1
        announce ("The ship is attacked by a crew of drowned pirates!")
        Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
