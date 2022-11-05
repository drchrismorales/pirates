#!/usr/bin/env python3

# player - controlling a ship
#    ship is lost at sea, trying to return home
#         - dangers and opportunities
#         - crew, crew's health

from game import *

ship_v     = ship.Ship()
world_v    = world.World (ship_v)
start_loc  = world_v.get_startloc()
ship_v.set_loc (start_loc)

player_v   = player.Player(world_v, ship_v)

while (player.Player.the_player.notdone()):
	player.Player.the_player.get_world().start_day ()
	player.Player.the_player.process_day()
	player.Player.the_player.get_world().end_day ()

# world_v.print()