
from re import I
from game.ship import *
from game.context import Context
import jsonpickle
from game.display import announce

class Player (Context):

    the_player = None

    def __init__ (self, world, ship):
        super().__init__()
        Player.the_player = self
        self.sight_range = 3
        self.name = 'Player'
        self.gameInProgress = True
        self.ship = ship
        self.world = world
        self.reporting = True
        self.go = False
        self.verbs['quit'] = self
        self.verbs['status'] = self
        self.verbs['go'] = self
        self.verbs['save'] = self
        self.verbs['load'] = self
        self.verbs['debug'] = self
        self.verbs['map'] = self

        self.seen = []
        for i in range (0, self.world.worldsize):
            self.seen.append ([])
            for j in range (0, self.world.worldsize):
                self.seen[i].append(False)


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "quit"):
            self.gameInProgress = False
            self.go = True
        elif (verb == "map"):
            self.print_map ()
        elif (verb == "debug"):
            announce ("home port is at:" + str(self.world.homex) + ", " + str(self.world.homey))
            self.world.print ()
        elif (verb == "save"):
            announce ("saving...", end="",pause=False)
            f = open ("save.json", "w")
            f.write (jsonpickle.encode (self))
            f.close()
            announce ("..done")
        elif (verb == "load"):
            with open ("save.json") as f:
                s = f.read()    
            Player.the_player = jsonpickle.decode (s)
            self.go = True
        elif (verb == "status"):
            self.print()
        elif (verb == "go"):
            self.go = True
            if (len(cmd_list) > 1):
                if (cmd_list[1] == "north"):
                    self.ship.process_verb ("north", cmd_list, nouns)
                elif (cmd_list[1] == "south"):
                    self.ship.process_verb ("south", cmd_list, nouns)
                elif (cmd_list[1] == "west"):
                    self.ship.process_verb ("west", cmd_list, nouns)
                elif (cmd_list[1] == "east"):
                    self.ship.process_verb ("east", cmd_list, nouns)
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

        if (cmd_list[0] in verbs.keys()):
            verbs[cmd_list[0]].process_verb (cmd_list[0], cmd_list, nouns)
        else:
            announce (" I did not understand that command of " + cmd_list[0])



    # get / process input
    def process_day(self):

        # update the player's map
        # get ships location and then look at the range around them
        ship_loc = self.ship.get_loc()
        x = ship_loc.get_x()
        y = ship_loc.get_y()
        for ix in range (x-self.sight_range, x+self.sight_range):
            for iy in range (y-self.sight_range, y+self.sight_range):
                if ((ix >=0) and (ix < self.world.worldsize) and (iy >=0) and (iy < self.world.worldsize)):
                    self.seen[ix][iy] = True

        self.go = False

        if (self.reporting):
            announce ("Captain's Log: Day " + str(self.world.get_day()),pause=False)
            announce ("The ship is at location ", end="",pause=False)
            loc = self.ship.get_loc()
            announce (str(loc.get_x()) + ", " + str(loc.get_y()),pause=False)
            announce ("Food stores are at: " + str (self.ship.get_food()),pause=False)
            self.ship.print ()

        if (self.ship.get_food()<0):
            self.gameInProgress = False
            announce (" everyone starved!!!!!!!!!! ")
            return

        
        while (self.go == False):
            Player.get_interaction ([self, self.ship])


    def notdone (self):
        return self.gameInProgress

    def times_up (self):
        self.gameInProgress = False

    def print (self):
        self.ship.print()

    def get_ship (self):
        return self.ship

    def get_world(self):
        return self.world

    def print_map (self):
        ship_loc = self.ship.get_loc()
        for x in range (0, self.world.worldsize):
            for y in range (0, self.world.worldsize):
                if (self.world.locs[x][y] == ship_loc):
                    print ("S", end="")
                elif (self.seen[x][y]):
                    print (self.world.locs[x][y].get_symbol(), end="")
                else:
                    print ("?", end="")
            print ()

