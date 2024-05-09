from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random

class GoldenClaymore(Item):
    def __init__(self):
        super().__init__("golden-claymore", 1000) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (50,80)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class EthanJungleTemple(location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "temple"
        self.symbol = 'j'
        self.visitable = True
        self.starting_location = JungleEntrance(self)
        self.locations = {}
        self.locations["entrence"] = JungleEntrance(self)
        self.locations["temple"] = JungleTemple(self)
        self.locations["riddle_1"] = RiddleOne(self)
        self.locations["riddle_2"] = RiddleTwo(self)
        self.locations["riddle_3"] = RiddleThree(self)
        self.locations["treasure"] = Treasure(self)

    def enter(self, ship):
        announce ("You have arrived at a dense, mysterious jungle island.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class JungleEntrance(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "jungleEntrance"
        self.verbs['enter'] = self
        self.verbs['leave'] = self

    def enter(self):
        announce ("You stand at the edge of a dense jungle. You can see a mysterious temple deeper inside.\nYou can enter it.")
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "leave"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "enter"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["temple"]


class JungleTemple(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "jungleTemple"
        self.verbs['south'] = self
        self.verbs['enter'] = self

    def enter(self):
        announce ("You step into the ancient temple, feeling a sense of reverence and mystery.\nYou see a series of rooms with riddles to solve.")
        # Add riddles to solve here, if you get them right, you go to the next room, if you get them wrong, you get attacked by a monster, if you defeat the monster, you go to the next room anyways. At the end, you get a special item, a golden claymore sword
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "enter"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["riddle_1"]

class Riddle(location.SubLocation):
    def __init__(self, m, name, question, answers, correct, next_loc):
        super().__init__(m)
        self.name = name
        self.question = question
        self.answers = answers
        self.correct = correct
        self.next_loc = next_loc
        self.verbs['answer'] = self
        self.verbs['north'] = self

    def enter(self):
        print (f"\nThe wall reads the following\n\n")
        print (f"{self.question}\n")
        for key, value in self.answers.items():
            print (f"{key}) {value}\n")
        print ("\nAnswer with 'answer a' or 'answer b' or 'answer c' or 'answer d'\n")


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "answer"):
            if cmd_list[1] == self.correct:
                announce ("Correct! The door to the next room opens.")
                config.the_player.go = True
                config.the_player.next_loc = self.main_location.locations[self.next_loc]
            else:
                game = config.the_player
                randomPirate = random.choice(game.get_pirates())
                if (randomPirate.isLucky() == True):
                    announce(f"Incorrect! An arrow shoots from the wall at {randomPirate.get_name()}, but luckely it misses!\n")
                else:
                    randomPirate.inflict_damage(10, " arrow shot.")
                    announce(f"Incorrect! An arrow shoots from the wall and injures {randomPirate.get_name()}! Try again!\n")

class RiddleOne(Riddle):
    def __init__(self, m):
        question = "What has keys but can't open locks?"
        answers = {
            "a": "A piano",
            "b": "A computer",
            "c": "A book",
            "d": "A map"
        }
        correct = "a"
        next_loc = "riddle_2"
        super().__init__(m, "riddleOne", question, answers, correct, next_loc)

    def enter(self):
        print ("The doors all slam around you, there's no turning back now...")
        super().enter()

class RiddleTwo(Riddle):
    def __init__(self, m):
        question = "What has a head, a tail, is brown, and has no legs?"
        answers = {
            "a": "A snake",
            "b": "A horse",
            "c": "A penny",
            "d": "A banana"
        }
        correct = "c"
        next_loc = "riddle_3"
        super().__init__(m, "riddleTwo", question, answers, correct, next_loc)

class RiddleThree(Riddle):
    def __init__(self, m):
        question = "The more you take, the more you leave behind. What am I?"
        answers = {
            "a": "A secret",
            "b": "Footprints",
            "c": "Money",
            "d": "Time"
        }
        correct = "b"
        next_loc = "treasure"
        super().__init__(m, "riddleThree", question, answers, correct, next_loc)

class Treasure(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "treasure"
        self.verbs['leave'] = self

    def enter(self):
        announce ("You have solved all the riddles and have reached the treasure room! You see a golden claymore sword in the middle of the room and take it.\nYou can now leave.")
        config.the_player.add_to_inventory([GoldenClaymore()])
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "leave"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False