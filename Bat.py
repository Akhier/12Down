from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from Enum_Direction import Direction as D
from C_Death import Death, death_cleanup
from S_Combat import Attack_Coord
from C_Creature import Creature
from C_Attack import Attack
from Message import Message
import S_MoveCreature as MC
from C_Tile import Tile
from math import hypot
from Menu import Menu
import random
import config
import Color


def make_bat(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Bat', 'b', False, True,
                          color=Color.dark_gray))
    CM.add_Component(newmonsterid, 'Death',
                     Death('The small bat lets out one final pitiful squeak.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(3, 0, 8, 12, 5, 15))
    CM.add_Component(newmonsterid, 'Action', Bat_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_vampire_bat(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Vampire Bat', 'B', False, True,
                          color=Color.gray))
    deatheffects = [death_cleanup, vampires_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Vampire Bat falls to the floor.' +
                           ' The once dread creature is no more.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(6, 0, 10, 12, 5, 60))
    CM.add_Component(newmonsterid, 'Action', Bat_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def vampires_choice(vampireid):
    choice = None
    while choice is None:
        choice = Menu('You have conquered a Vampire (bat). ' +
                      'Now claim your reward!',
                      ['One fang is broken but the other is swordlike',
                       'The wings are glowing, *poke* *poke*',
                       'Drink it\'s blood, tis only fair'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playerattack = CM.get_Component('Attack', config.PlayerAttack)
        playerattack.Dice = 1
        playerattack.Sides = 6
        playerattack.Special['LifeDrain'] = 1
        playercreature.MaxHp -= 4
        Message('A nice sword but draining to wield')
    if choice == 1:
        playercreature.BaseAgility += 2
        playercreature.Special['Dodge'] = 20
        Message('The glow flows into you and suddenly you feel jumpy.')
    if choice == 2:
        playercreature.MaxHp += 10
        playercreature.CurHp = playercreature.MaxHp * 2
        Message('Drink it\'s blood, tis only fair!')


class Bat_AI:

    def __init__(self, batid):
        self.BatId = batid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack',
                         Attack(1, 2, {'LifeDrain': 1}))

    def take_turn(self):
        batcoord = CM.get_Component('Coord', self.BatId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(batcoord.X - playercoord.X,
                             batcoord.Y - playercoord.Y)
        if int(disttoplayer) <= 1:
            Attack_Coord(self.BasicAttackId, self.BatId, playercoord)
        direction = random.choice([D.N, D.S, D.E, D.W,
                                   D.NE, D.NW, D.SE, D.SW])
        MC.Walk_Direction(self.BatId, direction)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(batcoord.X - playercoord.X,
                             batcoord.Y - playercoord.Y)
        if int(disttoplayer) <= 1:
            Attack_Coord(self.BasicAttackId, self.BatId, playercoord)
