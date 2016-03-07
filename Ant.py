from S_MoveCreature import Walk_Direction, Get_Direction_To, \
    Get_Alt_Direction_To
from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from C_Death import Death, death_cleanup
from S_Combat import Attack_Coord
from C_Creature import Creature
from C_Attack import Attack
from Message import Message
from C_Tile import Tile
from math import hypot
from Menu import Menu
import config
import Color


def make_ant(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Ant', 'a', False, True,
                          color=Color.darker_red))
    CM.add_Component(newmonsterid, 'Death',
                     Death('The ants shell now smashed gives way ' +
                           'as it breaths it\'s final breath',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(1, 10, 10, 5, 5, 7))
    CM.add_Component(newmonsterid, 'Action', Ant_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_queen_ant(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Queen Ant', 'A', False, True,
                          color=Color.white))
    deatheffects = [queens_choice, death_cleanup]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Ant Queen shudders and slumps over now dead.' +
                           ' The once majestic creature now pitiful.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(5, 10, 10, 5, 4, 7))
    CM.add_Component(newmonsterid, 'Action', Ant_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def queens_choice(queenid):
    choice = None
    while choice is None:
        choice = Menu('You have beaten the first boss. Now claim your reward!',
                      ['Reinforce your gear with it\'s shell',
                       'Wield it\'s jaws as daggers',
                       'Examine the weird glow on it\'s antenna'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playercreature.BaseAgility -= 1
        playercreature.BaseDefense += 1
        playercreature.Special['EnhancedDefense'] = 25
        Message('Your armor feels studier though it is stiffer')
    if choice == 1:
        playerattack = CM.get_Component('Attack', config.PlayerAttack)
        playerattack.Dice = 2
        playerattack.Sides = 4
        playerattack.Special['PierceDefense'] = 5
        Message('Maybe having 2 sharp daggers will up your damager?')
    if choice == 2:
        playercreature.BaseAgility += 1
        playercreature.VisionRange += 1
        Message('The strange glow streams into your eyes. After the shock ' +
                'wears of you notice you can see better')


class Ant_AI:

    def __init__(self, antid):
        self.AntId = antid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack', Attack(1, 1))

    def take_turn(self):
        antcreature = CM.get_Component('Creature', self.AntId)
        antcoord = CM.get_Component('Coord', self.AntId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(antcoord.X - playercoord.X,
                             antcoord.Y - playercoord.Y)
        if disttoplayer < antcreature.VisionRange:
            if int(disttoplayer) <= 1:
                Attack_Coord(self.BasicAttackId, self.AntId, playercoord)
            else:
                direction = Get_Direction_To(antcoord, playercoord)
                if not Walk_Direction(self.AntId, direction):
                    directions = Get_Alt_Direction_To(direction)
                    if not Walk_Direction(self.AntId, directions[0]):
                        Walk_Direction(self.AntId, directions[1])
