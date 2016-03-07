from ComponentManager import ComponentManager as CM
from C_Coord import Coord
from Ant import make_ant
import config
import random


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
            make_ant(testcoord, dungeonlevel)
            placed_monsters += 1
