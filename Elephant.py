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
import config
import random
import Color


def make_elephant(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Elephant', 'e', False, True,
                          color=Color.gray))
    CM.add_Component(newmonsterid, 'Death',
                     Death('Before like an angry mountain this elephant ' +
                           'is now just a boulder.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(30, 1, 10, 5, 7, 42))
    CM.add_Component(newmonsterid, 'Action', Elephant_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_pink_elephant(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Pink Elephant', 'E', False, True,
                          color=Color.pink))
    deatheffects = [death_cleanup, pink_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Pink Elephant disapeers. Now you just ' +
                           'have to ask, was it there to begin with?',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(60, 2, 10, 5, 7, 168))
    CM.add_Component(newmonsterid, 'Action', Elephant_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def pink_choice(pinkid):
    choice = None
    while choice is None:
        choice = Menu('The Pink Elephant no longer parades around. ' +
                      'Now claim your reward!',
                      ['Let\'s collect these sparkles',
                       'It feels like it is my spirit animal!',
                       'I really just need a drink right now.'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playercreature.Special['RandomBlink'] = 10
        Menu('You feel that these sparkles will let you blink around a ' +
             'few times. (Ctrl + b)')
    if choice == 1:
        if playercreature.BaseDefense < 2:
            playercreature.BaseDefense = 2
        playercreature.MaxHp += 30
        playercreature.CurHp = playercreature.MaxHp
    if choice == 2:
        playercreature.Special['HealthPotion'] = 5
        Message('Oh look, bottles of red liquid. ' +
                '\'D\'rink to heal, caps at max.')


class Elephant_AI:

    def __init__(self, elephantid):
        self.ElephantId = elephantid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack',
                         Attack(2, 4, special={'PierceDefense': 10}))
        self.resting = False

    def take_turn(self):
        elephantcreature = CM.get_Component('Creature', self.ElephantId)
        elephantcoord = CM.get_Component('Coord', self.ElephantId)
        elephanttile = CM.get_Component('Tile', self.ElephantId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(elephantcoord.X - playercoord.X,
                             elephantcoord.Y - playercoord.Y)
        if disttoplayer < elephantcreature.VisionRange:
            if int(disttoplayer) <= 1:
                if not self.resting:
                    Attack_Coord(self.BasicAttackId, self.ElephantId,
                                 playercoord)
                    self.resting = True
                else:
                    self.resting = False
                    Message('The ' + elephanttile.TileName +
                            ' rests this turn instead of attacking.',
                            color=Color.yellow)
            else:
                self.resting = False
                direction = MC.Get_Direction_To(elephantcoord, playercoord)
                if not MC.Walk_Direction(self.ElephantId, direction):
                    directions = MC.Get_Alt_Direction_To(direction)
                    if not MC.Walk_Direction(self.ElephantId, directions[0]):
                        MC.Walk_Direction(self.ElephantId, directions[1])
        else:
            tiles = CM.dict_of('Tile')
            elephantids = []
            for key, value in tiles.iteritems():
                if value.TileName == 'Elephant' or \
                        value.TileName == 'Pink Elephant':
                    if key != self.ElephantId:
                        elephantids.append(key)
            elephantcoords = CM.get_Components('Coord', elephantids)
            shortestdist = (False, elephantcreature.VisionRange)
            for key, coord in elephantcoords.iteritems():
                dist = hypot(
                    elephantcoord.X - coord.X, elephantcoord.Y - coord.Y)
                if dist < shortestdist[1] and dist > 1.5:
                    shortestdist = (coord, dist)
            if shortestdist[0]:
                direction = MC.Get_Direction_To(elephantcoord, shortestdist[0])
                if not MC.Walk_Direction(self.ElephantId, direction):
                    directions = MC.Get_Alt_Direction_To(direction)
                    if not MC.Walk_Direction(self.ElephantId, directions[0]):
                        MC.Walk_Direction(self.ElephantId, directions[1])
            else:
                direction = random.choice([D.N, D.S, D.E, D.W,
                                           D.NE, D.NW, D.SE, D.SW])
                MC.Walk_Direction(self.ElephantId, direction)
