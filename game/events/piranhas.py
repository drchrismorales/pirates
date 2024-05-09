from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class EthanPiranha (Context, event.Event):
    '''Encounter with jumping piranhas. Uses the parser to decide what to do about it.'''
    def __init__(self):
        super().__init__()
        self.name = "piranha visitor"
        self.piranhas = random.randint(1,5)
        self.verbs['kick'] = self
        self.verbs['help'] = self
        self.result = {}
        self.go = False

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "kick"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "the piranhas are kicked off."
                if (self.piranhas > 1):
                    self.piranhas = self.piranhas - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "luckily, the piranhas are kicked off."
                else:
                    self.result["message"] = c.get_name() + " is hurt by the piranhas."
                    if (c.inflict_damage(self.piranhas, "Hurt by piranhas")):
                        self.result["message"] = ".. " + c.get_name() + " is hurt by the piranhas!"

        elif (verb == "help"):
            print("the piranhas will pester you until you kick them off")
            self.go = False
        else:
            print("it seems the only option here is to kick")
            self.go = False

    def process(self, world):
        self.go = False
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = "default message"

        while (self.go == False):
            print(str(self.piranhas) + " piranhas have jumped onto the ship, what do you want to do?")
            Player.get_interaction([self])

        return self.result