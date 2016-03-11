from S_CoordtoCoordFov import coord_to_coord_fov as coordfov
from ComponentManager import ComponentManager as CM
from S_DistanceBetweenCoords import get_distance
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


def make_goblin(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Goblin', 'g', False, True,
                          color=Color.green))
    CM.add_Component(newmonsterid, 'Death',
                     Death('A dead goblin, now this is ' +
                           'generic adventuring fair!',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(20, 2, 10, 10, 8, 68))
    CM.add_Component(newmonsterid, 'Action', Goblin_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_hobgoblin(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Hobgoblin', 'G', False, True,
                          color=Color.dark_green))
    deatheffects = [death_cleanup, hobs_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('Hobgoblins die like goblins, just darker.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(30, 3, 12, 10, 8, 272))
    CM.add_Component(newmonsterid, 'Action', Goblin_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def hobs_choice(hobsid):
    choice = None
    while choice is None:
        choice = Menu('The Hobgoblin is now hobless. ' +
                      'Now claim your reward!',
                      ['An actual helmet! Joy',
                       'This sword is big but glows',
                       'Fallen on the ground next to it is a vial'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    playerattack = CM.get_Component('Attack', config.PlayerAttack)
    if choice == 0:
        playercreature.Special['ReduceCrit'] = 50
        if playercreature.BaseDefense <= 5:
            playercreature.BaseDefense += 1
        Message('Unlike you probably assumed this doesn\'t seem ' +
                'to reduce the chance of getting critted ' +
                'but rather damage taken from one.')
    if choice == 1:
        playerattack = Attack(2, 6, special={'PlusAgility': 4,
                                             'PierceDefense': 5})
        Message('This seems to be a magic weapon which helps in combat!')
    if choice == 2:
        playerattack.Special['CausePoison'] = (35, 5, 1)
        Message('The vial contains a sticky poison ' +
                'so you apply it to your weapon.')


class Goblin_AI:

    def __init__(self, goblinid):
        self.GoblinId = goblinid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack', Attack(2, 3))
        self.nearbygoblins = []

    def take_turn(self):
        goblincreature = CM.get_Component('Creature', self.GoblinId)
        goblincoord = CM.get_Component('Coord', self.GoblinId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = hypot(goblincoord.X - playercoord.X,
                             goblincoord.Y - playercoord.Y)
        if disttoplayer <= goblincreature.VisionRange and \
                coordfov(goblincoord, playercoord):
                if int(disttoplayer) <= 1:
                    Attack_Coord(self.BasicAttackId, self.GoblinId,
                                 playercoord)
                else:
                    direction = MC.Get_Direction_To(goblincoord, playercoord)
                    MC.Walk_Direction_Persistantly(self.GoblinId, direction)
        else:
            curnearbygoblins = []
            tiles = CM.dict_of('Tile')
            coords = CM.dict_of('Coord')
            for key, value in tiles.iteritems():
                if (value.TileName == 'Goblin' or
                        value.TileName == 'Hobgoblin') and \
                        key != self.GoblinId:
                    if get_distance(goblincoord, coords[key]) <= \
                            goblincreature.VisionRange:
                        curnearbygoblins.append(key)
            if not self.nearbygoblins:
                self.nearbygoblins = curnearbygoblins
            else:
                direction = False
                for key in curnearbygoblins:
                    if key not in self.nearbygoblins:
                        direction = MC.Get_Direction_To(
                            goblincoord, coords[key])
                        break
                if direction:
                    MC.Walk_Direction_Persistantly(self.GoblinId, direction)
