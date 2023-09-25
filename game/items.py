from game.display import menu
import game.combat as combat
import random

class Item(combat.ActionResolver):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        self.damage = (0,0)
        self.firearm = False
        self.charges = 0
        self.usedUp = False
        self.skill = None
        self.verb = None
        self.verb2 = None

    def __str__(self):
        return self.name + " (" + str(self.value) + " shillings)"

    def __lt__(self, other):
        return self.name < other.name

    def value(self):
        return self.value

    def ready(self):
        return (self.firearm == False or self.charges > 0)

    def discharge(self):
        if(self.firearm):
            self.charges -= 1

    def recharge(self, owner):
        if self.firearm == True and self.charges == 0 and owner.powder > 0:
            self.charges = 1
            owner.powder -= 1

    def getAttacks(self, owner):
        attacks = []
        if self.damage[1] > 0 and self.verb != None and self.skill in owner.skills.keys() and self.ready():
            attacks.append(combat.CombatAction(self.verb + " with " + self.name, combat.Attack(self.name, self.verb2, owner.skills[self.skill], self.damage, self.firearm), self))

        return attacks

    def pickTargets(self, action, attacker, allies, enemies):
        options = []
        for t in enemies:
            options.append("attack " + t.name)
        choice = menu (options)
        return [enemies[choice]]

    def resolve(self, action, moving, chosen_targets):
        super().resolve(action, moving, chosen_targets)
        if (action.attack.gunshot == True):
            self.discharge()


class Cutlass(Item):
    def __init__(self):
        super().__init__("cutlass", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class BelayingPin(Item):
    def __init__(self):
        super().__init__("belaying-pin", 1) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (5,30)
        self.skill = "melee"
        self.verb = "bash"
        self.verb2 = "bashes"

class Flintlock(Item):
    def __init__(self):
        super().__init__("flintlock", 400) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,100)
        self.firearm = True
        self.charges = 1
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"
