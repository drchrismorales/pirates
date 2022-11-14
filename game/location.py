from game.context import Context
from game import config

class Location:
    symbols = [' ', '*', '-']

    def __init__(self, x, y, w) -> None:
        self.x = x
        self.y = y
        self.world = w
        self.symbol = ' '
        self.name = 'ocean'
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
        config.the_player.visiting = True
        while config.the_player.visiting:
            self.start_turn ()
            self.process_turn ()
            self.end_turn ()
        config.the_player.location = config.the_player.ship

    def start_turn(self):
        pass

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

    def __init__(self, m):
        super().__init__()
        self.main_location = m
        self.name = 'room'
        self.visitable = False
