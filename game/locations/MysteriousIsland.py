from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items


import game.combat as combat
import game.event as event
import random

class MysteriousIsland(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = "M"
        self.visitable = True
        self.starting_location = Beach(self)
        self.locations = {}

        # Surface (starting point)
        self.locations["beach"] = self.starting_location
        self.locations["cliff"] = Cliff(self)
        self.locations["ruins"] = Ruins(self)

        # Inside temple
        self.locations["temple_entrance"] = Temple_Entrance(self)
        self.locations["crypt"] = Crypt(self)
        self.locations["nave"] = Nave(self)
        self.locations["vestibule"] = Vestibule(self)
        self.locations["sanctuary"] = Sanctuary(self)

    def visit(self):
        print("You arrive at the island.")
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class Beach(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs["go"] = self  # Override player go method to add more directions
        # self.event_chance = 50
        # self.events.append (seagull.Seagull())

    def enter(self):
        description = (
            "You are on the island's beach. Your ship is anchored here."
        )
        description += "\nTo your north is a hill. To your west is a forest."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            config.the_player.go = True
            if len(cmd_list) > 1:
                if cmd_list[1] == "north":
                    config.the_player.next_loc = self.main_location.locations["cliff"]
                if cmd_list[1] == "west":
                    config.the_player.next_loc = self.main_location.locations["ruins"]
                elif cmd_list[1] == "south" or cmd_list[1] == "east":
                    announce("Nothing but open ocean.")
                elif (
                    cmd_list[1] == "ship"
                    or cmd_list[1] == "exit"
                    or cmd_list[1] == "dock"
                ):
                    announce("You return to your ship.")
                    config.the_player.next_loc = config.the_player.ship
                    config.the_player.visiting = False


class Cliff(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cliff"
        self.verbs["go"] = self
        self.verbs["take"] = self
        self.items = {items.Cutlass, items.BelayingPin}


    def enter(self):
        description = "You ascend the hill to the plateau.\n"
        # description = "Climbing the ladder, "
        description += (
            "Many buildings seem worse for wear, many if not all abandoned.\n"
        )
        if None not in self.items:
            description += "You see weapons in one of the buildings.\n"
            for item in self.items:
                description += f'A {item.name}\n'

        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            if len(cmd_list) > 1:
                config.the_player.go = True
                if cmd_list[1] == "south":
                    config.the_player.next_loc = self.main_location.locations["beach"]
                elif cmd_list[1] == "ladder":
                    config.the_player.next_loc = self.main_location.locations[
                        "sanctuary"
                    ]
                elif (
                    cmd_list[1] == "west"
                    or cmd_list[1] == "east"
                    or cmd_list[1] == "north"
                ):
                    announce("Nothing but open ocean.")
        if verb == "take":
            at_least_one = False
            for key in self.items:
                if self.items[key] != None and (cmd_list[1] == self.items[key].name or cmd_list[1] == "all"):
                        announce (f"You take the {self.items[key].name}.")
                        config.the_player.add_to_inventory([self.items[key]])
                        config.the_player.go = True
                        at_least_one = True
            if not at_least_one:
                announce("Not a valid item name.")


class Ruins(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "ruins"
        self.verbs["go"] = self

    def enter(self):
        # The description has a base description, followed by variable components.
        description = "You and your remaining team make their way through the dense foliage. The sunlight beams brightly through a clearing ahead.\n"
        description += "You see ruins of a temple. The entrance looks unstable.\n"

        # TODO: Add makeshift weapons

        # TODO: add check for user coming from the dungeon for the first time.

        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            if len(cmd_list) > 1:
                config.the_player.go = True
                if cmd_list[1] == "east":
                    config.the_player.next_loc = self.main_location.locations["beach"]
                elif cmd_list[1] == "temple" or cmd_list[1] == "ruins":
                    config.the_player.next_loc = self.main_location.locations[
                        "temple_entrance"
                    ]
                elif cmd_list[1] == "south" or cmd_list[1] == "west":
                    announce(
                        "The foliage in that direction is too thick to cut through."
                    )

        else:
            announce("Invalid command.")


class Temple_Entrance(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "entrance"
        self.verbs["go"] = self
        self.entered_before = False

    def enter(self):
        if not self.entered_before:
            description = "You and your crewmates enter the structure. Suddenly, the entrance collapses."
            # TODO: Add a specific pirate name at random. Maybe make it a recurring joke.
            description += (
                f'\nOne of the pirates groans. "Not this again," they mutter.'
            )
        else:
            description = "You are in the central chamber."

        description += "\nThough the room is dim, you can make out doorways to your left and right."

        announce(description)
        self.entered_before = True

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            config.the_player.go = True
            if len(cmd_list) > 1:
                if cmd_list[1] == "crypt" or cmd_list[1] == "left":
                    config.the_player.next_loc = self.main_location.locations["crypt"]
                elif cmd_list[1] == "vestibule" or cmd_list[1] == "right":
                    config.the_player.next_loc = self.main_location.locations[
                        "vestibule"
                    ]

        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = (
                    False  # Track if you pick up an item, print message if not.
                )
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce("You take the " + item.name + " from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce(
                        "You pick up the "
                        + item.name
                        + " out of the pile of clothes. ...It looks like someone was eaten here."
                    )
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce("You don't see one of those around.")


class Crypt(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "crypt"
        self.verbs["go"] = self
        self.verbs["look"] = self
        self.verbs["hint"] = self
        self.verbs["read"] = self
        self.saw_book = False

    def enter(self):
        description = "You walk down a spiral staircase. At the bottom you find a long hallway with tombs on either side. Definitely a crypt."
        description += "\nOn the far wall of the hallway is a bookcase."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            config.the_player.go = True
            if len(cmd_list) > 1:
                if cmd_list[1] == "back" or cmd_list[1] == "entrance":
                    config.the_player.next_loc = self.main_location.locations[
                        "temple_entrance"
                    ]

        if verb == "look":
            if len(cmd_list) > 1 and "book" in cmd_list[1]:
                description = "You see a single book on the bookcase. The cover has a cryptic image scribbled into the corner:\n\n"
                description += "▒▒▒▒▒▒▒▒▒▒▒▒\n"
                description += "▒ ┌─o  ┌─┐ ▒\n"
                description += "▒ │    │ │ ▒\n"
                description += "▒ └────┘ │ ▒\n"
                description += "▒  ──────┘ ▒\n"
                description += "▒▒▒▒▒▒▒▒▒▒▒▒\n"
                announce(description)
                self.saw_book = True
        if verb == "hint":
            if not self.saw_book:
                announce("Try looking at the bookcase.")
            else:
                announce("This symbol might have some meaning in another room.")


class Vestibule(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "vestibule"
        self.verbs["go"] = self
        self.door_open = False

    def enter(self):
        description = "You walk into the vestibule. On the far side of the room there is a sealed door."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            if len(cmd_list) > 1:
                config.the_player.go = True
                if cmd_list[1] == "entrance" or cmd_list[1] == "back":
                    config.the_player.next_loc = self.main_location.locations[
                        "entrance"
                    ]
                if cmd_list[1] == "door" or cmd_list[1] == "nave":
                    if self.door_open:
                        config.the_player.next_loc = self.main_location.locations[
                            "nave"
                        ]
                    else:
                        announce(
                            "The door is locked. There must be some way to open it."
                        )

        elif verb == "look":
            description = "On further inspection, you notice a row of buttons laid out beside it. The 4 buttons are labeled U, D, L, and R."
            description += "\nBelow the panel is a drawing of a fox... reading a book? They seem perplexed. Weird runes are written below. You cannot read it."

        elif verb == "solve":
            if len(cmd_list) > 1:
                if cmd_list[1].lower() == "ldrurdl":
                    # Open the door
                    self.door_open = True
                    # Announce that it opened
                    announce("The door has been opened.")


class Nave(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "nave"
        self.verbs["go"] = self
        self.events.append(drowned_pirates.DrownedPirates())
        self.event_chance = 100

    def enter(self):
        description = (
            "You walk into the central nave. The room is in disrepair."
            " Large cracks have formed on the walls,"
            "\nand the ocean can be heard through shattered windows."
            " You notice an entryway behind the altar."
        )
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            if len(cmd_list) > 1:
                config.the_player.go = True
                if cmd_list[1] == "back" or cmd_list[1] == "Vestibule":
                    config.the_player.next_loc = self.main_location.locations[
                        "vestibule"
                    ]
                elif "sanctum" in cmd_list or "entryway" in cmd_list:
                    config.the_player.next_loc = self.main_location.locations["sanctum"]


class Sanctuary(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "sanctuary"
        self.verbs["go"] = self
        self.verbs["take"] = self
        self.ladder_unlocked = False
        self.food_left = True

    def enter(self):
        description = "You've found the inner sanctuary. There is a ladder leading out of this area."
        announce(description)
        self.ladder_unlocked = True

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            if len(cmd_list) > 1:
                config.the_player.go = True
                if cmd_list[1] == "ladder" or cmd_list[1] == "up":
                    config.the_player.next_loc = self.main_location.locations["cliff"]
                    self.main_location.locations["cliff"].setUnlocked()
                elif cmd_list[1] == "nave" or cmd_list[1] == "back":
                    config.the_player.next_loc = self.main_location.locations["nave"]
        if verb == "take":
            #Items to take:
            if 'food' in cmd_list:
                if self.food_left:
                    config.the_player.ship.food += 15
                    self.food_left = False

            at_least_one = False
            for key in self.items:
                if self.items[key] != None and (cmd_list[1] == self.items[key].name or cmd_list[1] == "all"):
                        announce (f"You take the {self.items[key].name}.")
                        config.the_player.add_to_inventory([self.items[key]])
                        config.the_player.go = True
                        at_least_one = True
            if not at_least_one:
                announce("Not a valid item name.")



            # cutlass



class Cultist(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["swing"] = ["swings",random.randrange(35,51), (5,10)]
        attacks["cast"] = ["casts an incantation",random.randrange(10,30), (20,30)]
        attacks["throw"] = ["throws a piece of rubble",random.randrange(10,20), (30,40)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))

class Cultists (event.Event):
    '''
    A combat encounter with a group of cultists. Based on drowned pirate code.
    When the event is drawn, creates a combat encounter with 2 to 8 cultists. kicks control over to the combat code to resolve the fight,
    then adds itself and a simple success message to the result.
    '''

    def __init__ (self):
        self.name = " cultists"

    def process (self, world):
        '''Process the event. The first Cultist becomes a cult leader, buffing its speed and health.'''
        result = {}
        result["message"] = "The cultists are defeated!"
        monsters = []
        min = 1
        uplim = 7
        monsters.append(Cultist("Cult Leader"))
        monsters[0].speed = 1.2*monsters[0].speed
        monsters[0].health = 2.5*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        for n in range (1, n_appearing + 1):
            monsters.append(Cultist("Cultist " + str(n)))
        announce ("You are attacked by a crew of Cultists!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
