
from re import I
from game.ship import *
from game.context import Context
import jsonpickle
from game.display import announce
import game.config as config
from game.items import *
import sys
import datetime

class Player (Context):

    def __init__ (self, world, ship):
        super().__init__()
        config.the_player = self
        self.sight_range = 2
        self.name = 'Player'
        self.gameInProgress = True
        self.ship = ship
        self.world = world
        self.location = ship
        self.next_loc = None
        self.visiting = False
        self.reporting = True
        self.go = False
        self.pirates = []
        self.piscine_dormitory = []
        self.CHARGE_SIZE = 128
        self.powder = self.CHARGE_SIZE*random.randrange(3,7)
        self.inventory = []
        n = random.randrange(2,6)
        for i in range (0,n):
            if random.randrange(0,10) == 0:
                itm = Flintlock()
            else:
                itm = Cutlass()
            self.inventory.append(itm)
        self.inventory.sort()

        n = random.randrange(3,7)
        for i in range (0,n):
            c = CrewMate()
            self.pirates.append (c)
            self.nouns[c.get_name()] = c

        self.verbs['quit'] = self
        self.verbs['status'] = self
        self.verbs['go'] = self
        self.verbs['save'] = self
        self.verbs['load'] = self
        self.verbs['debug'] = self
        self.verbs['map'] = self
        self.verbs['inventory'] = self
        self.verbs['restock'] = self

        self.seen = []
        for i in range (0, self.world.worldsize):
            self.seen.append ([])
            for j in range (0, self.world.worldsize):
                self.seen[i].append(False)


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "quit"):
            sys.exit(0)
        elif (verb == "map"):
            self.print_map ()
        elif (verb == "inventory"):
            self.print_inventory ()
        elif (verb == "debug"):
            announce ("home port is at:" + str(self.world.homex) + ", " + str(self.world.homey))
            self.world.print ()
        elif (verb == "restock"):
            if config.the_player.location != config.the_player.ship:
                announce ("Powder and shot can only be restocked on the ship!")
            else:
                for c in self.get_pirates():
                    c.restock()
        elif (verb == "save"):
            if "jsonpickle" not in sys.modules:
                announce ("jsonpickle hasn't be imported. Saving is impossible.")
            elif self.location != self.ship:
                announce ("Saving is only possible abord ship.")
            else:
                announce ("saving...", end="",pause=False)
                f = open ("save.json", "w")
                f.write (jsonpickle.encode (self))
                f.close()
                announce ("..done")
        elif (verb == "load"):
            if "jsonpickle" not in sys.modules:
                announce ("jsonpickle hasn't be imported. Loading is impossible.")
            elif self.location != self.ship:
                announce ("Loading is only possible abord ship.")
            else:
                with open ("save.json") as f:
                    s = f.read()    
                config.the_player = jsonpickle.decode (s)
                self.go = True
        elif (verb == "status"):
            self.print()
        elif (verb == "go"):
            self.go = True
            if (len(cmd_list) > 1):
                if (cmd_list[1] == "north"):
                    self.location.process_verb ("north", cmd_list, nouns)
                elif (cmd_list[1] == "south"):
                    self.location.process_verb ("south", cmd_list, nouns)
                elif (cmd_list[1] == "west"):
                    self.location.process_verb ("west", cmd_list, nouns)
                elif (cmd_list[1] == "east"):
                    self.location.process_verb ("east", cmd_list, nouns)
                elif (cmd_list[1] == "ashore" and self.location == self.ship):
                    if self.ship.get_loc ().visitable == True:
                        self.ship.process_verb ("anchor", cmd_list, nouns)
                        self.ship.get_loc ().visit()
                    else:
                        announce("There's nowhere to go ashore.")
                        self.go = False
        else:
            announce ("Error: Player object does not understand verb " + verb)
            pass

    @staticmethod
    def get_interaction (contexts):
        # look at all of the the contexts and find the verbs and nouns
        # that make sense in this context 
        # and then dispatch an action that is identified

        verbs = {}
        nouns = {}
        for c in contexts:
            for k, v in c.verbs.items():
                verbs[k] = v

        for c in contexts:
            for k, v in c.nouns.items():
                nouns[k] = v

        cmd = input ("what is your command: ")
        cmd_list = cmd.split()   # split on whitespace

        if(len(cmd_list) > 0):
            if (cmd_list[0] in verbs.keys()):
                verbs[cmd_list[0]].process_verb (cmd_list[0], cmd_list, nouns)
            elif len(cmd_list) > 1 and (cmd_list[0] in nouns.keys()):
                nouns[cmd_list[0]].process_verb (cmd_list[1], cmd_list[1:], nouns)
            else:
                announce (" I did not understand that command of " + cmd_list[0])



    # get / process input
    def process_day(self):

        # update the player's map
        # get ships location and then look at the range around them
        ship_loc = self.ship.get_loc()
        x = ship_loc.get_x()
        y = ship_loc.get_y()
        for ix in range (x-self.sight_range, x+self.sight_range+1):
            for iy in range (y-self.sight_range, y+self.sight_range+1):
                if ((ix >=0) and (ix < self.world.worldsize) and (iy >=0) and (iy < self.world.worldsize)):
                    self.seen[ix][iy] = True

        self.go = False

        if (self.reporting):
            announce ("Captain's Log: Day " + str(self.world.get_day()),pause=False)
            announce ("The ship is at location ", end="",pause=False)
            loc = self.ship.get_loc()
            announce (str(loc.get_x()) + ", " + str(loc.get_y()),pause=False)
            announce ("Food stores are at: " + str (self.ship.get_food()),pause=False)
            announce ("Powder stores are at: " + str (self.powder//self.CHARGE_SIZE) + " cannon " + str (self.powder%self.CHARGE_SIZE) + " sidearm",pause=False)
            self.ship.print ()
            for crew in self.get_pirates():
                crew.print()

        if (self.ship.get_food()<0):
            self.gameInProgress = False
            announce (" everyone starved!!!!!!!!!!")
            config.the_player.kill_all_pirates("died of sudden-onset starvation")
            return

        
        while (self.go == False):
            Player.get_interaction ([self, self.ship])


    def notdone (self):
        self.cleanup_pirates ()
        return self.gameInProgress

    def times_up (self):
        self.gameInProgress = False

    def print (self):
        self.ship.print()
        for crew in self.get_pirates():
            crew.print()
        for crew in self.get_pirates():
            crew.print()


    def get_ship (self):
        return self.ship

    def get_world(self):
        return self.world

    def get_pirates (self):
        live_pirates = [p for p in self.pirates if p.health > 0]
        if len(live_pirates) <= 0 and self.gameInProgress == True:
            self.cleanup_pirates() #calls game over
        return live_pirates

    def cleanup_pirates (self):
        i = 0
        recovery_possible = True
        #avoid endless recursion between get pirates and cleanup pirates
        live_pirates = [p for p in self.pirates if p.health > 0]
        if len(live_pirates) <= 0:
            recovery_possible = False

        while i < len(self.pirates):
            if (self.pirates[i].health <= 0):
                deader = self.pirates.pop(i)
                self.add_to_inventory(deader.items)
                deader.items = []
                self.piscine_dormitory.append(deader)
            else:
                i = i + 1
        if (len(self.pirates) <= 0):
            announce (" everyone died!!!!!!!!!!")
            Player.game_over()

    def kill_all_pirates (self, deathcause):
        announce (" everyone died!!!!!!!!!!")
        while len(self.pirates) > 0:
            deader = self.pirates.pop()
            if(deader.death_cause == ""):
                deader.death_cause = deathcause
            self.add_to_inventory(deader.items)
            deader.items = []
            self.piscine_dormitory.append(deader)
        Player.game_over()

    def add_to_inventory (self, invList):
        self.inventory = self.inventory + invList
        self.inventory.sort()

    def print_map (self):
        ship_loc = self.ship.get_loc()
        for y in range (0, self.world.worldsize):
            for x in range (0, self.world.worldsize):
                if (self.world.locs[x][y] == ship_loc):
                    print ("S", end="")
                elif (self.seen[x][y]):
                    print (self.world.locs[x][y].get_symbol(), end="")
                else:
                    print ("?", end="")
            print ()

    def print_inventory (self):
        for i in self.inventory:
            print (i)
        print ()

    @staticmethod
    def game_over ():
        config.the_player.gameInProgress = False
        #open high score
        Player.record_score()
        sys.exit(0)

    @staticmethod
    def record_score():
        f = open("scores.log", "a")
        now = datetime.datetime.now()
        score = 0
        multiplier = 1
        if len(config.the_player.pirates) <= 0:
            multiplier = .5 #living to spend it is half the fun.
        else:
            for c in config.the_player.pirates:
                score += c.health * 10
                config.the_player.add_to_inventory(c.items)
                c.items = []
        for t in config.the_player.inventory:
            score += t.value

        score = score*multiplier
        f.write(now.strftime("%A %B %d, %Y") + " " + str(score) + " points\n")
        for c in config.the_player.pirates:
            f.write(str(c) + "lived to tell the tale\n")
        for d in config.the_player.piscine_dormitory:
            f.write(str(d) + "\n")
        for i in config.the_player.inventory:
            f.write(str(i) + "\n")
        f.write("----------------------\n\n")
        
