
import random
import game.combat as combat
from game.display import announce
from game.items import *
from game.context import Context
from game import config


class CrewMate(Context):
    '''Describes a pirate crewmate. The player controls these.'''

    # possible_names = ['alice', 'bob', 'charlie', 'darren', 'eliza', 'francine', 'gale', 'hope']
    possible_names = ['Anne', 'Bartholomew', 'Benjamin', 'Po', 'Eliza', 'Edward', 'Grace', 'Henry', 'Mary', 'Paulsgrave', 'Jack', 'Turgut', 'William', 'Sayyida', 'Emanuel', 'Peter', 'Richard', 'Yang']
    longest_name = max([len(c) for c in possible_names] )

    def __init__ (self):
        super().__init__()
        self.name = random.choice (CrewMate.possible_names)
        CrewMate.possible_names.remove (self.name)
        self.max_health = 100
        self.death_cause = "" #track cause of death for the score log
        self.health = self.max_health
        #speed and move points for combat
        self.speed = 100 + random.randrange(-20,21)
        self.cur_move = 0
        #dictionary of skill success rates (in percent). Currently only used in combat.
        self.skills = {}
        self.skills["brawling"] = random.randrange(10,101)
        self.skills["swords"] = random.randrange(10,101)
        self.skills["guns"] = random.randrange(10,101)
        self.skills["cannons"] = random.randrange(10,101)
        self.skills["swimming"] = random.randrange(10,101)

        #list of equipped items. Currently only used in combat.
        self.items = []
        self.items.append(Cutlass())
        self.items.append(Flintlock())
        self.powder = 32

        #Status effects
        self.sick = False
        self.lucky = False

        #Things a pirate can do. Use name X to use (ex: anne equip flintlock)
        self.verbs['equip'] = self
        self.verbs['unequip'] = self
        self.verbs['inventory'] = self
        self.verbs['restock'] = self
        self.verbs['skills'] = self

    def __str__ (self):
        '''to string. Lists name and death cause (for score log)'''
        return self.name + " " + self.death_cause

    def get_name (self):
        return self.name

    def get_health (self):
        return self.health

    def receive_medicine (self, num):
        '''Makes the pirate no longer sick (but doesn't remove sickness event)'''
        if (num > 0):
            self.sick = False
            announce (self.name + " takes the medicine and is no longer sick!")

    def inflict_damage (self, num, deathcause):
        '''Injures the pirate. If needed, it will record the pirate's cause of death'''
        self.health = self.health - num
        if(self.health > 0):
            return False
        self.death_cause = deathcause
        return True

    def get_hunger (self):
        '''Sick pirates need more food.'''
        if (self.sick):
            return 3
        return 1

    def set_sickness (self, flag):
        self.sick = flag

    def start_day (self, ship):
        '''Beginning of day activities (days only occur while sailing on the ship)'''
        ship.take_food (self.get_hunger())
        if (self.sick):
            self.inflict_damage (1, "Died of their illness")
            if(self.health <= 0):
                announce(self.name + " has died of their illness!")
        self.start_turn ()

    def start_turn (self):
        '''Beginning of exploration turn activities (turns occur directly while exploring and as part of days)'''
        self.reload()

    def end_day (self):
        '''End of day activities (days only occur while sailing on the ship)'''
        if (self.sick):
            if (self.lucky == True or random.randint(1,10) == 1):
                self.sick = False
        self.lucky = False

    def print (self):
        '''Prints status to terminal'''
        outstring = "   " + self.name + " Health: " + str(self.health)
        if (self.sick):
            outstring = outstring + " --Sick"
        if (self.lucky):
            outstring = outstring + " ++Lucky"

        print (outstring)

    def print_skills (self):
        '''Prints status to terminal'''
        outstring = self.name + ":" + " "*(CrewMate.longest_name+1-len(self.name))
        for k in self.skills.keys():
            outstring = outstring + k + ":" + str(self.skills[k]) + " "
        print (outstring)

    def process_verb (self, verb, cmd_list, nouns):
        '''Processes commands'''
        #The pirate equips an item (based on the name of the item)
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

        #The pirate un-equips an item (based on the name of the item)
        elif (verb == "unequip"):
            if len(cmd_list) > 1:
                i = 0
                while i < len(self.items):
                    if self.items[i].name == cmd_list[1]:
                        found = self.items.pop(i)
                        config.the_player.inventory.append(found)
                        break
                    i += 1
            else:
                announce ("Unequip what?")

        #Prints a pirate's equipped items
        elif (verb == "inventory"):
            self.print_inventory()

        #Orders a pirate to restock their black powder (can only be done on ship)
        elif (verb == "restock"):
            if config.the_player.location != config.the_player.ship:
                announce ("Powder and shot can only be restocked on the ship!")
            else:
                self.restock()
        elif (verb == "skills"):
            self.print_skills ()
        else:
            print (self.name + " doesn't know how to " + verb)

    def print_inventory (self):
        for i in self.items:
            print (i)
        print ()

    def restock(self):
        '''pirate restocks their black powder from the ship's reserves'''
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
        '''pirate reloads their firearms (flintlock pistols are too time consuming to load in combat)'''
        for i in self.items:
            i.recharge(self)

    def getName(self):
        return self.name

    def getAttacks(self):
        '''gets the list of possible attacks for this pirate'''
        options = []
        if "brawling" in self.skills.keys():
            options.append(combat.CombatAction("punch",combat.Attack("punch", "punches", self.skills["brawling"], (1,11)), None))
        for i in self.items:
            attackList = i.getAttacks(self)
            if len(attackList) > 0:
                for putative_attk in attackList:
                    if putative_attk not in options:
                        options.append(putative_attk)
        return options
