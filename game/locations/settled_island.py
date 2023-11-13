from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items

class Settled_Island(location.Island):
    def __init__(self,x,y,w):
        super().__init__(x,y,w)
        self.name = "Settled Island"
        self.symbol = "I"
        self.visitable = True
        self.starting_location = Docks() #Insert Starting Location Here
        self.locations = {}
        self.locations["docks"] = self.starting_location
        self.locations["wharf"] = None #Add sublocation obj here
        self.locations["beach"] = None #Add sublocation obj here
        self.locations["woods"] = None #Add sublocation obj here
        self.locations["logging camp"] = None #Add sublocation obj here
        self.locations["town"] = None #Add sublocation obj here
        self.locations["tavern"] = None #Add sublocation obj here
        self.locations["casino"] = None #Add sublocation obj here
        self.locations["store"] = None #Add sublocation obj here

    def enter(self,ship):
        print("arrived at settled island")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Docks (location.SubLocation):
    def __init__(self,m):
        super().__init__(m):
        self.name="docks"
        self.verbs['north'] = self
        self.verbs['south']
        self.verbs['east']
        self.verbs['south']
        self.event_chance = 0

    def enter(self):
        announce()