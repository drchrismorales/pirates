
import game.location as location
from game.locations import *
from game.events import *
import game.ship as ship
import game.context as context
from game.display import announce
import game.config as config
import game.combat as Combat

import random

class World (context.Context):

    worldsize = 25
    startx = 12
    starty = 12

    def __init__ (self, s):
        super().__init__()
        self.ship = s
        self.day = 0
        self.locs = []
        for i in range (0, World.worldsize):
            self.locs.append([])
            for j in range (0, World.worldsize):
                self.locs[i].append(location.Location(i, j, self))

        self.homex = random.randrange (1,World.worldsize-2)
        self.homey = random.randrange (1,World.worldsize-2)
        #Home port can't be within a 4x4 square of the start location
        while (self.homey in range(self.starty-4, self.starty+5)) or (self.homex in range(self.startx-4, self.startx+5)):
            self.homex = random.randrange (1,World.worldsize-2)
            self.homey = random.randrange (1,World.worldsize-2)
        self.locs[self.homex][self.homey] = homeport.HomePort (self.homex, self.homey, self)

        #Add new islands to this list:
        island_list = [island.Island]
        for cur_island in island_list:
            placed = False
            while placed == False:
                x = random.randrange (1, World.worldsize - 2)
                y = random.randrange (1, World.worldsize - 2)
                #Islands can't be within a 2x2 square of the start location
                if (self.locs[x][y].name == "ocean") and ((y in range(self.starty-2, self.starty+3)) or (x in range(self.startx-2, self.startx+3))):
                    self.locs[x][y] = cur_island (x, y, self)
                    placed = True

        #The pirates apparently got lost in a whirlpool
        whirl = whirlpool.Whirlpool (self.startx + 1, self.starty, self)
        self.locs[self.startx+1][self.starty] = whirl

        #Test island: always start off next to a test island. Swap in your island to test yours.
        testland = MysteriousIsland.MysteriousIsland (self.startx, self.starty+1, self)
        #Dylan: testland = dylanisland.Dylan (self.startx, self.starty+1, self)
        self.locs[self.startx][self.starty+1] = testland

        # Peaceful island directly to the right of the spawning location.
        peacefulIsland = PeacefulIsland.PeacefulIsland(self.startx + 1, self.starty, self)
        self.locs[self.startx + 1][self.starty] = peacefulIsland

        self.events = []
        # self.events.append (lucky.LuckyDay())
        # self.events.append (nothing.Nothing())
        # self.events.append (seagull.Seagull())
        # self.events.append (seagull.Seagull())
        # self.events.append (seagull.Seagull())
        # self.events.append (sickness.Sickness())
        self.events.append (drowned_pirates.DrownedPirates())
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
        # The World is... toroidal, actually.
        #  Modulo operator causes the world to loop from bottom to top and right to left
        #  Python negative index handling causes it to loop the other way too.
        x = x%World.worldsize
        y = y%World.worldsize
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
