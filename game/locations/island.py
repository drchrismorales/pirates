
from game import location
from game import config
from game.display import announce

class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Beach_with_ship(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["trees"] = Trees(self)

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter (self, ship):
        announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        elif (verb == "east" or verb == "west"):
            announce ("You walk all the way around the island on the beach. It's not very interesting.")


class Trees (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter (self, ship):
        announce ("You walk into the small forest on the island. Nothing around here looks very edible.")
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]


