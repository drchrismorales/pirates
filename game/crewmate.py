
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce
import game.items as items
from game.context import Context
import game.config as config


class CrewMate(Context, superclasses.CombatCritter):
    '''Describes a pirate crewmate. The player controls these.'''

    # possible_names = ['alice', 'bob', 'charlie', 'darren', 'eliza', 'francine', 'gale', 'hope']
    possible_names = ['Anne', 'Bartholomew', 'Benjamin', 'Po', 'Eliza', 'Edward', 'Grace', 'Henry', 'Mary', 'Paulsgrave', 'Jack', 'Turgut', 'William', 'Sayyida', 'Emanuel', 'Peter', 'Richard', 'Yang']
    longest_name = max([len(c) for c in possible_names] )

    def __init__ (self):
        self.max_health = 100
        Context.__init__(self)
        superclasses.CombatCritter.__init__(self, random.choice (CrewMate.possible_names), self.max_health, 100 + random.randrange(-20,21))
        CrewMate.possible_names.remove (self.name)
        self.death_cause = "" #track cause of death for the score log
        self.hurtToday = False
        self.cur_move = 0
        #dictionary of skill success rates (in percent). Currently only used in combat.
        self.skills = {}
        self.skills["brawling"] = random.randrange(10,101)
        self.skills["swords"] = random.randrange(10,101)
        self.skills["melee"] = random.randrange(10,101)
        self.skills["guns"] = random.randrange(10,101)
        self.skills["cannons"] = random.randrange(10,101)
        self.skills["swimming"] = random.randrange(10,101)

        #list of equipped items. Currently only used in combat.
        self.items = []
        self.items.append(items.Cutlass())
        self.items.append(items.Flintlock())
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

        #List of defenders
        self.defenders = []

        #List of defendees
        self.defendees = []

    def __str__ (self):
        '''to string. Lists name and death cause (for score log)'''
        return self.name + " " + self.death_cause

    def get_health (self):
        return self.health

    def receive_medicine (self, num):
        '''Makes the pirate no longer sick (but doesn't remove sickness event)'''
        if (num > 0):
            self.sick = False
            announce (self.name + " takes the medicine and is no longer sick!")

    def inflict_damage (self, num, deathcause, combat=False):
        '''Injures the pirate. If needed, it will record the pirate's cause of death'''
        if combat and len(self.defenders) > 0:
            defender = random.choice (self.defenders)
            announce (f"{defender.name} blocks the attack!")
            return defender.inflict_damage ((num+1)//2, deathcause, False) #Combat should be false here to avoid possible infinite recursion.
        #else:
        self.health = self.health - num
        self.hurtToday = True
        if(self.health > 0):
            return None
        self.death_cause = deathcause
        for d in self.defendees:
            d.removeDefender(self)
        self.defendees = []
        for d in self.defenders:
            d.removeDefendee(self)
        self.defenders = []
        return self

    def addDefender(self, defender):
        self.defenders.append(defender)

    def addDefendee(self, defendee):
        self.defendees.append(defendee)

    def removeDefender(self, defender):
        self.defenders = [d for d in self.defenders if d != defender]

    def removeDefendee(self, defendee):
        self.defendees = [d for d in self.defendees if d != defendee]

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
        elif self.hurtToday == True:
            self.hurtToday = False
        elif self.health < 100:
            #Note: more serious wounds take MUCH longer to heal
            # Try to limit the damage you take in combat!
            if self.health >= 75:
                self.health += random.randint(1,10)
            elif self.health >= 50:
                self.health += random.randint(1,6)
            elif self.health >= 25:
                self.health += random.randint(1,4)
            else:
                self.health += 1
            #Cap at 100
            if self.health > 100:
                self.health = 100
        self.start_turn ()

    def start_turn (self):
        '''Beginning of exploration turn activities (turns occur directly while exploring and as part of days)'''
        self.reload()

    def end_day (self):
        '''End of day activities (days only occur while sailing on the ship)'''
        if (self.sick):
            if (self.isLucky() == True or random.randint(1,10) == 1):
                self.sick = False
        self.lucky = False

    def print (self):
        '''Prints status to terminal'''
        outstring = "   " + self.name + " Health: " + str(self.health)
        if (self.sick):
            outstring = outstring + " --Sick"
        if (self.isLucky()):
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
                        self.items.sort()
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
                        config.the_player.inventory.sort()
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
        elif config.the_player.powder == 0:
            if restock_needed < (32 - self.powder):
                announce (self.name + " takes the last powder!")
            else:
                announce (self.name + " reports that the ship is out of powder!")
        else:
            announce (self.name + " restocks their powder and shot!")

    def reload(self):
        '''pirate reloads their firearms (flintlock pistols are too time consuming to load in combat)'''
        for i in self.items:
            i.recharge(self)

    def getAttacks(self):
        '''gets the list of possible attacks for this pirate'''
        for d in self.defendees:
            d.removeDefender(self)
        self.defendees = []
        options = []
        for i in self.items:
            attackList = i.getAttacks(self)
            if len(attackList) > 0:
                for putative_attk in attackList:
                    if putative_attk not in options:
                        options.append(putative_attk)
        if "brawling" in self.skills.keys():
            options.append(superclasses.CombatAction("punch",superclasses.Attack("punch", "punches", self.skills["brawling"], (1,11), False), self))
        options.append(superclasses.CombatAction("defend",superclasses.Defend("defend", "defends"), self))
        return options
