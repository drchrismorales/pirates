from game import event

class Nothing (event.Event):
    '''Some padding for ship-board events. Does nothing but print a message about nothing happening, then adds itself to the new events result'''

    def __init__ (self):
        self.name = " nothing happened"

    def process (self, world):
        result = {}
        result["message"] = "nothing happened"
        result["newevents"] = [ self ]
        return result
