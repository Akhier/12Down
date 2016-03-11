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


def make_cat(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Cat', 'c', False, True,
                          color=Color.orange))
    CM.add_Component(newmonsterid, 'Death',
                     Death('The lithe cat seems to have run out of lives.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(9, 0, 10, 10, 5, 20, special={'Dodge': 10}))
    CM.add_Component(newmonsterid, 'Action', Cat_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_twin_tailed_cat(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Twin Tailed Cat', 'C', False, True,
                          color=Color.orange))
    deatheffects = [death_cleanup, twin_tailed_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Twin Tailed Cat doesn\'t land on it\'s feet ' +
                           'this time. This kitty won\'t wave no more.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(9, 0, 10, 10, 5, 80, special={'Dodge': 20}))
    CM.add_Component(newmonsterid, 'Action', Cat_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def twin_tailed_choice(twintailid):
    choice = None
    while choice is None:
        choice = Menu('Twin Tailed Cat conquered courageously. ' +
                      'Now claim your reward!',
                      ['One of the tails is glowing brightly',
                       'The eyes also seem to have a glow to them',
                       'This fur might pad my armor'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playercreature.Special['LifeSaver'] = 1
        Message('As you touch the tail the whole cat ' +
                'suddenly glows and disappears.')
    if choice == 1:
        playercreature.BaseAgility += 2
        playercreature.VisionRange += 2
        config.fov_recompute = True
        Message('The glow jumps into your eyes and you suddenly ' +
                'can see in the dark better!')
    if choice == 2:
        playercreature.BaseAgility += 4
        if 'EnhancedDefense' in playercreature.Special:
            playercreature.Special['EnhancedDefense'] += 5
        else:
            playercreature.Special['EnhancedDefense'] = 10
        playercreature.BaseDefense += 2
        Message('Somehow your armor is not only better at absorbing ' +
                'blows but also better fitting.')


class Cat_AI:

    def __init__(self, catid):
        self.CatId = catid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack', Attack(1, 1))

    def take_turn(self):
        catcreature = CM.get_Component('Creature', self.CatId)
        catcoord = CM.get_Component('Coord', self.CatId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(catcoord.X - playercoord.X,
                             catcoord.Y - playercoord.Y)
        if disttoplayer < catcreature.VisionRange and \
                coordfov(catcoord, playercoord):
            if int(disttoplayer) <= 1:
                Attack_Coord(self.BasicAttackId, self.CatId, playercoord)
            else:
                direction = MC.Get_Direction_To(catcoord, playercoord)
                if not MC.Walk_Direction(self.CatId, direction):
                    directions = MC.Get_Alt_Direction_To(direction)
                    if not MC.Walk_Direction(self.CatId, directions[0]):
                        MC.Walk_Direction(self.CatId, directions[1])
        else:
            tiles = CM.dict_of('Tile')
            catids = []
            for key, value in tiles.iteritems():
                if value.TileName == 'Cat' or \
                        value.TileName == 'Twin Tailed Cat':
                    if key != self.CatId:
                        catids.append(key)
            catcoords = CM.get_Components('Coord', catids)
            shortestdist = (False, catcreature.VisionRange)
            for key, coord in catcoords.iteritems():
                dist = hypot(catcoord.X - coord.X, catcoord.Y - coord.Y)
                if dist < shortestdist[1]:
                    shortestdist = (coord, dist)
            if shortestdist[0]:
                direction = MC.Get_Direction_To(shortestdist[0], catcoord)
                if not MC.Walk_Direction(self.CatId, direction):
                    directions = MC.Get_Alt_Direction_To(direction)
                    if not MC.Walk_Direction(self.CatId, directions[0]):
                        MC.Walk_Direction(self.CatId, directions[1])
