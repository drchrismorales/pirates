import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class EnchantedGuardian (event.Event):
    '''
    A combat encounter with a guardian of a distant past.
    When the event is drawn, creates a combat encounter with 2 to 3 drowned pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " ancient guardian"

    def process (self, world):
        '''Process the event. Populates a combat with monsters. The first Drowned may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}
        result["message"] = "the guardians are defeated!"
        monsters = []
        min = 2
        uplim = 4
        if random.randrange(2) == 0:
            min = 1
            uplim = 4
            monsters.append(combat.Guardian("Elder Guardian"))
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.Guardian("Guardian "+str(n)))
            n += 1
        announce ("You are attacked by a squad of Guardians!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result

