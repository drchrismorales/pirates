import random
import game.config as config
import game.crewmate as crew
import game.superclasses as superclasses
from game.context import Context
from game.display import announce
from game.display import menu

class Combat():

    def __init__ (self, monsters):
        self.monsters = monsters

    def process_verb (self, verb, cmd_list, nouns):
        print (self.nouns + " can't " + verb)

    def crewmateAction(self, attacker, allies, enemies):
        """The player chooses an action for a crewmate to take."""
        announce(attacker.get_name() + " has seized the initiative! What should they do?",pause=False)
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
                chosen_action = superclasses.CombatAction(chosen_attk.name, chosen_attk, None)
            #Resolve
            chosen_action.resolve(chosen_action, moving, chosen_targets)
            self.monsters = [m for m in self.monsters if m.health >0]
            config.the_player.cleanup_items()


class Monster(superclasses.CombatCritter):
    def __init__ (self, name: str, hp: int, attacks: dict[str, list], speed: float):
        super().__init__(name, hp, speed)
        self.attacks = attacks
        self.cur_move = 0

    def pickAttack(self):
        attacks = []
        for key in self.attacks.keys():
             attacks.append(superclasses.Attack(key, self.attacks[key][0], self.attacks[key][1], self.attacks[key][2], False))
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
