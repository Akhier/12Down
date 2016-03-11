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


def make_hawk(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Hawk', 'h', False, True,
                          color=Color.darker_orange))
    CM.add_Component(newmonsterid, 'Death',
                     Death('The dead hawk flutters to the ground dead.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(10, 0, 10, 25, 10, 73))
    CM.add_Component(newmonsterid, 'Action', Hawk_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_savage_hawk(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Savage Hawk', 'H', False, True,
                          color=Color.dark_crimson))
    deatheffects = [death_cleanup, savage_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Savage Hawks eye dim as it ' +
                           'falls to the ground.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(12, 0, 10, 30, 10, 293))
    CM.add_Component(newmonsterid, 'Action', Hawk_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def savage_choice(savageid):
    choice = None
    while choice is None:
        choice = Menu('The Savage hawk is grounded. ' +
                      'Now claim your reward!',
                      ['The claws glow',
                       'The eyes glow',
                       'and believe it or not the wings glow!'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playercreature.Special['SideSwipe'] = True
        Message('You feel that just walking past enemies (diagonally)' +
                ' that you can get attacks in!')
    if choice == 1:
        if playercreature.BaseAgility < 10:
            playercreature.BaseAgility += 1
        if 'Dodge' in playercreature.Special:
            playercreature.Special['Dodge'] += 10
        else:
            playercreature.Special['Dodge'] = 20
        Message('Your eyesight sharpens and you feel you can dodge better.')
    if choice == 2:
        if 'CardinalLeap' in playercreature.Special:
            (need, cur, dist) = playercreature.Special('CardinalLeap')
            need -= 1
            if need <= 1:
                need = 3
                dist += 1
            playercreature.Special['CardinalLeap'] = (need, need, dist)
        else:
            playercreature.Special['CardinalLeap'] = (5, 5, 3)
        Message('The seems like it can occasionally ' +
                'boost your leaping ability. (ctrl + cardinal direction)')


class Hawk_AI:

    def __init__(self, hawkid):
        self.HawkId = hawkid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack',
                         Attack(2, 4, special={'PierceDefense': 5}))

    def take_turn(self):
        hawkcreature = CM.get_Component('Creature', self.HawkId)
        hawkcoord = CM.get_Component('Coord', self.HawkId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(hawkcoord.X - playercoord.X,
                             hawkcoord.Y - playercoord.Y)
        if disttoplayer < hawkcreature.VisionRange and \
                coordfov(hawkcoord, playercoord):
            if int(disttoplayer) <= 1:
                Attack_Coord(self.BasicAttackId, self.HawkId,
                             playercoord)
                MC.Walk_Direction_Persistantly(
                    self.HawkId, MC.Get_Direction_To(
                        hawkcoord, playercoord))
            else:
                direction = MC.Get_Direction_To(hawkcoord, playercoord)
                MC.Walk_Direction_Persistantly(self.HawkId, direction)
        else:
            MC.Walk_Random_Failable(self.HawkId)
