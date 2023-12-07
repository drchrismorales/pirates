from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
from game.player import Player
from game.combat import *
from game.events import guardian
from game.events import Boss

class Dylan(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "enchanted island"
        self.symbol = 'E'  # Symbol for the map
        self.visitable = True
        self.locations = {}
        self.locations["mystic_cave"] = MysticCave(self)
        self.locations["riddle_lake"] = RiddleLake(self)
        self.locations["gateway"] = Gateway(self)
        self.locations["final_battle"] = FinalBattle(self)
        self.locations["moisty_mires"] = Moistymire(self)

        self.starting_location = self.locations["mystic_cave"]

    def enter(self, ship):
        announce("You approach an enchanted island surrounded by mystical energy.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

#For reference: (Mystic Cave and Riddle Lake)
class MysticCave(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "mystic_cave"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.event_chance = 10
        self.events.append(guardian.EnchantedGuardian())

    def cipher(self, text, shift,):
        encrypted_text = ""

        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                shifted_char = chr((ord(char) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))
                encrypted_text += shifted_char
            else:
                encrypted_text += char

        return encrypted_text

    def enter(self):
        announce("You arrive at the entrance of a mystic cave. Strange symbols glow on the cave walls.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif verb == "north":
            config.the_player.next_loc = self.main_location.locations["gateway"]
        elif verb == "east":
            config.the_player.next_loc = self.main_location.locations["riddle_lake"]
        elif verb == "west":
            config.the_player.next_loc = self.main_location.locations["moisty_mires"]
        elif verb == "inspect":
            announce("You see ancient writings on the cave walls and a mysterious aura.")
            res = input("What would you like to inspect further?\n:")
            if res == "writings":
                encrypted_message = self.cipher("seek the heart of the labyrinth", 5)
                announce("You decipher the writings.\n" + encrypted_message +"\nseek the heart of the labyrinth")
            else:
                announce("That doesn't seem to be here.")

class RiddleLake(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "riddle_lake"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.verbs["take"] = self
        self.item_in_lake = EnchantedKey()
        self.event_chance = 30
        self.events.append(guardian.EnchantedGuardian())

    def cipher(self, text, shift):
        encrypted_text = ""

        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                shifted_char = chr((ord(char) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))
                encrypted_text += shifted_char
            else:
                encrypted_text += char

        return encrypted_text

    def enter(self):
        announce("You stand beside a serene lake surrounded by riddles.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["mystic_cave"]
        elif verb in ["north", "east", "west"]:
            announce("You can't proceed in that direction. The lake is in your way.")
        elif verb == "inspect":
            announce("You see riddles written on large stones surrounding the lake.")
            res = input("What would you like to inspect further?\n:")
            if res == "riddles":
                em = self.cipher("I have keys but no locks, i have space but no room, you csn enter, but you can't go inside what am I.", 5)
                ress = input(em + "\n")
                if ress == "Keyboard":
                    if self.item_in_lake != None:
                        announce("You reach into the lake and find an enchanted key.")
                        config.the_player.add_to_inventory(EnchantedKey().as_list())
                        self.item_in_lake = None
                        config.the_player.go = True
            else:
                announce("That doesn't seem to be here.")
        else:
            announce("That doesn't seem to be here.") 

# This is where I add EnchantedKey class
class EnchantedKey(items.Item):
    def __init__(self):
        super().__init__("Enchanted Key", 1)
       

    def as_list(self):
        return [self]



class Moistymire(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "moisty_mires"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.verbs["take"] = self
        self.item_in_lake = EnchantedKey()
        self.event_chance = 30
        self.events.append(guardian.EnchantedGuardian())

    def cipher(self, text, shift):
        encrypted_text = ""

        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                shifted_char = chr((ord(char) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))
                encrypted_text += shifted_char
            else:
                encrypted_text += char

        return encrypted_text
    def enter(self):
        announce("You stand beside a serene lake surrounded by riddles.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["mystic_cave"]
        elif verb in ["north", "east", "west"]:
            announce("You can't proceed in that direction. The moisty mire is in your way.")
        elif verb == "inspect":
            announce("You see riddles written on large stones surrounding the swamp.")
            res = input("What would you like to inspect further?\n:")
            if res == "riddles":
                announce("The riddles challenge your intellect, but solving them may reveal hidden truths.")
                em = self.cipher("Im always near the waters flow, with a bright hue that seems to glow. I rise and fall, but never leave, what am I.\n", 5)
                ress = input(em)
                if ress == "Wave":
                    if self.item_in_lake is not None:
                        announce("You reach into the swamp and find an enchanted key.")
                        config.the_player.add_to_inventory(EnchantedKey().as_list())
                        self.item_in_lake = None
                        config.the_player.go = True
            else:
                announce("That doesn't seem to be here.")
        else:
            announce("The lake holds no more secrets.")
class Gateway(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "gateway"
        self.portal_color = "shimmering blue"
        self.puzzle_difficulty = "intricate"
        self.guardian_present = True
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.portal_color = "shimmering blue"
        self.directions = {"north": None, "south": None, "east": None, "west": None}



    def enter(self):
        announce("You stand before a mystical gateway shimmering with energy.")

    def process_verb(self, verb, cmd_list, nouns):
        self.portal_active = True
        self.energy_surge = False  
        self.teleportation_count = 0  


        if verb == "inspect":
            announce("You see a huge door")
            res = input ("what would you like to inspect further\n")
            if res == "door":
                announce("you walk up to the door and see a key hole.")
                has_key = any(isinstance(item, EnchantedKey) for item in config.the_player.inventory)
                

                if has_key:


                    aa = input('would you like to insert your key?\n')
                    if aa == 'yes':
                        announce("The door has opened")
                        aaa = input('would you like to enter?\n')
                        if aaa == 'yes':
                            config.the_player.go = True
                            config.the_player.next_loc = self.main_location.locations["final_battle"]

                    else:
                        announce('You feel a greater power laughing at your lack of courage')
                else:
                    announce('You hear a voice saying you are not ready yet')

#This is where I will add my FinalBattle class implementation
class FinalBattle(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "final_battle"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["inspect"] = self
        self.event_chance = 100
        self.events.append(Boss.FinalBossFight())
        self.item_in_final_battle = UltimateSword()

    def enter(self):
        announce("You have reached the final battleground. A formidable enemy awaits.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            announce("You strategically retreat to gather your strength.")
            config.the_player.next_loc = self.main_location.locations["gateway"]
        elif verb in ["north", "east", "west"]:
            announce("You encounter magical barriers preventing you from going that way.")
        elif verb == "inspect":
            announce("You see the final boss menacingly glaring at you.")
            res = input("What would you like to inspect further?\n:")
            if res == "boss":
                if self.item_in_final_battle is not None:
                    announce("You bravely approach the boss and discover an ultimate sword.")
                    aa = input('Would you like to take it?\n')
                    if aa == 'yes':
                        announce('You wield the ultimate sword, empowering your attacks.')
                        config.the_player.add_to_inventory(UltimateSword().as_list())
                        self.item_in_final_battle = None
                        config.the_player.go = True
                    else:
                        announce('You decide to face the boss without the ultimate sword.')
                        config.the_player.go = True
                else:
                    announce('There is nothing more to find on the boss.')
            else:
                announce("That doesn't seem to be here.")



#This is where Im emplementing my ultimate weapon, which is a sword
class UltimateSword(items.Item):
    def __init__(self):
        super().__init__("Ultimate Sword", 10)
        self.damage = (60, 80)
        self.skill = "swords"
        self.verb = "strike"
        self.verb2 = "strikes"

    def as_list(self):
        return [self]
