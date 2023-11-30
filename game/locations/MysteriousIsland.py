
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
        self.starting_location = (Beach(self))
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["cult_room"] = Nave(self)
        self.locations['puzzle_room'] = Vestibule(self)
        self.locations['sanctuary'] = Sanctuary(self)


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
        self.verbs['go'] = self
        self.nouns['north'] = self
        self.nouns['west'] = self
        self.nouns['ship'] = self
        self.verbs['exit'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())

    def enter (self):
        announce ("You are on the beach. Your ship is anchored to the dock.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "go"):
            print(nouns)
            if 'ship' in nouns or 'exit' in nouns:
                config.the_player.next_loc = config.the_player.ship
                config.the_player.visiting = False
            elif 'west' in nouns:
                config.the_player.next_loc = self.main_location.locations["ruins"]
            elif 'cliff' in nouns: 
                config.the_player.next_loc = self.main_location.locations["cliff"]
            else:
                print(nouns)

        else:
            announce("Command not recognized.")


class Cliff (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "cliff"
        self.verbs['go'] = self
        self.verbs['take'] = self
        self.nouns['south'] = self
        self.nouns['ladder'] = self


    def enter (self):
        description = "You ascend the cliff to the north."
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        print(nouns)
        print(cmd_list)
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == 'ladder':
            announce('You don\'t see a ladder.')


class Ruins (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "ruins"
        self.verbs['go'] = self
        self.nouns['ruins'] = self
        self.nouns['east'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "An abandoned town presides here."

        #TODO: add check for user coming from the dungeon for the first time.

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
        self.name = "vestibule"
        self.verbs['go'] = self
        self.nouns['left'] = self
        self.nouns['right'] = self
        self.nouns['crypt'] = self
        self.nouns['chamber'] = self
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
    def __init__ (self, m):
        super().__init__(m)
        self.name = "crypt"
        self.verbs['go'] = self
        self.verbs['back'] = self
        self.verbs['vestibule'] = self

    def enter (self):
        description = "TODO"
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


class Vestibule(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "vestibule"
        self.verbs['go'] = self
        self.nouns['left'] = self
        self.nouns['right'] = self
        self.nouns['chamber'] = self

    def enter (self):
        description = "TODO"
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


class Nave(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "nave"
        self.verbs['go'] = self
        self.nouns['vestibule'] = self
        self.nouns['back'] = self
        self.nouns['vestibule'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes

    def enter (self):
        description = "TODO"
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


class Sanctuary(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "sanctuary"
        self.verbs['go'] = self
        self.nouns['up'] = self
        self.nouns['ladder'] = self
        self.nouns['back'] = self
        self.nouns['nave'] = self


    def enter (self):
        description = "TODO"
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