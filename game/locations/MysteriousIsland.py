
from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items

class MysteriousIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = (self.Beach)
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["cult_room"] = Cult_Room(self)
        self.locations['puzzle_room'] = Puzzle_Room(self)
        self.locations['treasure_stash'] = Treasure_Stash(self)


    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class Beach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['west'] = self
        self.verbs['ship'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())

    def enter (self):
        announce ("arrive at the beach. Your ship is at anchor in a small bay to the east.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "ship"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["cliff"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["ruins"]


class Cliff (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['go'] = self
        self.verbs['take'] = self
        self.nouns['south'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes

    def enter (self):
        description = "You ascend the cliff to the north. "
        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        print(nouns)
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")


class Ruins (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['go'] = self
        self.verbs['take'] = self
        self.nouns['south'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into the small forest on the island."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        print(nouns)
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")


class Temple_Entrance (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['go'] = self
        self.verbs['take'] = self
        self.nouns['south'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes

    def enter (self):
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        print(nouns)
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")


class Crypt(location.SubLocation):
    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = (self.Beach)
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["cult_room"] = Cult_Room(self)
        self.locations['puzzle_room'] = Puzzle_Room(self)
        self.locations['treasure_stash'] = Treasure_Stash(self)


    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = (self.Beach)
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["cult_room"] = Cult_Room(self)
        self.locations['puzzle_room'] = Puzzle_Room(self)
        self.locations['treasure_stash'] = Treasure_Stash(self)


    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class Cult_Room(location.SubLocation):
    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = (self.Beach)
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["cult_room"] = Cult_Room(self)
        self.locations['puzzle_room'] = Puzzle_Room(self)
        self.locations['treasure_stash'] = Treasure_Stash(self)


    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class Puzzle_Room(location.SubLocation):
    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = (self.Beach)
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["cult_room"] = Cult_Room(self)
        self.locations['puzzle_room'] = Puzzle_Room(self)
        self.locations['treasure_stash'] = Treasure_Stash(self)


    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class Treasure_Stash(location.SubLocation):
    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = (self.Beach)
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["cult_room"] = Cult_Room(self)
        self.locations['puzzle_room'] = Puzzle_Room(self)
        self.locations['treasure_stash'] = Treasure_Stash(self)


    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()