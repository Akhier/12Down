from S_CoordtoCoordFov import coord_to_coord_fov as coordfov
from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from C_Death import Death, death_cleanup
from S_Combat import Attack_Coord
from C_Creature import Creature
from C_Attack import Attack
from Message import Message
import S_MoveCreature as MC
from C_Tile import Tile
from math import hypot
from Menu import Menu
import config
import Color


def make_frog(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Frog', 'f', False, True,
                          color=Color.lighter_green))
    CM.add_Component(newmonsterid, 'Death',
                     Death('Squished frog, how droll.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(10, 0, 5, 20, 5, 61))
    CM.add_Component(newmonsterid, 'Action', Frog_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_poison_frog(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Poison Frog', 'F', False, True,
                          color=Color.red))
    deatheffects = [death_cleanup, poison_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('Congradulations! You didn\'t even need a blender.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(20, 0, 10, 21, 5, 244))
    CM.add_Component(newmonsterid, 'Action', Frog_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def poison_choice(poisonid):
    choice = None
    while choice is None:
        choice = Menu('The Poison Frog has croaked. ' +
                      'Now claim your reward!',
                      ['Frog Legs, yumm',
                       'Wait the legs are actually glowing',
                       'Hey, I see that look. Don\'t lick it'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playercreature.CurHp += 6
        playercreature.BaseAgility += 2
        playercreature.Special['Poisoned'] = (2, 1, config.PlayerId)
        Message('Did you forget the first part of its name?')
    if choice == 1:
        playercreature.Special['CardinalLeap'] = (5, 5, 3)
        Message('You now feel like leaping. (ctrl + cardinal direction)')
    if choice == 2:
        playercreature.Special['Poisoned'] = (5, 1, config.PlayerId)
        playercreature.Special['PoisonResistance'] = 10
        Message('Well maybe this will teach you though the resist will help')


class Frog_AI:

    def __init__(self, frogid):
        self.FrogId = frogid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack',
                         Attack(1, 4, special={'CausePoison': (25, 5, 1)}))
        self.resting = 0

    def take_turn(self):
        frogcreature = CM.get_Component('Creature', self.FrogId)
        frogcoord = CM.get_Component('Coord', self.FrogId)
        frogtile = CM.get_Component('Tile', self.FrogId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(frogcoord.X - playercoord.X,
                             frogcoord.Y - playercoord.Y)
        if disttoplayer < frogcreature.VisionRange and \
                coordfov(frogcoord, playercoord):
            if int(disttoplayer) <= 1:
                Attack_Coord(self.BasicAttackId, self.FrogId,
                             playercoord)
            else:
                direction = MC.Get_Direction_To(frogcoord, playercoord)
                if self.resting <= 0:
                    if not MC.Walk_Direction(self.FrogId, direction):
                        directions = MC.Get_Alt_Direction_To(direction)
                        if not MC.Walk_Direction(self.FrogId, directions[0]):
                            MC.Walk_Direction(self.FrogId, directions[1])
                    self.resting = 2
                else:
                    MC.Walk_Direction_Multiple(self.FrogId, direction, 3)
                    Message('The ' + frogtile.TileName + ' jumps.')
                    self.resting -= 1
        else:
            MC.Walk_Random_Failable(self.FrogId)
