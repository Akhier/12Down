from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from C_DungeonLevel import DungeonLevel
from C_Creature import Creature
from Message import Message
from C_Coord import Coord
from C_Flags import Level
from C_Tile import Tile
import config
import Color


def New_Game():
    EM.Id = []
    CM.Component = {}
    config.DungeonLevelIds = []
    config.CurrentDungeonLevel = 1
    config.PlayerId = EM.new_Id()
    config.fov_recompute = True
    config.game_msg = []
    config.game_state = 'playing'
    config.xptolevel = 66.6
    CM.add_Component(config.PlayerId, 'Tile', Tile('Player', '@', False,
                                                   True, Color.sky))
    CM.add_Component(config.PlayerId, 'Coord',
                     Coord(config.playscreen_width / 2,
                           config.playscreen_height / 2))
    CM.add_Component(config.PlayerId, 'Creature', Creature(10, 0, 10,
                                                           10, 0, 6))
    CM.add_Component(config.PlayerId, 'Level', Level())
    firstlevelid = EM.new_Id()
    mapid = config.mapgen.create(firstlevelid)
    config.DungeonLevelIds.append(firstlevelid)
    firstlevel = DungeonLevel(1, mapid)
    CM.add_Component(firstlevelid, 'DungeonLevel', firstlevel)
    Message('Welcome young adventurer! You have just entered my dungeon and' +
            ' through my deal with the adventurers guild you may explore my' +
            ' first 26 levels! Though of course everything will still try to' +
            ' kill you but atleast once finish there is an easy passage out!',
            Color.red)
