from game.context import Context
from game import config
from game.display import *
import random

class Location:
    '''A map location. May own explorable sub-locations'''
    symbols = [' ', '*', '-']

    def __init__(self, x, y, w) -> None:
        self.x = x
        self.y = y
        self.world = w
        self.symbol = ' '
        self.name = 'ocean'
        #by default, not visitable
        self.visitable = False
        self.go = True
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

    def get_symbol(self):
        return self.symbol

    def enter(self, ship):
        pass
    def start_day(self):
        pass
    def end_day(self):
        pass

    def visit(self):
        '''main loop governing exploration of an island'''
        config.the_player.visiting = True
        while config.the_player.visiting:
            self.start_turn ()
            self.process_turn ()
            self.end_turn ()
        #Reset to default after visit
        config.the_player.location = config.the_player.ship
        config.the_player.next_loc = None

    def start_turn(self):
        for crew in config.the_player.get_pirates():
            crew.start_turn ()
        config.the_player.location.start_turn()

    def process_turn(self):
        config.the_player.go = False
        for crew in config.the_player.get_pirates():
            crew.print()
        while (config.the_player.go == False):
            config.the_player.get_interaction ([config.the_player, config.the_player.location])

    def end_turn(self):
        if config.the_player.next_loc != None:
            config.the_player.location = config.the_player.next_loc
        config.the_player.location.enter()
        config.the_player.next_loc = None

class SubLocation(Context):
    '''The explorable locations owned by a map Location that can be visited.'''

    def __init__(self, m):
        super().__init__()
        self.main_location = m
        self.name = 'room'
        #The chance an event triggers in this sub-location
        self.event_chance = 0
        #The events that may occur in this sub-location
        self.events = []
    
    def start_turn(self):
        #Maybe draw an event (if there are events and the event chance is rolled)
        if len(self.events) > 0 and self.event_chance > random.randrange(100):
            random.shuffle (self.events)
            today_event = self.events.pop()
            announce ("----------------------",pause=False)
            results = today_event.process (self)
            announce (results["message"])
            for e in results["newevents"]:
                self.events.append(e)
            announce ("----------------------",pause=False)
    
