from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
import S_MapInfo as MapInfo
from C_Coord import Coord
from C_Tile import Tile
import libtcodpy
import config


mapid = config.mapgen.create(222)
testmap = CM.get_Component('Map', mapid)
mapseethrough = MapInfo.seethrough_map(mapid)
Player = EM.new_Id
CM.add_Component(Player, 'Tile', Tile('Player', '@', False, True))
CM.add_Component(Player, 'Coord', Coord(30, 20))
while not config.gamewindow.is_window_closed:
    playercoord = CM.get_Component('Coord', Player)
    fovmap = config.fov.Calculate_Sight(mapseethrough, playercoord.X,
                                        playercoord.Y, 100)
    for y in range(testmap.Height):
        for x in range(testmap.Width):
            checktile = CM.get_Component('Seen', testmap.TileIds[x][y])
            if fovmap[x][y] and not checktile.seen:
                checktile.seen = True
            if checktile.seen:
                tile = CM.get_Component('Tile', testmap.TileIds[x][y])
                config.playscreen.write(x, y, tile.Char)
    config.gamewindow.clear
    config.playscreen.blit()
    config.messagescreen.blit()
    config.statscreen.blit()
    player = CM.get_Component('Tile', Player)
    config.gamewindow.write(playercoord.X, playercoord.Y, player.Char)
    config.gamewindow.flush
    libtcodpy.console_wait_for_keypress(True)
