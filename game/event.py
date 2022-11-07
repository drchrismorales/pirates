
# define the interface to events

class Event:

    def __init__(self):
        self.name = "default event"

    def process (self, world):
        return {}
