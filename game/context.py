
class Context:

    def __init__ (self):
        self.verbs = {}   # verb associated with a object
        self.nouns = {}   # in game name of an object

    def process_verb (self, verb, cmd_list, nouns):
        print (self.nouns + " can't " + verb)

