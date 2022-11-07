
the_display = None

class Display ():
    pass

def announce(announcement, end='\n', pause = True):
    #if(the_display != None):
    #   display stuff
    #else:
    if(pause):
        input (announcement)
    else:
        print (announcement, end)
