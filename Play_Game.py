from ComponentManager import ComponentManager as CM
from Handle_Keys import Handle_Keys
from S_MapInfo import char_map
from Render import Render
from Menu import Menu
import libtcodpy
import config
import Color


def Play_Game():
    config.player_action = None
    config.mouse = libtcodpy.Mouse()
    config.key = libtcodpy.Key()
    while not config.gamewindow.is_window_closed:
        libtcodpy.sys_check_for_event(libtcodpy.EVENT_KEY_PRESS |
                                      libtcodpy.EVENT_MOUSE,
                                      config.key, config.mouse)
        Render()
        config.gamewindow.flush
        check_level_up()
        dungeonlevelid = config.DungeonLevelIds[config.CurrentDungeonLevel]
        dungeonlevel = CM.get_Component('DungeonLevel', dungeonlevelid)
        objectids = []
        objectids.extend(dungeonlevel.ItemIds)
        objectids.extend(dungeonlevel.FeatureIds)
        objectids.extend(dungeonlevel.MonsterIds)
        objectids.append(config.PlayerId)
        charmap = char_map(dungeonlevel.MapId)
        for objectid in objectids:
            objectcoord = CM.get_Component('Coord', objectid)
            x = objectcoord.X
            y = objectcoord.Y
            if config.visible[x][y]:
                config.playscreen.write_ex(x, y, charmap[x][y],
                                           Color.map_tile_visible)
        config.player_action = Handle_Keys()
        if config.player_action == 'exit' or config.game_state == 'finished':
            choice = None
            while choice is None:
                choice = Menu('Are you sure you want to Quit?',
                              ['Yes I want to quit', 'No'], 34)
            if choice == 0:
                config.gamewindow.clear
                config.playscreen.clear
                break
        if config.game_state == 'playing' and \
                config.player_action != 'no action':
            actions = CM.dict_of('Action')
            for key in actions.iterkeys():
                if key in objectids:
                    actions[key].take_turn()


def check_level_up():
    level_up_xp = int(config.xptolevel * config.xpscale)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if playercreature.Xp >= level_up_xp:
        playercreature.CurHp = playercreature.MaxHp
        playercreature.Xp = level_up_xp - playercreature.Xp
        playerlevel = CM.get_Component('Level', config.PlayerId)
        playerlevel.level += 1
        config.xptolevel = level_up_xp
        choice = None
        options = ['+2hp, +1Def, +1Str, +1Agi',
                   '+6hp and +2Def', '+6hp and +2Str',
                   '+6hp and +2Agi', '+10hp']
        sdef = False
        sstr = False
        sagi = False
        if playercreature.BaseDefense > 3:
            options.append('-4Def then +20hp')
            sdef = True
        if playercreature.BaseStrength > 3:
            options.append('-3Str then +9Agi')
            sstr = True
        if playercreature.BaseAgility > 3:
            options.append('-3Agi then +9Str')
            sagi = True
        while choice is None:   # HP Defense Strength Agility
            choice = Menu('Level Up! Choose how you would like' +
                          'to increase your stats.', options,
                          config.messagescreen_width)
        if choice == 0:
            playercreature.MaxHp += 2
            playercreature.CurHp += 2
            playercreature.BaseDefense += 1
            playercreature.BaseStrength += 1
            playercreature.BaseAgility += 1
        elif choice == 1:
            playercreature.MaxHp += 6
            playercreature.CurHp += 6
            playercreature.BaseDefense += 2
        elif choice == 2:
            playercreature.MaxHp += 6
            playercreature.CurHp += 6
            playercreature.BaseStrength += 2
        elif choice == 3:
            playercreature.MaxHp += 6
            playercreature.CurHp += 6
            playercreature.BaseAgility += 2
        elif choice == 4:
            playercreature.MaxHp += 10
            playercreature.CurHp += 10
        elif choice == 5:
            if sdef:
                playercreature.BaseDefense -= 4
                playercreature.MaxHp += 20
                playercreature.CurHp += 20
            elif sstr:
                playercreature.BaseStrength -= 3
                playercreature.BaseAgility += 9
            elif sagi:
                playercreature.BaseAgility -= 3
                playercreature.BaseStrength += 9
        elif choice == 6:
            if sdef and sstr:
                playercreature.BaseStrength -= 3
                playercreature.BaseAgility += 9
            elif sagi:
                playercreature.BaseAgility -= 3
                playercreature.BaseStrength += 9
        elif choice == 7:
            playercreature.BaseAgility -= 3
            playercreature.BaseStrength += 9
