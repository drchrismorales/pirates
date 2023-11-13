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
        self.locations["wharf"] = Wharf() #Add sublocation obj here
        self.locations["beach"] = None #Add sublocation obj here
        self.locations["woods"] = None #Add sublocation obj here
        self.locations["logging camp"] = None #Add sublocation obj here
        #might make a seperate import for these locations
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
        super().__init__(m)
        self.name="docks"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['south'] = self
        self.event_chance = 0

    def enter(self):
        announce("thing that announces entry")
    
    def process_verb (self,verb,cmd_list, nouns):
        if verb == "south":
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif verb == "north":
            config.the_player.next_loc = self.main_location.locations["wharf"]
        elif (verb == "east") or (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["beach"]

class Wharf (location.SubLocation):
    def __init__(self,m):
        super().__init__(m)
        self.name = "wharf"