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


def make_jellyfish(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Jellyfish', 'j', False, True,
                          color=Color.white))
    CM.add_Component(newmonsterid, 'Death',
                     Death('The jellyfish splats onto the floor. Wonder ' +
                           'how it was floating in the first place.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(10, 10, 10, 10, 4, 84))
    CM.add_Component(newmonsterid, 'Action', Jellyfish_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_clear_jellyfish(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Clear Jellyfish', 'J', False, True,
                          color=Color.map_tile_visible))
    deatheffects = [death_cleanup, clear_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Clear Jellyfishs falls but upward.' +
                           'How weird...',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(10, 10, 10, 15, 4, 336))
    CM.add_Component(newmonsterid, 'Action', Jellyfish_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def clear_choice(clearid):
    choice = None
    while choice is None:
        choice = Menu('The Clear jellyfish is just a splatter on the ' +
                      'ceiling. Now claim your reward!',
                      ['This tentacle could be a whip',
                       'I wonder what it tastes like',
                       'There is a glowing puddle on the floor'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        attack = CM.get_Component('Attack', config.PlayerAttack)
        attack = Attack(1, 12, special={'Paralyze': 20})
        Message('Slimy but a workable whip none the less.')
    if choice == 1:
        if playercreature.BaseAgility < 10:
            playercreature.BaseAgility = 10
        else:
            playercreature.BaseAgility += 5
        playercreature.Special['ParalyzeResistance'] = 5
        Message('Actually it tastes good and you feel a bit more flexible.')
    if choice == 2:
        if 'HealthPotion' in playercreature.Special:
            playercreature.Special['HealthPotion'] += 3
        else:
            playercreature.Special['HealthPotion'] = 5
        Message('You shove it in a bottle and if you ' +
                'squint it looks like a health potion')


class Jellyfish_AI:

    def __init__(self, jellyfishid):
        self.JellyfishId = jellyfishid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack',
                         Attack(2, 4, special={'Paralyze': 5}))

    def take_turn(self):
        jellyfishcreature = CM.get_Component('Creature', self.JellyfishId)
        jellyfishcoord = CM.get_Component('Coord', self.JellyfishId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(jellyfishcoord.X - playercoord.X,
                             jellyfishcoord.Y - playercoord.Y)
        if disttoplayer <= jellyfishcreature.VisionRange and \
                coordfov(jellyfishcoord, playercoord):
            if int(disttoplayer) <= 1:
                Attack_Coord(self.BasicAttackId, self.JellyfishId,
                             playercoord)
            else:
                direction = MC.Get_Direction_To(jellyfishcoord,
                                                playercoord)
                MC.Walk_Direction_Persistantly(self.JellyfishId, direction)
        else:
            MC.Walk_Random_Failable(self.JellyfishId)
