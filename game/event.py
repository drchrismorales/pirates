
# define the interface to events

class Event:

    def __init__(self):
        self.name = "default event"
        print (" event created ")

    def process (self, world):
        return {}
