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
from Menu import Menu
import ECS_Storage
import config
import Color


def New_Game():
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
