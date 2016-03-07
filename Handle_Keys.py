from ComponentManager import ComponentManager as CM
from S_PlaceMonsters import Place_Monsters_On_Level
from EntityManager import EntityManager as EM
from Enum_Direction import Direction as Dir
from S_MoveCreature import Walk_Direction
from C_DungeonLevel import DungeonLevel
from S_Combat import Attack_Coord
from Menu import Menu
import libtcodpy
import config


def Handle_Keys():
    if config.key.vk == libtcodpy.KEY_ENTER and config.key.lalt:
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    elif config.key.vk == libtcodpy.KEY_ESCAPE:
        return 'exit'

    playercoord = CM.get_Component('Coord', config.PlayerId)
    if config.game_state == 'playing':
        if config.key.vk == libtcodpy.KEY_UP or \
                config.key.vk == libtcodpy.KEY_KP8:
            if Walk_Direction(config.PlayerId, Dir.N):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.N))
        elif config.key.vk == libtcodpy.KEY_DOWN or \
                config.key.vk == libtcodpy.KEY_KP2:
            if Walk_Direction(config.PlayerId, Dir.S):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.S))
        elif config.key.vk == libtcodpy.KEY_LEFT or \
                config.key.vk == libtcodpy.KEY_KP4:
            if Walk_Direction(config.PlayerId, Dir.W):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.W))
        elif config.key.vk == libtcodpy.KEY_RIGHT or \
                config.key.vk == libtcodpy.KEY_KP6:
            if Walk_Direction(config.PlayerId, Dir.E):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.E))
        elif config.key.vk == libtcodpy.KEY_HOME or \
                config.key.vk == libtcodpy.KEY_KP7:
            if Walk_Direction(config.PlayerId, Dir.NW):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.NW))
        elif config.key.vk == libtcodpy.KEY_PAGEUP or \
                config.key.vk == libtcodpy.KEY_KP9:
            if Walk_Direction(config.PlayerId, Dir.NE):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.NE))
        elif config.key.vk == libtcodpy.KEY_END or \
                config.key.vk == libtcodpy.KEY_KP1:
            if Walk_Direction(config.PlayerId, Dir.SW):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.SW))
        elif config.key.vk == libtcodpy.KEY_PAGEDOWN or \
                config.key.vk == libtcodpy.KEY_KP3:
            if Walk_Direction(config.PlayerId, Dir.SE):
                config.fov_recompute = True
            else:
                Attack_Coord(config.PlayerAttack, config.PlayerId,
                             playercoord.get_coord_from_self(Dir.SE))
        elif config.key.vk == libtcodpy.KEY_KP5:
            pass

        else:
            key_char = chr(config.key.c)
            if key_char == '>':
                playercoord = CM.get_Component('Coord', config.PlayerId)
                curlevel = config.CurrentDungeonLevel
                leveldata = CM.get_Component('DungeonLevel',
                                             config.DungeonLevelIds[curlevel])
                coords = CM.dict_of('Coord')
                tolevels = CM.dict_of('ToLevel')
                for key, value in coords.iteritems():
                    if (value == playercoord and
                            key in tolevels and
                            key in leveldata.FeatureIds):
                        next_level()
                        config.fov_recompute = True
                        break
            return 'no action'


def msgbox(text, width=50):
    Menu(text, [], width)


def next_level():
    if config.CurrentDungeonLevel > 0:
        dungeonlevelid = config.DungeonLevelIds[config.CurrentDungeonLevel]
        dungeonlevel = CM.get_Component('DungeonLevel', dungeonlevelid)
        levelmap = CM.get_Component('Map', dungeonlevel.MapId)
        for key in dungeonlevel.MonsterIds:
            CM.cleanup(key)
        for lst in levelmap.TileIds:
            for key in lst:
                CM.cleanup(key)
    config.fov_recompute = True
    config.playscreen.clear
    config.CurrentDungeonLevel += 1
    newlevelid = EM.new_Id()
    config.DungeonLevelIds[config.CurrentDungeonLevel] = newlevelid
    mapid = config.mapgen.create(newlevelid)
    newlevel = DungeonLevel(config.CurrentDungeonLevel, mapid)
    CM.add_Component(newlevelid, 'DungeonLevel', newlevel)
    Place_Monsters_On_Level(newlevelid)
