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


def make_kangaroo(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Kangaroo', 'k', False, True,
                          color=Color.dark_sepia))
    CM.add_Component(newmonsterid, 'Death',
                     Death('This kangaroo won\'t be hopping anymore.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(10, 0, 10, 25, 10, 73))
    CM.add_Component(newmonsterid, 'Action', Kangaroo_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_electric_kangaroo(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Electric Kangaroo', 'K', False, True,
                          color=Color.cyan))
    deatheffects = [death_cleanup, electric_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Electric Kangaroos eye dim as it ' +
                           'falls to the ground.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(12, 0, 10, 30, 10, 293))
    CM.add_Component(newmonsterid, 'Action', Kangaroo_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def electric_choice(electricid):
    choice = None
    while choice is None:
        choice = Menu('The Electric kangaroo is grounded. ' +
                      'Now claim your reward!',
                      ['There are a few sparks still flowing over it',
                       'The feet seem to glow',
                       'Outback Barbecue'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playercreature.Special['Paralyzed'] = True
        if 'ParalyzeResistance' in playercreature.Special:
            playercreature.Special['ParalyzeResistance'] += 2
        else:
            playercreature.Special['ParalyzeResistance'] = 5
        if playercreature.BaseDefense < 10:
            playercreature.BaseDefense += 1
        Message('Shocking!')
    if choice == 1:
        if 'CardinalLeap' in playercreature.Special:
            (need, cur, dist) = playercreature.Special('CardinalLeap')
            need -= 1
            if need <= 1:
                need = 3
                dist += 1
            playercreature.Special['CardinalLeap'] = (need, need, dist)
        Message('Feet apperently equals leaping. (ctrl + cardinal direction)')
    if choice == 2:
        if playercreature.MaxHp < 20:
            playercreature.MaxHp += 6
        elif playercreature.MaxHp < 30:
            playercreature.MaxHp += 4
        else:
            playercreature.MaxHp += 2
        playercreature.CurHp = playercreature.MaxHp
        if playercreature.BaseDefense < 5:
            playercreature.BaseDefense += 3
        elif playercreature.BaseDefense < 10:
            playercreature.BaseDefense += 2
        else:
            playercreature.BaseDefense += 1
        if playercreature.BaseAgility < 10:
            playercreature.BaseAgility += 3
        elif playercreature.BaseAgility < 20:
            playercreature.BaseAgility += 2
        else:
            playercreature.BaseAgility += 1
        if playercreature.BaseStrength < 10:
            playercreature.BaseStrength += 3
        elif playercreature.BaseStrength < 20:
            playercreature.BaseStrength += 2
        else:
            playercreature.BaseStrength += 1
        Message('Overall stat boosts. The less there was the more there is!')


class Kangaroo_AI:

    def __init__(self, kangarooid):
        self.KangarooId = kangarooid
        self.BasicAttackId = EM.new_Id
        tile = CM.get_Component('Tile', kangarooid)
        if tile.TileName == 'Kangaroo':
            CM.add_Component(self.BasicAttackId, 'Attack', Attack(4, 2))
        else:
            CM.add_Component(self.BasicAttackId, 'Attack',
                             Attack(4, 2, special={'Paralyze': 10}))
        self.playerinvision = False

    def take_turn(self):
        kangaroocreature = CM.get_Component('Creature', self.KangarooId)
        kangaroocoord = CM.get_Component('Coord', self.KangarooId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(kangaroocoord.X - playercoord.X,
                             kangaroocoord.Y - playercoord.Y)
        if disttoplayer <= kangaroocreature.VisionRange and \
                coordfov(kangaroocoord, playercoord):
            if int(disttoplayer) <= 1:
                Attack_Coord(self.BasicAttackId, self.KangarooId,
                             playercoord)
            else:
                direction = MC.Get_Direction_To(kangaroocoord, playercoord)
                MC.Walk_Direction_Persistantly(self.KangarooId, direction)
        else:
            MC.Walk_Random_Multiple_Failable(self.KangarooId, 1, 2)
