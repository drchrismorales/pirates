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

class ActionResolver():
    def pickTargets(self, action, attacker, allies, enemies):
        """The player should pick targets"""
        options = []
        for t in enemies:
            options.append("attack " + t.get_name())
        choice = menu (options)
        return [enemies[choice]]

    def resolve(self, action, moving, chosen_targets):
        chosen_attk = action.attack
        for chosen_target in chosen_targets:
            if chosen_target != None:
                roll = random.randrange(100)
                if moving.isLucky() == True:
                    roll = min(roll, random.randrange(100))
                if roll < chosen_attk.success:
                    announce (moving.get_name() + " " + chosen_attk.description + " " + chosen_target.get_name() + "!")
                    damage = random.randrange(chosen_attk.damage_range[0],chosen_attk.damage_range[1]+1)
                    deathcause = "slain by a " + moving.get_name() + "'s " + chosen_attk.name
                    chosen_target.inflict_damage(damage, deathcause)
                    if chosen_target.health <= 0:
                        announce (chosen_target.get_name() + " is killed!")
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

    def get_name(self):
        return self.name

    def isLucky(self):
        return self.lucky

    def inflict_damage (self, num, deathcause):
        self.health = self.health - num
        if(self.health > 0):
            return False
        return True

    def getAttacks(self):
        return []

class CombatAction(ActionResolver):
    """A more sophisticated combat action object, with a name, Attack instance, and Item instance. Resolves all combat actions. Used for monster attacks, but the added complexity over Attack alone is meant for player actions."""
    def __init__ (self, name, attack, resolver):
        self.name = name
        self.attack = attack
        self.resolver = resolver

    def __str__ (self):
        """To-string uses the Action's listed name"""
        return self.name

    def __eq__ (self, other):
        """Test-equals compares the two CombatActions' Attacks"""
        if not isinstance(other, CombatAction):
            return False
        return self.attack == other.attack

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
