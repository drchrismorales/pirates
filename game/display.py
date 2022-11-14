
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

def menu(options):
    #if(the_display != None):
    #   display stuff
    #else:
    chosen = -1
    while chosen < 0 or chosen >= len(options):
        menuletters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(len(options)):
            if i >= len(menuletters):
                print ("too many options :(")
                break
            print (menuletters[i] + " - " + options[i])
        o = input("Choose: ")
        chosen = menuletters.find(o)
    return chosen
