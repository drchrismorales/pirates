
class Location:
    symbols = [' ', '*', '-']

    def __init__(self, x, y, w) -> None:
        self.x = x
        self.y = y
        self.world = w
        self.symbol = ' '
        self.name = 'ocean'
    
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
