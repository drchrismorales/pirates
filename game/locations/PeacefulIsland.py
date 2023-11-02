from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class PeacefulIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'T'
        self.visitable = True
        self.starting_location = BeachWithShip(self)
        self.locations = {}

        self.locations["northBeach"] = NorthBeach(self)
        self.locations["shed"] = Shed(self)

        self.locations["southBeach"] = self.starting_location
        self.locations["eastBeach"] = EastBeach(self)
        self.locations["westBeach"] = WestBeach(self)

        self.locations["southHill"] = SouthHill(self)
        self.locations["shrine"] = Shrine(self)

    def enter (self, ship):
        print ("You have arrived at a seemingly tranquil island.")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class BeachWithShip (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # All the beaches on the island have a 25% chance for a seagull encounter.
        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        announce ("You arrive at the beach of a seemingly peaceful island.\n" +
                  "Your ship is at anchor in a small bay to the south.\n" +
                  "The calm blow of the wind rustles the ancient-looking tress adorned with vibrant foliage.\n" + 
                  "Up ahead, you can see a a shrine sitting atop a hill.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["southHill"]
        elif (verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]

class EastBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "eastBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You walk upon the east beach of the island.\nThe sand is smooth beneath your feet."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["shrine"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]

class WestBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "westBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You walk upon the west beach of the island.\nUnnaturally tall palm tress hang high above your head."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["shrine"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]

# North Beach + Shed

class NorthBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "northBeach"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['enter'] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You walk upon the north beach of the island.\nA worn-down shed sits to the side of the beach. You can enter it."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["shrine"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
        if (verb == "enter"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["shed"]

class Shed (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "shed"
        self.verbs['exit'] = self
        self.verbs['leave'] = self

        self.event_chance = 100
        self.events.append(GiantSpiderEvent())

    def enter (self):
        description = "Rotted wood lines the walls of the musty shed."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]
            config.the_player.go = True

class GiantSpiderEvent (event.Event):

    def __init__ (self):
        self.name = " giant spider attack."

    def process (self, world):
        result = {}
        spider = GiantSpider()
        announce("A giant spider leaps from the ceiling and attacks your crew!")
        combat.Combat([spider]).combat()
        announce("The giant spider goes limp.")
        # Set newevents to an empty list. If I added 'self' to the list, the event would be readded upon completing, effectively making the spider respawn every turn you are in here.
        result["newevents"] = []
        # Set the result message to an empty string, as we are printing our own strings at the right time.
        result["message"] = ""

        announce("In the shed, you find a double-headed hoe. It looks like it'd make a decent weapon.")
        config.the_player.add_to_inventory([DoubleHoe()])
        
        return result
    
class GiantSpider(Monster):
    
    # Giant spider can bite or slash. Both do the same damage, it's just a flavor difference.
    # 100-110 speed. 64-96 health.
    def __init__ (self):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(60,80), (5,15)]
        attacks["slash"] = ["slashes",random.randrange(60,80), (5,15)]
        super().__init__("Giant Spider", random.randint(64,96), attacks, 100 + random.randint(0, 10)) 

class DoubleHoe(Item):

    # Less damage than a cutlass, but lets you pick up to two targets per fight.
    def __init__(self):
        super().__init__("double-hoe", 10) 
        self.damage = (8,50) 
        self.skill = "swords"
        self.verb = "slam"
        self.verb2 = "slams"
        self.NUMBER_OF_ATTACKS = 2 # Number of attacks to be made in pickTargets

    def pickTargets(self, action, attacker, allies, enemies):
        if (len(enemies) <= self.NUMBER_OF_ATTACKS): # If less than or equal to two targets, hit everyone
            return enemies
        else:
            options = []
            for t in enemies:
                options.append("attack " + t.name)
            targets = []

            while(len(targets) < self.NUMBER_OF_ATTACKS): # While loop so that it keeps going until the player picks two different targets.
                print(f"Pick target number {len(targets)}.")
                choice = menu(options)
                if(not choice in targets):
                    targets.append(enemies[choice])
            return targets

# Hill + Shrine

class SouthHill (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southHill"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['pick'] = self
        self.flowers = SouthHill.GetThreeFlowerColors()

    def enter (self):
        description = "You walk forward through the tress and up the south end of the hill towards the shrine.\nColorful flowers dot the grass you walk through. It might be fun to pick one from the ground."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[verb + "Beach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["shrine"]

        # If the player chooses to pick a flower, ask them for their input and then run another function if needed.
        if(verb == "pick"):
            pickedFlower = False
            while(not pickedFlower):
                print("You spot three flowers to pick from. Choose one!")
                for i in self.flowers:
                    print("-" + i)
                print("-Leave.")

                flowerChoice = input()

                # If the player chooses to leave, return in order to end the function.
                if("leave" in flowerChoice.lower()):
                    return

                # We make the player's choice lowercase and then uppercase the first letter in order to make it non-case sensitive and also directly work with what GetThreeFlowerColors() returns.
                flowerChoice = flowerChoice.lower()
                flowerChoice = flowerChoice[0].upper() + flowerChoice[1:]

                if(flowerChoice in self.flowers):
                    self.flowers.remove(flowerChoice)
                    pickedFlower = True
                    
                    # Handle the appropriate effect for the flower color that the player chose.
                    SouthHill.GetEffectFromFlowerColor(flowerChoice)

                    flowerChoice = flowerChoice[0].lower() + flowerChoice[1:]
                    print(f"You picked the {flowerChoice} flower.")

    # Returns a list of three random flowers from the list defined below. As we don't refer to 'self' anywhere inside, we can make it a static method (meaning it's not tied to an instance of an object).
    @staticmethod
    def GetThreeFlowerColors():
        listOfColors = ["Red", "Blue", "Green", "White", "Black"]
        return random.choices(listOfColors, k=3)
    
    # Handles the effect of the flower inputted through the 'choice' parameter.
    @staticmethod
    def GetEffectFromFlowerColor(choice):
        # We refer to config.the_player a bunch in this function, so it's more convenient to make it a variable here so that we don't have to type out the whole thing every time. Shouldn't affect readability. 
        game = config.the_player 
        
        # Harm a random crewmate for picking the flower from the field it was so peacefully resting in. Gives a decent bit of score.
        if(choice == "Red"):
            randomPirate = random.choice(game.get_pirates())
            randomPirate.inflict_damage(10, " disturbing nature.")

            game.add_to_inventory([RedFlower()])
            announce(f"{randomPirate.get_name()} feels a sharp pang throughout their body as they pick the flower.")

        # "Time Travel" the crew, doing a few different things:
        #   -Randomizes the ship position and sets the crew's position to be the ship. 
        #   -Heals or hurts pirates at random, as if they were damaged from their travels.
        #   -Makes some sick or lucky at random.
        #   -Randomizes the ship's food and medicine.
        elif(choice == "Blue"): 
            spotX = random.randint(1, 5)
            spotY = random.randint(1, 5)
            # Make either movement negative at a 50% chance. 
            if(random.randint(0, 1) == 0):
                spotX *= -1
            if(random.randint(0, 1) == 0):
                spotY *= -1

            # Clamp the numbers so the location can't be outside the world.
            spotX = numpy.clip(game.ship.loc.get_x() + spotX, 0, game.world.worldsize)
            spotY = numpy.clip(game.ship.loc.get_y() + spotY, 0, game.world.worldsize)
                
            new_loc = game.world.get_loc (spotX, spotY)
            game.go = True
            game.ship.set_loc (new_loc)
            game.next_loc = game.ship
            game.visiting = False

            for i in game.get_pirates():
                # Mess with the crewmate's health a bit.
                i.health //= random.uniform(0.5, 1.5)
                i.health += random.randrange(-20, 20)
                if(i.health > i.max_health):
                    i.health = i.max_health

                i.death_cause = "Unknown causes."

                # Randomize sickness or luckiness.
                if(random.randint(0, 2) == 0):
                    i.lucky = True
                if(random.randint(0, 2) == 0):
                    i.sick = True

            # The crew would've used food and medicine over time, along with possibly obtaining some.
            game.ship.food //= random.uniform(0.5, 1.5)
            game.ship.medicine //= random.uniform(0.5, 1.5)

            game.add_to_inventory([BlueFlower()])
            announce(f"As soon as your crew picks the flower, you blink, and you seem to suddenly be a few days further in time.")

        # Nothing special, just an extra 5 free score at the end.
        elif(choice == "Green"): 
            game.add_to_inventory([GreenFlower()])
            announce(f"You pick the flower from the field. Nothing seems to happen.")

        # Reroll a pirate's stats
        elif(choice == "Black"): 
            randomPirate = random.choice(game.get_pirates())
            randomPirate.skills["brawling"] = random.randrange(10,101)
            randomPirate.skills["swords"] = random.randrange(10,101)
            randomPirate.skills["melee"] = random.randrange(10,101)
            randomPirate.skills["guns"] = random.randrange(10,101)
            randomPirate.skills["cannons"] = random.randrange(10,101)
            randomPirate.skills["swimming"] = random.randrange(10,101)
            announce(f"The black flower wilts as soon as {randomPirate.get_name()} picks it. They feel different.")
        
        # Add three instances of the seagull event to the worldwide event pool.
        elif(choice == "White"):
            SEAGULL_COUNT = 3
            for i in range(SEAGULL_COUNT):
                game.world.events.append(seagull.Seagull())
            game.add_to_inventory([WhiteFlower()])
            announce("You hear a loud squawking in the distance as you pick the white flower.")
        
class GreenFlower(Item): # 5 free score.
    def __init__(self):
        super().__init__("green-flower", 5) 

class WhiteFlower(Item): # 10 free score because you have to put up with more seagulls.
    def __init__(self):
        super().__init__("white-flower", 10) 

class BlueFlower(Item): # 25 free score. Time travel is risky.
    def __init__(self):
        super().__init__("blue-flower", 10) 

class RedFlower(Item): # 50 free score, since you need to take damage for it.
    def __init__(self):
        super().__init__("red-flower", 50) 

# A shrine to an ancient deity. An invisible spirit guardian protects it, rewarding those who show wisdom. 
class Shrine (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "westBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['investigate'] = self
        self.shrineUsed = False

    def enter (self):
        description = "You walk to the top of the hill. A finely-crafted shrine of scarlet and yellow wood stands before you. You may investigate it."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
        if(verb == "south"):
            config.the_player.next_loc = self.main_location.locations[f"southHill"]
        if(verb == "investigate"):
            self.HandleShrine()

    # Handles the logic and output for the shrine.
    def HandleShrine(self):
        if(not self.shrineUsed):
            print("As you investigate the shrine, your body freezes up, and a mysterious voice echoes into your mind.")
            print("'Lost travelers... I am the spirit guardian of this shrine. I can provide you with bountiful luck and vitality if you answer my riddle.'")
            choice = input("Answer the spirit's riddle? ")
            if("yes" in choice.lower()):
                self.HandleRiddles()
            else:
                print("You turn away from the shrine.")
        else:
            print("The shrine is inert.")

    # Handles everything for the shrine spirit's riddles.
    def HandleRiddles(self):
        riddle = self.GetRiddleAndAnswer()
        guesses = 3

        # While the player still has guesses, ask for their answer and respond appropriately.
        while guesses > 0:
            print(riddle[0])
            plural = ""
            if(guesses != 1):
                plural = "s"
            
            print(f"You may guess {guesses} more time{plural}.") 
            choice = input("What is your guess? ")
            if riddle[1] in choice:
                self.RiddleReward()
                announce("Feeling blessed by the shrine spirit, you say your thanks and turn away.")
                return
            else:
                guesses -= 1
                announce("You have guessed incorrectly.")

        if(guesses <= 0):
            self.shrineUsed = True

    # Returns a random riddle from the list defined below.
    def GetRiddleAndAnswer(self):
        riddleList = [ # A list of tuples. The first item is the riddle, while the second item is the answer.
            ("On four long legs, my slim body sits. I eat not a bite, and drink not a sip. With a passionless face I greet countless guests, whom I carry all day without needing to rest. What am I?", "chair"),
            ("Under a full moon, I throw a yellow hat into the red sea. What happens to the yellow hat?", "wet"),
            ("Four legs in the morning, two in the afternoon, three in the evening. What am I?", "person"),
            ("I have four corners like a square pancake, but I'm stuffed and seasoned and carefully baked. I pass through the lips one piece at a time, the more you consume, the broader your mind. What am I?", "book")
            ]
        return random.choice(riddleList)
    
    # Reward the player by making all of their pirates lucky, not sick, and fully healed.
    def RiddleReward(self):
        announce("You have guessed correctly. I will now mend your crew and bless them with luck.")
        for i in config.the_player.get_pirates():
            i.lucky = True
            i.sick = False
            i.health = i.max_health
        self.shrineUsed = True

# made by zach \o/