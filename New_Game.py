from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from Handle_Keys import next_level
from C_Creature import Creature
from C_Attack import Attack
from Message import Message
from C_Coord import Coord
from C_Death import Death
from C_Flags import Level
from C_Tile import Tile
from Panel import Panel
from Menu import Menu
import ECS_Storage
import libtcodpy
import config
import Color


def New_Game():
    get_name()
    ECS_Storage.init()
    config.DungeonLevelIds = {}
    config.CurrentDungeonLevel = 0
    config.PlayerId = EM.new_Id()
    config.PlayerAttack = EM.new_Id()
    config.fov_recompute = True
    config.game_msg = []
    config.game_state = 'playing'
    config.xptolevel = 66.6
    CM.new_Component('ToLevel')
    CM.add_Component(config.PlayerId, 'Tile', Tile('Player', '@', False,
                                                   True, Color.sky))
    CM.add_Component(config.PlayerId, 'Coord',
                     Coord(config.playscreen_width / 2,
                           config.playscreen_height / 2))
    deatheffects = [player_death]
    CM.add_Component(config.PlayerId, 'Death',
                     Death('You have died. What a pity.' +
                           ' Did you even manage to get any loot?',
                           '%', effects=deatheffects))
    CM.add_Component(config.PlayerId, 'Creature', Creature(10, 0, 10,
                                                           10, 7, 0))
    CM.add_Component(config.PlayerId, 'Level', Level())
    CM.add_Component(config.PlayerAttack, 'Attack', Attack(1, 4))
    next_level()
    Message('Welcome young adventurer! You have just entered my dungeon and' +
            ' through my deal with the adventurers guild you may explore my' +
            ' first 26 levels! Though of course everything will still try to' +
            ' kill you but atleast once finish there is an easy passage out!',
            Color.red)


def player_death(playerid):
    choice = None
    while choice is None:
        choice = Menu('You have Died!', ['Exits to Main Menu'], 30)
    config.game_state = 'finished'


def get_name():
    config.PlayerName = ''
    name = ''
    namepanel = Panel(0, 0, config.window_width, config.window_height)
    while True:
        namepanel.clear
        config.gamewindow.clear
        namepanel.write(config.window_width / 2 - 10,
                        int(config.window_height * .2),
                        'Please Enter a Name!')
        namepanel.write(config.window_width / 2 - len(name) / 2 - 2,
                        int(config.window_height * .3),
                        '( ' + name + ' )')
        namepanel.blit()
        config.gamewindow.flush
        key = libtcodpy.console_wait_for_keypress(True)
        if key.vk == libtcodpy.KEY_BACKSPACE and len(name) > 0:
            name = name[:-1]
        elif key.vk == libtcodpy.KEY_ENTER and len(name) > 0:
            option = None
            while option is None:
                option = Menu('Is ' + name + ' the name you want?',
                              ['Yes', 'No'], 20)
            if option == 0:
                break
        else:
            if key.c != 0:
                key_char = chr(key.c)
                name += key_char
    config.PlayerName = name
