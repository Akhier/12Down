from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from C_Flags import ToLevel, Seen
from C_Coord import Coord
from C_Tile import Tile
import config
import Color


def create_stairs(dungeonlevelid):
    stairs = EM.new_Id()
    CM.add_Component(stairs, 'Tile', Tile('Stairs Down', '>', True,
                                          True, Color.map_tile_visible))
    CM.add_Component(stairs, 'Coord', Coord(config.playscreen_width / 2,
                                            config.playscreen_height / 2))
    CM.add_Component(stairs, 'ToLevel', ToLevel(2))
    CM.add_Component(stairs, 'Seen', Seen(seen=True))
    dungeonlevelid = config.DungeonLevelIds[config.CurrentDungeonLevel]
    firstlevel = CM.get_Component('DungeonLevel', dungeonlevelid)
    firstlevel.FeatureIds.append(stairs)
