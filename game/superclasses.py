from __future__ import annotations
from game.display import announce
from game.display import menu
import random

class Attack():
    """Basic attack object, with a name, description, chance of success, and damage range. Sufficient for specifying monster attacks."""
    def __init__ (self, name, description, success, damage_range, gunshot):
        self.name = name
        self.description = description
        self.success = success
        self.damage_range = damage_range
        self.gunshot = gunshot

    def __eq__(self, other):
        if not isinstance(other, Attack):
            return False
        if self.name == other.name and self.description == other.description and self.success == other.success and self.damage_range == other.damage_range:
            return True
        return False

class Defend():
    def __init__ (self, name, description):
        self.name = name
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Defend):
            return False
        if self.name == other.name and self.description == other.description:
            return True
        return False


class ActionResolver():
    def pickTargets(self, action, attacker, allies, enemies):
        """The player should pick targets"""
        options = []
        if isinstance(action.action, Defend):
            for t in allies:
                options.append("protect " + t.get_name())
            choice = menu (options)
            return [allies[choice]]
        else:
            for t in enemies:
                options.append("attack " + t.get_name())
            choice = menu (options)
            return [enemies[choice]]

    def resolve(self, action, moving, chosen_targets):
        chosen_attk = action.action
        if isinstance(chosen_attk, Defend):
            for chosen_target in chosen_targets:
                if chosen_target != None:
                    #Moving is defending chosen target. Moving is the defender and target is the defendee
                    moving.addDefendee(chosen_target)
                    chosen_target.addDefender(moving)
        else:
            for chosen_target in chosen_targets:
                if chosen_target != None:
                    roll = random.randrange(100)
                    if moving.isLucky() == True:
                        roll = min(roll, random.randrange(100))
                    if roll < chosen_attk.success:
                        announce (moving.get_name() + " " + chosen_attk.description + " " + chosen_target.get_name() + "!")
                        damage = random.randrange(chosen_attk.damage_range[0],chosen_attk.damage_range[1]+1)
                        deathcause = "slain by a " + moving.get_name() + "'s " + chosen_attk.name
                        deader = chosen_target.inflict_damage(damage, deathcause, True)
                        if not (deader is None):
                            announce (deader.get_name() + " is killed!")
                    elif (roll == chosen_attk.success):
                        announce (moving.get_name() + " barely misses " + chosen_target.get_name() + "!")
                    else:
                        announce (moving.get_name() + " misses " + chosen_target.get_name() + ".")

class CombatCritter(ActionResolver):
    def __init__(self, name, hp, speed):
        self.name = name
        self.lucky = False
        self.health = hp
        self.speed = speed

        #List of defenders
        self.defenders = []

        #List of defendees
        self.defendees = []

    def get_name(self):
        return self.name

    def isLucky(self):
        return self.lucky

    def inflict_damage (self, num, deathcause, combat = False):
        self.health = self.health - num
        if(self.health > 0):
            return None
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

    def getAttacks(self):
        return []

class CombatAction(ActionResolver):
    """A more sophisticated combat action object, with a name, Attack instance, and Resolver instance. Resolves all combat actions. Used for monster attacks, but the added complexity over Attack alone is meant for player actions."""
    def __init__ (self, name, action, resolver):
        self.name = name
        self.action = action
        self.resolver = resolver

    def __str__ (self):
        """To-string uses the Action's listed name"""
        return self.name

    def __eq__ (self, other):
        """Test-equals compares the two CombatActions' Attacks"""
        if not isinstance(other, CombatAction):
            return False
        return self.action == other.action

    def pickTargets(self, action, attacker, allies, enemies):
        """The player should pick targets. Passes through to the associated item if there is one, otherwise has the player pick one target"""
        if (self.resolver != None):
            return self.resolver.pickTargets(action, attacker, allies, enemies)
        else:
            return super().pickTargets(action, attacker, allies, enemies)

    def resolve(self, action, moving, chosen_targets):
        """The action resolves itself, using moving and the chosen_targets"""
        resolver = action.resolver
        if resolver != None:
            resolver.resolve(action, moving, chosen_targets)
        else:
            super().resolve(action, moving, chosen_targets)
