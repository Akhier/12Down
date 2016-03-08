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


def make_dog(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Dog', 'd', False, True,
                          color=Color.darker_yellow))
    CM.add_Component(newmonsterid, 'Death',
                     Death('The little doggie wimpers as it falls over.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(12, 1, 14, 8, 5, 26, special={'Dodge': 10}))
    CM.add_Component(newmonsterid, 'Action', Dog_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_rabid_dog(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Rabid Dog', 'D', False, True,
                          color=Color.dark_yellow))
    deatheffects = [death_cleanup, rabid_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Rabid Dog foams at the mouth then slumps ' +
                           'over. It might be a dog eat dog world but ' +
                           'don\'t eat it.', '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(16, 2, 14, 6, 5, 104))
    CM.add_Component(newmonsterid, 'Action', Dog_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def rabid_choice(twintailid):
    choice = None
    while choice is None:
        choice = Menu('The Rabid Dog was put down. ' +
                      'Now claim your reward!',
                      ['The claws are dimly glowing',
                       'You think it\'s teeth would make a nice necklace',
                       'Though maybe you shouldn\'t touch a Rabid Dog'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playercreature.Special['CritChance'] = 20
        if playercreature.BaseStrength < 10:
            playercreature.BaseStrength = 10
        Message('The glow flows into your muscles. ' +
                'Now you feel like your strikes will be harder.')
    if choice == 1:
        if playercreature.BaseDefense <= 0:
            playercreature.BaseDefense = 1
        if 'EnhancedDefense' in playercreature.Special:
            playercreature.Special['EnhancedDefense'] += 10
        else:
            playercreature.Special['EnhancedDefense'] = 20
        Message('They do make a nice necklace. ' +
                'For some reason this makes you feel better defended!')
    if choice == 2:
        playercreature.Xp += 500
        Message('Sometimes wisdom comes from experiance. ' +
                'In this case it is the reverse.')


class Dog_AI:

    def __init__(self, dogid):
        self.DogId = dogid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack', Attack(1, 4))

    def take_turn(self):
        dogcreature = CM.get_Component('Creature', self.DogId)
        dogcoord = CM.get_Component('Coord', self.DogId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(dogcoord.X - playercoord.X,
                             dogcoord.Y - playercoord.Y)
        if disttoplayer < dogcreature.VisionRange:
            if int(disttoplayer) <= 1:
                Attack_Coord(self.BasicAttackId, self.DogId, playercoord)
            else:
                direction = MC.Get_Direction_To(dogcoord, playercoord)
                if not MC.Walk_Direction(self.DogId, direction):
                    directions = MC.Get_Alt_Direction_To(direction)
                    if not MC.Walk_Direction(self.DogId, directions[0]):
                        MC.Walk_Direction(self.DogId, directions[1])
        else:
            tiles = CM.dict_of('Tile')
            dogids = []
            for key, value in tiles.iteritems():
                if value.TileName == 'Dog' or \
                        value.TileName == 'Rabid Dog':
                    if key != self.DogId:
                        dogids.append(key)
            dogcoords = CM.get_Components('Coord', dogids)
            shortestdist = (False, dogcreature.VisionRange)
            for key, coord in dogcoords.iteritems():
                dist = hypot(dogcoord.X - coord.X, dogcoord.Y - coord.Y)
                if dist < shortestdist[1] and dist > 1.5:
                    shortestdist = (coord, dist)
            if shortestdist[0]:
                direction = MC.Get_Direction_To(dogcoord, shortestdist[0])
                if not MC.Walk_Direction(self.DogId, direction):
                    directions = MC.Get_Alt_Direction_To(direction)
                    if not MC.Walk_Direction(self.DogId, directions[0]):
                        MC.Walk_Direction(self.DogId, directions[1])
            else:
                direction = random.choice([D.N, D.S, D.E, D.W,
                                           D.NE, D.NW, D.SE, D.SW])
                MC.Walk_Direction(self.DogId, direction)
