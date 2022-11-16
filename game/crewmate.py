
import random
from game.display import announce
from game.items import *
from game.context import Context
from game import config


class CrewMate(Context):

    # possible_names = ['alice', 'bob', 'charlie', 'darren', 'eliza', 'francine', 'gale', 'hope']
    possible_names = ['anne', 'bartholomew', 'benjamin', 'po', 'eliza', 'edward', 'grace', 'henry', 'mary', 'paulsgrave', 'jack', 'turgut', 'william', 'sayyida', 'emanuel', 'peter', 'richard', 'yang']

    def __init__ (self):
        super().__init__()
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
        self.powder = 32

        self.sick = False
        self.lucky = False

        self.verbs['equip'] = self
        self.verbs['unequip'] = self
        self.verbs['inventory'] = self
        self.verbs['restock'] = self

    def __str__ (self):
        return self.name + " " + self.death_cause

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
        self.reload()
        if (self.sick):
            self.inflict_damage (1, "Died of their illness")
            if(self.health <= 0):
                announce(self.name + " has died of their illness!")

    def start_turn (self):
        self.reload()

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
        if (verb == "equip"):
            if len(cmd_list) > 1:
                i = 0
                while i < len(config.the_player.inventory):
                    if config.the_player.inventory[i].name == cmd_list[1]:
                        found = config.the_player.inventory.pop(i)
                        self.items.append(found)
                        break
                    i += 1
            else:
                announce ("Equip what?")
        elif (verb == "unequip"):
            if len(cmd_list) > 1:
                i = 0
                while i < len(self.items):
                    if self.items[i].name == cmd_list[1]:
                        found = self.pop(i)
                        config.the_player.inventory.append(found)
                        break
                    i += 1
            else:
                announce ("Unequip what?")
        elif (verb == "inventory"):
            self.print_inventory()
        elif (verb == "restock"):
            if config.the_player.location != config.the_player.ship:
                announce ("Powder and shot can only be restocked on the ship!")
            else:
                self.restock()
        else:
            print (self.name + " doesn't know how to " + verb)

    def print_inventory (self):
        for i in self.items:
            print (i)
        print ()

    def restock(self):
        restock_needed = 32 - self.powder
        if config.the_player.powder > restock_needed:
            self.powder += restock_needed
            config.the_player.powder -= restock_needed
        else:
            self.powder += config.the_player.powder
            config.the_player.powder = 0
        if restock_needed == 0:
            announce (self.name + " doesn't need a restock!")
        else:
            announce (self.name + " restocks their powder and shot!")
    def reload(self):
        for i in self.items:
            if i.firearm == True and i.charge == False and self.powder > 0:
                i.charge = True
                self.powder -= 1
