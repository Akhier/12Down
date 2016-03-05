from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from S_RecursiveShadowCasting import Fov_RSC
from S_MakeMap import MapGen
import S_MapInfo as MapInfo
from Console import Console
from C_Coord import Coord
from C_Tile import Tile
from Panel import Panel
import libtcodpy
import config


gamewindow = Console(config.window_width, config.window_height,
                     config.window_title)
playscreen = Panel(config.playscreen_x, config.playscreen_y,
                   config.playscreen_width, config.playscreen_height)
messagescreen = Panel(config.messagescreen_x, config.messagescreen_y,
                      config.messagescreen_width, config.messagescreen_height,
                      border=True)
statscreen = Panel(config.statscreen_x, config.statscreen_y,
                   config.statscreen_width, config.statscreen_height,
                   border=True)
fov = Fov_RSC(config.playscreen_width, config.playscreen_height)
mapgen = MapGen(config.playscreen_width, config.playscreen_height)
mapid = mapgen.create(222)
testmap = CM.get_Component('Map', mapid)
mapseethrough = MapInfo.seethrough_map(mapid)
Player = EM.new_Id
CM.add_Component(Player, 'Tile', Tile('Player', '@', False, True))
CM.add_Component(Player, 'Coord', Coord(30, 20))
while not gamewindow.is_window_closed:
    playercoord = CM.get_Component('Coord', Player)
    fovmap = fov.Calculate_Sight(mapseethrough, playercoord.X,
                                 playercoord.Y, 100)
    for y in range(testmap.Height):
        for x in range(testmap.Width):
            checktile = CM.get_Component('Seen', testmap.TileIds[x][y])
            if fovmap[x][y] and not checktile.seen:
                checktile.seen = True
            if checktile.seen:
                tile = CM.get_Component('Tile', testmap.TileIds[x][y])
                playscreen.write(x, y, tile.Char)
    gamewindow.clear
    playscreen.blit()
    messagescreen.blit()
    statscreen.blit()
    player = CM.get_Component('Tile', Player)
    gamewindow.write(playercoord.X, playercoord.Y, player.Char)
    gamewindow.flush
    libtcodpy.console_wait_for_keypress(True)
