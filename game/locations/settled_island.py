from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items

class Flags:
    knowledge_flag = False
    map_flag = False
    supply_flag = False
    quest_flag = False
class Settled_Island(location.Location):
    def __init__(self,x,y,w):
        super().__init__(x,y,w)
        self.name = "Settled Island"
        self.symbol = "\u0413"
        self.visitable = True
        self.starting_location = Docks(self) #Insert Starting Location Here
        self.locations = {}
        self.locations["docks"] = self.starting_location
        self.locations["wharf"] = Wharf(self)
        self.locations["beach"] = None #Add sublocation obj here
        self.locations["jungle"] = None #Add sublocation obj here
        self.locations["inland_settlement"] = None #Add sublocation obj here
        #might make a seperate import for these locations
        self.locations["town"] = Town(self)
        self.locations["tavern"] = None #Add sublocation obj here
        self.locations["casino"] = None #Add sublocation obj here
        self.locations["store"] = None #Add sublocation obj here

    def enter(self,ship):
        print("You Arrive at the settled island")

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
        announce("You dock your ship at the docks")
    
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
        self.verbs['north'] = self
        self.verbs['south'] = self
        #no east or west
        self.verbs['talk'] = self
        self.verbs['repair'] = self
        
    def enter(self):
        announce("You walk up to a small wharf \n On the wharf is a stranded merchant and a shipwright")
    
    def process_verb (self,verb,cmd_list,nouns):
        if verb == "south":
            announce("You wander back to the docks.")
            config.the_player.next_loc = self.main_location.locations["docks"]
        elif verb == "north":
            announce("You walk north of the dock into town")
            config.the_player.next_loc = self.main_location.locations["town"]
        elif verb == "talk":
            if len(cmd_list) == 1:
                announce("You try to talk to nobody?")
            elif cmd_list[1] == "merchant":
                announce("You try to talk to the merchant")
            elif cmd_list[1] == "shipwright":
                announce("You try to talk to the shipwright")
            else:
                announce("That person isn't here")
        elif verb == "repair":
            announce("You ask the shipwright to fix your ship")
            if not Flags.quest_flag:
                announce("Shipwright: I don't have the supplies to fix your ship")
            else:
                pass #not implemented yet

class Town(location.SubLocation):
    def __init__(self,m):
        super().__init__(m)
        self.verbs['south'] = self
        self.verbs['casino'] = self
        self.verbs['store'] = self
        self.verbs['tavern'] = self
        #non-go verbs
        self.verbs['talk'] = self

    def process_verb(self, verb, cmd_list, nouns):
        if verb == 'south':
            announce("you return to the wharf")
            config.the_player.next_loc = self.main_location.locations['wharf']
        elif verb == 'casino':
            announce("you try to enter the casino")
        elif verb == 'store':
            announce("you try to enter the store")
        elif verb == 'tavern':
            announce("You try to enter the tavern")
        elif verb == "talk":
            announce("There is nobody arround")