from game.display import menu

class Item():
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        self.damage = (0,0)
        self.firearm = False
        self.charge = False
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
        return (self.firearm == False or self.charge == True)

    def discharge(self):
        if(self.firearm):
            self.charge = False

    def recharge(self, owner):
        if self.firearm == True and self.charge == False and owner.powder > 0:
            self.charge = True
            owner.powder -= 1

    def pickTargets(self, attacker, allies, enemies):
        options = []
        for t in enemies:
            options.append("attack " + t.name)
        choice = menu (options)
        return [enemies[choice]]



class Cutlass(Item):
    def __init__(self):
        super().__init__("cutlass", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class Flintlock(Item):
    def __init__(self):
        super().__init__("flintlock", 400) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,100)
        self.firearm = True
        self.charge = True
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"
