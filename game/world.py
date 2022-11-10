
from game.location import *
from game.locations import *
from game.events import *
from game.ship import *
from game.context import Context
from game.display import announce
import game.config as config

import random

class World (Context):

    worldsize = 25
    startx = 12
    starty = 12
    num_islands = 8

    def __init__ (self, s):
        super().__init__()
        self.ship = s
        self.day = 0
        self.locs = []
        for i in range (0, World.worldsize):
            self.locs.append([])
            for j in range (0, World.worldsize):
                self.locs[i].append(Location(i, j, self))

        self.homex = random.randrange (1,World.worldsize-2)
        self.homey = random.randrange (1,World.worldsize-2)
        self.locs[self.homex][self.homey] = homeport.HomePort (self.homex, self.homey, self)

        i = 0
        while (i < World.num_islands):
            x = random.randrange (1, World.worldsize - 2)
            y = random.randrange (1, World.worldsize - 2)
            if (self.locs[x][y].name == "ocean"):
                self.locs[x][y] = island.Island (x, y, self)
                i = i + 1

        whirl = whirlpool.Whirlpool (self.startx + 1, self.starty, self)
        self.locs[self.startx+1][self.starty] = whirl

        self.events = []
        self.events.append (lucky.LuckyDay())
        self.events.append (nothing.Nothing())
        self.events.append (seagull.Seagull())
        self.events.append (seagull.Seagull())
        self.events.append (seagull.Seagull())
        self.events.append (sickness.Sickness())
        self.nouns["world"] = self

    def get_day (self):
        return self.day

    def start_day (self):
        self.day = self.day + 1
#        announce ("starting day " + str(self.day))
        
        if self.day > 1:
            num_events = random.randint (0,2)
            random.shuffle (self.events)
            for i in range (0, num_events):
                today_event = self.events.pop()
                announce ("----------------------",pause=False)
                results = today_event.process (self)
                announce (results["message"])
                for e in results["newevents"]:
                    self.events.append(e)
                announce ("----------------------",pause=False)
        
        # ship knows where it is
        action = self.ship.start_day(self)
        for i in range (0, World.worldsize):
            for j in range (0, World.worldsize):
                self.locs[i][j].start_day()


    def end_day (self):
#        announce ("ending day " + str(self.day))
        
        # ship knows where it is
        action = self.ship.end_day(self)
        for i in range (0, World.worldsize):
            for j in range (0, World.worldsize):
                self.locs[i][j].end_day()

    def get_startloc (self):
        return self.locs[World.startx][World.starty]

    def get_loc (self, x, y):
        return self.locs[x][y]

    def get_ship (self):
        return self.ship


    def print (self):
        ship_loc = self.ship.get_loc()
        for i in range (0, World.worldsize):
            for j in range (0, World.worldsize):
                l = self.locs[i][j]
                if (l == ship_loc):
                    print ("S", end="")
                else:
                    print (self.locs[i][j].get_symbol(), end="")
            print ()