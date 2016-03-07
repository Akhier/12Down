from S_MoveCreature import Walk_Direction, Get_Direction_To, \
    Get_Alt_Direction_To
from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from S_Combat import Attack_Coord
from C_Creature import Creature
from C_Attack import Attack
from C_Tile import Tile
from math import hypot
import config
import Color


def make_ant(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Ant', 'a', False, True,
                          color=Color.darker_red))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(1, 10, 10, 5, 5, 7))
    CM.add_Component(newmonsterid, 'Action', Ant_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


class Ant_AI:

    def __init__(self, antid):
        self.AntId = antid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack', Attack(0, 1))

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
