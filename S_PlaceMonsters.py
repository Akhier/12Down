from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from C_Creature import Creature
from C_Coord import Coord
from C_Tile import Tile
import config
import random
import Color


def Place_Monsters_On_Level(dungeonlevelid):
    dungeonlevel = CM.get_Component('DungeonLevel', dungeonlevelid)
    curmap = CM.get_Component('Map', dungeonlevel.MapId)
    random.seed(curmap.Seed)
    placed_monsters = 0
    while placed_monsters <= config.monster_per_level:
        x = random.randint(1, curmap.Width - 1)
        y = random.randint(1, curmap.Height - 1)
        testcoord = Coord(x, y)
        coords = CM.dict_of('Coord')
        tiles = CM.dict_of('Tile')
        freetoplace = True
        for key, value in coords.iteritems():
            if testcoord == value and key in tiles:
                if not tiles[key].Passable:
                    freetoplace = False
        if freetoplace:
            newmonsterid = EM.new_Id()
            CM.add_Component(newmonsterid, 'Coord', testcoord)
            CM.add_Component(newmonsterid, 'Tile',
                             Tile('Ant', 'a', False, True,
                                  color=Color.darker_red))
            CM.add_Component(newmonsterid, 'Creature',
                             Creature(1, 10, 10, 5, 5, 7))
            dungeonlevel.MonsterIds.append(newmonsterid)
            placed_monsters += 1
