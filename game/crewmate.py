
import random
from game.display import announce
from game.items import *


class CrewMate:

    # possible_names = ['alice', 'bob', 'charlie', 'darren', 'eliza', 'francine', 'gale', 'hope']
    possible_names = ['anne', 'bartholomew', 'benjamin', 'po', 'eliza', 'edward', 'grace', 'henry', 'mary', 'paulsgrave', 'jack', 'turgut', 'william', 'sayyida', 'emanuel', 'peter', 'richard', 'yang']

    def __init__ (self):
        self.name = random.choice (CrewMate.possible_names)
        CrewMate.possible_names.remove (self.name)
        self.max_health = 100
        self.death_cause = ""
        self.health = self.max_health
        self.speed = 100 + random.randrange(-20,21)
        self.cur_move = 0
        self.skills = {}
        self.skills["brawling"] = random.randrange(10,101)
        self.skills["swords"] = random.randrange(10,101)
        self.skills["guns"] = random.randrange(10,101)
        self.skills["cannons"] = random.randrange(10,101)
        self.skills["swimming"] = random.randrange(10,101)

        self.items = []
        self.items.append(Cutlass())
        self.items.append(Flintlock())

        self.sick = False
        self.lucky = False

    def get_name (self):
        return self.name

    def get_health (self):
        return self.health

    def receive_medicine (self, num):
        if (num > 0):
            self.sick = False
            announce (self.name + " takes the medicine and is no longer sick!")

    def inflict_damage (self, num, deathcause):
        self.health = self.health - num
        if(self.health > 0):
            return False
        self.death_cause = deathcause
        return True

    def get_hunger (self):
        if (self.sick):
            return 3
        return 1

    def set_sickness (self, flag):
        self.sick = flag

    def start_day (self, ship):
        ship.take_food (self.get_hunger())
        if (self.sick):
            self.inflict_damage (1, "Died of their illness")
            if(self.health <= 0):
                announce(self.name + " has died of their illness!")

    def end_day (self):
        if (self.sick):
            if (self.lucky == True or random.randint(1,10) == 1):
                self.sick = False
        self.lucky = False

    def print (self):
        outstring = "   " + self.name + " Health: " + str(self.health)
        if (self.sick):
            outstring = outstring + " --Sick"
        if (self.lucky):
            outstring = outstring + " ++Lucky"
            
        print (outstring)

    def process_verb (self, verb, cmd_list, nouns):
        print (self.name + " doesn't know how to " + verb)
