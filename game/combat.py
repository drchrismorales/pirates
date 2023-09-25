import random
import game.config as config
import game.crewmate as crew
from game.display import announce
from game.display import menu
from game.context import Context

class Attack():
    """Basic attack object, with a name, description, chance of success, and damage range. Sufficient for specifying monster attacks."""
    def __init__ (self, name, description, success, damage_range):
        self.name = name
        self.description = description
        self.success = success
        self.damage_range = damage_range

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
            options.append("attack " + t.getName())
        choice = menu (options)
        return [enemies[choice]]

    def resolve(self, action, moving, chosen_targets):
        chosen_attk = action.attack
        for chosen_target in chosen_targets:
            if chosen_target != None:
                roll = random.randrange(100)
                if moving.lucky == True:
                    roll = min(roll, random.randrange(100))
                if roll < chosen_attk.success:
                    announce (moving.getName() + " " + chosen_attk.description + " " + chosen_target.getName() + "!")
                    damage = random.randrange(chosen_attk.damage_range[0],chosen_attk.damage_range[1]+1)
                    deathcause = "slain by a " + moving.getName() + "'s " + chosen_attk.name
                    chosen_target.inflict_damage(damage, deathcause)
                    if chosen_target.health <= 0:
                        announce (chosen_target.getName() + " is killed!")
                elif (roll == chosen_attk.success):
                    announce (moving.getName() + " barely misses " + chosen_target.getName() + "!")
                else:
                    announce (moving.getName() + " misses " + chosen_target.getName() + ".")

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

class Combat():

    def __init__ (self, monsters):
        self.monsters = monsters

    def process_verb (self, verb, cmd_list, nouns):
        print (self.nouns + " can't " + verb)

    def crewmateAction(self, attacker, allies, enemies):
        """The player chooses an action for a crewmate to take."""
        announce(attacker.getName() + " has seized the initiative! What should they do?",pause=False)
        actions = attacker.getAttacks()
        # actions = attacker.getMiscActions()
        if len(actions) > 0:
            choice = menu (actions)
            return actions[choice]
        #else: run in circles, scream and shout
        return None

    def combat (self):
        while len(self.monsters):
            combatants = config.the_player.get_pirates() + self.monsters
            min_t = None
            for c in combatants:
                t = (100 - c.cur_move)/c.speed
                if min_t == None:
                    min_t = t
                else:
                    min_t = min(t, min_t)
            for c in combatants:
                c.cur_move += c.speed*min_t
            speeds = [c.cur_move for c in combatants]
            max_move = max(speeds)
            ready = [c for c in combatants if c.cur_move == max_move]
            moving = random.choice(ready)
            moving.cur_move = 0
            if isinstance(moving, crew.CrewMate):
                chosen_action = self.crewmateAction(moving, config.the_player.get_pirates(), self.monsters)
                if(chosen_action != None):
                    chosen_targets = chosen_action.pickTargets(chosen_action, moving, config.the_player.get_pirates(), self.monsters)
            else:
                chosen_targets = [random.choice(config.the_player.get_pirates())]
                chosen_attk = moving.pickAttack()
                chosen_action = CombatAction(chosen_attk.name, chosen_attk, None)
            #Resolve
            chosen_action.resolve(chosen_action, moving, chosen_targets)
            self.monsters = [m for m in self.monsters if m.health >0]
            config.the_player.cleanup_items()


class Monster:
    def __init__ (self, name, hp, attacks, speed):
        self.name = name
        self.health = hp
        self.attacks = attacks
        self.speed = speed
        self.cur_move = 0
        self.lucky = False

    def inflict_damage (self, num, deathcause):
        self.health = self.health - num
        if(self.health > 0):
            return False
        return True

    def getName(self):
        return self.name

    def pickAttack(self):
        attacks = []
        for key in self.attacks.keys():
             attacks.append(Attack(key, self.attacks[key][0], self.attacks[key][1], self.attacks[key][2]))
        return random.choice(attacks)

class Macaque(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))

class Drowned(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(35,51), (5,15)]
        attacks["punch 1"] = ["punches",random.randrange(35,51), (1,10)]
        attacks["punch 2"] = ["punches",random.randrange(35,51), (1,10)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))
