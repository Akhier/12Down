from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from C_DungeonLevel import DungeonLevel
from Message import Message
from C_Coord import Coord
from C_Tile import Tile
import config
import Color


def New_Game():
    config.Id = []
    config.Component = {}
    config.DungeonLevelIds = []
    config.PlayerId = EM.new_Id()
    config.game_msg = []
    CM.add_Component(config.PlayerId, 'Tile', Tile('Player', '@', False, True))
    CM.add_Component(config.PlayerId, 'Coord', Coord(-1, -1))
    firstlevelid = EM.new_Id()
    CM.add_Component(firstlevelid, 'Map', config.mapgen.create(firstlevelid))
    config.DungeonLevelIds.append(firstlevelid)
    firstlevel = DungeonLevel(1)
    CM.add_Component(firstlevelid, 'DungeonLevel', firstlevel)
    Message('Welcome young adventurer! You have just entered my dungeon and' +
            ' through my deal with the adventurers guild you may explore my' +
            ' first 26 levels! Though of course everything will still try to' +
            ' kill you but atleast once finish there is an easy passage out!',
            Color.red)
