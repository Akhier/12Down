from ComponentManager import ComponentManager as CM
from S_MakeMap import MapGen
from Console import Console
from Panel import Panel
import libtcodpy
import random


gamewindow = Console(80, 50, '26Down - By Akhier Dragonheart')
playscreen = Panel(0, 0, 60, 40, border=True)
messagescreen = Panel(0, 40, 60, 10, border=True)
statscreen = Panel(60, 0, 20, 50, border=True)
mapgen = MapGen(58, 38)
while not gamewindow.is_window_closed:
    testmap = CM.get_Component('Map', mapgen.create(random.random()))
    middle = CM.get_Component('Seen', testmap.TileIds[58 / 2][38 / 2])
    middle.seen = True
    for y in range(testmap.Height):
        for x in range(testmap.Width):
            checktile = CM.get_Component('Seen', testmap.TileIds[x][y])
            if checktile.seen:
                tile = CM.get_Component('Tile', testmap.TileIds[x][y])
                playscreen.write(x + 1, y + 1, tile.Char)
    gamewindow.clear
    playscreen.blit()
    messagescreen.blit()
    statscreen.blit()
    gamewindow.flush
    libtcodpy.console_wait_for_keypress(True)
