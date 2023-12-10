from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items


import game.combat as combat
import game.event as event
import random


# Made by Joseph
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
        self.verbs["help"] = self
        self.verbs["hint"] = self
        self.verbs["exit"] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())

    def enter(self):
        description = "You are on the island's beach. Your ship is anchored here.\n"
        description += "To your north is a hill. To your west is a forest."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            if len(cmd_list) > 1:
                config.the_player.go = True
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

        if verb == "hint" or verb == "help":
            announce("Use \"go ship\" to return to your ship.")

        if verb == "exit":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
            

class Cliff(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cliff"
        self.verbs["go"] = self
        self.verbs["take"] = self
        self.verbs["hint"] = self
        self.verbs["help"] = self
        self.items = {"Cutlass":items.Cutlass(), "dagger":Dagger()} # Dict is used for ease of item removal when removing. List would work but it's more clunky.
        self.ladder_open = False

    def enter(self):
        description = "You are at the island's highest point. There is a town here.\n"
        description += "Many buildings seem worse for wear. Many, if not all have been abandoned.\n"
        
        if len(self.items) > 0:
            description += "Some weapons remain in what once was the town's armory. You see "
            for num, item in enumerate(self.items):
                if num == len(self.items) - 1:
                    description += "and a"
                else:
                    description += "a"

                description += f" {self.items[item].name}"
                description += "." if num == len(self.items) - 1 else ", "
        
        if self.ladder_open:
            description += "\nYou may re-enter the temple through the ladder."

        announce(description)
        self.event_chance = 50
        self.events.append (seagull.Seagull())

    def open_ladder(self):
        self.ladder_open = True

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go" and len(cmd_list) > 1:
            config.the_player.go = True
            if cmd_list[1] == "south":
                config.the_player.next_loc = self.main_location.locations["beach"]
            elif cmd_list[1] == "ladder" and self.ladder_open:
                config.the_player.next_loc = self.main_location.locations["sanctuary"]
            elif (
                cmd_list[1] == "west"
                or cmd_list[1] == "east"
                or cmd_list[1] == "north"
            ):
                announce("Nothing but open ocean.")
            else:
                announce(f"Direction not recognized. This location only recognizes cardinal directions{' and ladder' if self.ladder_open else ''}.\n")

        if verb == "take":
            if len(cmd_list) > 1:
                at_least_one = False
                for key in dict(self.items):
                    if cmd_list[1] == self.items[key].name or cmd_list[1] == "all":
                        announce(f"You take the {self.items[key].name}.")
                        item = self.items.pop(key)
                        config.the_player.add_to_inventory([item])
                        config.the_player.go = True

                        at_least_one = True
                
                if not at_least_one:
                    announce("No items of that name here.")
            else:
                announce("Must enter an item name, or all.")

        if verb == "hint" or verb == "help":
            announce("Use \"take {item name}\" to take an item.")
        

class Ruins(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "ruins"
        self.verbs["go"] = self
        self.verbs["hint"] = self
        self.verbs["help"] = self

    def enter(self):
        # The description has a base description, followed by variable components.
        description = "You and your remaining team make their way through the dense foliage. The sunlight beams brightly through a clearing ahead.\n"
        description += "You see ruins of a temple. "
        if not self.main_location.locations["temple_entrance"].entered_before:
            description += "The entrance looks unstable. It might not stay open for much longer."
        else:
            description += "The entrance is destroyed.\nHowever, the ladder you used to escape is still accessible on the cliffside."

        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go" and len(cmd_list) > 1:
            config.the_player.go = True
            if cmd_list[1] == "east":
                config.the_player.next_loc = self.main_location.locations["beach"]
            elif cmd_list[1] == "temple" or cmd_list[1] == "ruins":
                if not self.main_location.locations["temple_entrance"].entered_before:
                    config.the_player.next_loc = self.main_location.locations["temple_entrance"]
                else:
                    announce("The entrance is collapsed, it would be unwise to enter again.")
            elif cmd_list[1] == "south" or cmd_list[1] == "west":
                announce("The foliage in that direction is too thick to cut through.")

        if verb == "help" or verb == "hint":
            description = "this island uses directions other than cardinal directions at times.\n"
            description += "If you want to explore the ruins, use \"go ruins\"."
            announce(description)


class Temple_Entrance(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "entrance"
        self.verbs["go"] = self
        self.verbs["hint"] = self
        self.verbs["help"] = self
        self.entered_before = False

    def enter(self):
        if not self.entered_before:
            description = "You and your crewmates enter the structure. Suddenly, the entrance collapses.\n"
            # TODO: Add a specific pirate name at random. Maybe make it a recurring joke.
            description += 'One of the pirates groans. "Not this again..," they mutter.\n\n'
        else:
            description = "You are in the central chamber.\n"

        description += "Though the room is dim, you can make out doorways to your left and right."

        announce(description)
        self.entered_before = True

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            config.the_player.go = True
            if len(cmd_list) > 1:
                if cmd_list[1] == "crypt" or cmd_list[1] == "left":
                    config.the_player.next_loc = self.main_location.locations["crypt"]
                elif cmd_list[1] == "vestibule" or cmd_list[1] == "right":
                    config.the_player.next_loc = self.main_location.locations["vestibule"]

        if verb == "hint" or verb == "help":
            announce("Use \"go {left|right}\" to move to the appropriate room.")


class Crypt(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "crypt"
        self.verbs["go"] = self
        self.verbs["look"] = self
        self.verbs["hint"] = self
        self.verbs["help"] = self
        self.verbs["read"] = self
        self.saw_book = False

    def enter(self):
        description = "You walk down a spiral staircase.\n"
        description = "At the bottom you find a long hallway with tombs on either side.\n"
        description += "On the far wall you see a bookcase."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go" and len(cmd_list) > 1:
                config.the_player.go = True
                if cmd_list[1] == "back" or cmd_list[1] == "entrance":
                    config.the_player.next_loc = self.main_location.locations["temple_entrance"]

        if verb == "look":
            description = "You see a single book on the bookcase. The cover has a cryptic image scribbled into the corner:\n\n"
            description += "▒▒▒▒▒▒▒▒▒▒▒▒\n"
            description += "▒ ┌─o  ┌─┐ ▒\n"
            description += "▒ │    │ │ ▒\n"
            description += "▒ └────┘ │ ▒\n"
            description += "▒  ──────┘ ▒\n"
            description += "▒▒▒▒▒▒▒▒▒▒▒▒\n"
            announce(description)
            self.saw_book = True

        if verb == "hint" or verb == "help":
            if not self.saw_book:
                description = "try looking at the bookcase."
            else:
                description = "This symbol might have some meaning in another room."
            description += "\nTo leave this room, use \"go back\"."
            announce(description)


class Vestibule(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "vestibule"
        self.verbs["go"] = self
        self.verbs["hint"] = self
        self.verbs["help"] = self
        self.verbs["solve"] = self
        self.verbs["look"] = self
        self.door_open = False

    def enter(self):
        description = "You walk into the vestibule. On the far side of the room there is a sealed door."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go":
            if len(cmd_list) > 1:
                config.the_player.go = True
                if cmd_list[1] == "entrance" or cmd_list[1] == "back":
                    config.the_player.next_loc = self.main_location.locations["temple_entrance"]
                if cmd_list[1] == "door" or cmd_list[1] == "nave":
                    if self.door_open:
                        config.the_player.next_loc = self.main_location.locations["nave"]
                    else:
                        announce("The door is locked. There must be some way to open it. \"Look\" for clues.") # Hint hint

        elif verb == "look":
            # This puzzle is inspired by Tunic. Play it if you haven't already, saying anything else would be a spoiler.
            description = "On further inspection, you notice a row of buttons laid out beside it. The 4 buttons are labeled U, D, L, and R.\n"
            description += "Below the panel is a drawing of a fox... reading a book? They seem perplexed.\n"
            description += "Weird runes are written in an abstract \"language\" below. You can't read them.\n"
            description += "(To try a solution, use \"solve {solution}\")."
            announce(description)

        elif verb == "solve":
            if len(cmd_list) > 1:
                if cmd_list[1].lower() == "ldrurdl":
                    # Open the door
                    self.door_open = True
                    # Announce that it opened
                    announce("The door has been opened.")
                else:
                    announce("Incorrect solution (Solution must be one word, no spaces).")
            else:
                announce("No solution entered.")

        elif verb == "help" or verb == "hint":
            description = "Looking closer at the panel could give some insight.\n"
            description += "Commands:\n"
            description += "* go back\n"
            description += "* go door\n"
            description += "* solve {solution}"
            announce(description)


class Nave(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "nave"
        self.verbs["go"] = self
        self.verbs["help"] = self
        self.verbs["hint"] = self
        self.events.append(Cultists())
        self.event_chance = 100
        self.room_entered = False

    def enter(self):
        description = (
            "Your crew walks into the central nave. The room is in disrepair."
            " Large cracks have formed on the walls,"
            "\nand the crashing ocean can be heard through shattered windows."
            " there is a door behind the altar leading to the inner sanctuary."
        )
        if not self.room_entered:
            description += "\nThere is an uneasiness in the air. You hear... voices, coming from the room across the aisle."
        announce(description)


        if not self.room_entered:
            announce("\nThe voices suddenly become quiet.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "go" and len(cmd_list) > 1:
            config.the_player.go = True
            if cmd_list[1] == "back" or cmd_list[1] == "vestibule":
                config.the_player.next_loc = self.main_location.locations[
                    "vestibule"
                ]
            elif "sanctuary" in cmd_list or "entryway" in cmd_list or "altar" in cmd_list:
                config.the_player.next_loc = self.main_location.locations["sanctuary"]

        elif verb == "help" or verb == "hint":
            description = "Commands:\n"
            description += "* go back\n"
            description += "* go entryway\n"
            announce(description)


class Sanctuary(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "sanctuary"
        self.verbs["go"] = self
        self.verbs["take"] = self
        self.verbs["hint"] = self
        self.verbs["help"] = self
        self.medicine_left = True
        self.food_left = True
        self.items = {"musket":Musket(), "cutlass":items.Cutlass(), "flintlock":items.Flintlock()}

    def enter(self):
        description = "You've found the inner sanctuary. There is a ladder leading out of this area.\n"
        self.main_location.locations["cliff"].open_ladder() #Not sure if there's a better way to do this

        if len(self.items) > 0:
            description += "There are weapons hanging on the wall. You see "
            for num, item in enumerate(self.items):
                if num == len(self.items) - 1:
                    description += "and a"
                else:
                    description += "a"

                description += f" {self.items[item].name}"
                description += "." if num == len(self.items) - 1 else ", "

            if self.food_left:
                description += "\nThere is food in this room."
            if self.medicine_left:
                description += "\nThere is medicine in this room."
            
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        # bodge job, but it makes sure the cultists wont appear in the area again.
        self.event_chance = 0
        if verb == "go" and len(cmd_list) > 1:
            config.the_player.go = True
            if cmd_list[1] == "ladder" or cmd_list[1] == "up":
                self.main_location.locations["cliff"].open_ladder()
                config.the_player.next_loc = self.main_location.locations["cliff"]
            elif cmd_list[1] == "nave" or cmd_list[1] == "back":
                config.the_player.next_loc = self.main_location.locations["nave"]

        if verb == "take":
            if len(cmd_list) > 1:
                at_least_one = False
                for key in dict(self.items):
                    if cmd_list[1] == self.items[key].name or cmd_list[1] == "all":
                        announce(f"You take the {self.items[key].name}.")
                        item = self.items.pop(key)
                        config.the_player.add_to_inventory([item])
                        config.the_player.go = True

                        at_least_one = True
                    
                if self.food_left and (cmd_list[1] == "food" or cmd_list[1] == "all"):
                    announce("You take the food.")
                    config.the_player.ship.food += 25
                    config.the_player.go = True
                    self.food_left = False
                    at_least_one = True

                if self.medicine_left and (cmd_list[1] == "food" or cmd_list[1] == "all"):
                    announce("You take the medicine.")
                    config.the_player.ship.medicine += 3
                    config.the_player.go = True
                    self.medicine_left = False
                    at_least_one = True
                
                if not at_least_one:
                    announce("No items of that name here.")

        if verb == "hint" or verb == "help":
            announce("Use \"go ladder\" to leave this area.")


class Cultist(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["curse"] = ["curses", random.randrange(40,60), (15, 25)]
        attacks["stab"] = ["recklessly stabs", random.randrange(75, 90), (5, 12)]
        attacks["summon"] = ["summons a staff and strikes", random.randrange(30, 70), (12, 22)]
        if random.randint(1, 10) == 1 or name == "Cult Leader":
            # Literally able to just summon from the underworld
            attacks["ritual"] = ["provokes an eldrich horror to attack", random.randrange(60, 85), (25, 45)]
        else:
            # Otherwise just hurls a pocket knife or something  
            attacks["throw"] = ["throws a small blade at", random.randrange(40, 50), (10, 30)]

        super().__init__(
            name, random.randrange(40, 60), attacks, 75 + random.randrange(-10, 11)
        )


class Cultists(event.Event):
    """
    A combat encounter with a group of cultists. Based on drowned pirate code.
    When the event is drawn, creates a combat encounter with 2 to 6 cultists. kicks control over to the combat code to resolve the fight,
    then adds itself and a simple success message to the result.
    """

    def __init__(self, max_count = 7):
        self.name = " cultists"
        self.max_count = max_count

    def process(self, world):
        """Process the event. The first Cultist becomes a cult leader, buffing its speed and health."""
        result = {}
        result["message"] = "The cultists are defeated!"
        monsters = []
        min = 4
        uplim = self.max_count - 1
        monsters.append(Cultist("Cult Leader"))
        monsters[0].speed = 1.2 * monsters[0].speed
        monsters[0].health = 2.5 * monsters[0].health
        n_appearing = random.randrange(min, uplim)
        for n in range(1, n_appearing + 1):
            monsters.append(Cultist("Cultist " + str(n)))
        announce(f"The crew is attacked by {n_appearing + 1} cultists!")
        combat.Combat(monsters).combat()
        result["newevents"] = [self]
        return result


class Musket(items.Item):
    def __init__(self):
        super().__init__("musket", 500) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20, 120)
        self.firearm = True
        self.charges = 1
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"

class Dagger(items.Item):
    def __init__(self):
        super().__init__("dagger", 10) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20, 40)
        self.skill = "melee"
        self.verb = "stab"
        self.verb2 = "stabs"

# Not actually in my level, but it would be a funny concept, an instakill weapon with 3 charges that can't be reloaded
'''
class Noisy_Cricket(items.Item):
    def __init__(self):
        super().__init__("noisy cricket", 1) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (99999, 99999)
        self.firearm = True
        self.charges = 3
        self.skill = "cannons"
        self.verb = "shoot"
        self.verb2 = "de-atomizes"
'''