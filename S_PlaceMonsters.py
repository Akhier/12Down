from ComponentManager import ComponentManager as CM
from C_Coord import Coord
import config
import random
import Ant
import Bat


monsters = {1: Ant.make_ant, 2: Bat.make_bat}
bossmonsters = {1: Ant.make_queen_ant, 2: Bat.make_vampire_bat}


def Place_Monsters_On_Level(dungeonlevelid):
    dungeonlevel = CM.get_Component('DungeonLevel', dungeonlevelid)
    curmap = CM.get_Component('Map', dungeonlevel.MapId)
    random.seed(curmap.Seed)
    placed_monsters = 0
    while placed_monsters <= config.monster_per_level:
        if dungeonlevel.Level == 1:
            monster = monsters[1]
        elif dungeonlevel.Level == 2:
            if random.randint(1, 10) == 1:
                monster = monsters[1]
            else:
                monster = monsters[2]
        x = random.randint(1, curmap.Width - 1)
        y = random.randint(1, curmap.Height - 1)
        if x < curmap.Width / 2 - 4 or x > curmap.Width / 2 + 4 or \
                y < curmap.Height / 2 - 4 or y > curmap.Height / 2 + 4:
            testcoord = Coord(x, y)
            if Try_Place(testcoord, dungeonlevel, monster):
                placed_monsters += 1
                placed_in_relation = 0
                while Place_in_Relation(testcoord, dungeonlevel,
                                        monster) and \
                        placed_in_relation <= config.monster_per_level * .25:
                    placed_monsters += 1
                    placed_in_relation += 1


def Place_in_Relation(sourcecoord, dungeonlevel, monster,
                      maxoffset=5, minoffset=3):
    goodoffset = False
    while not goodoffset:
        xoffset = random.randint(-maxoffset, maxoffset)
        yoffset = random.randint(-maxoffset, maxoffset)
        if minoffset > 0:
            if (xoffset >= minoffset or xoffset <= -minoffset) and \
                    (yoffset >= minoffset or yoffset <= -minoffset):
                goodoffset = True
        else:
            goodoffset = True
    targetcoord = Coord(sourcecoord.X + xoffset, sourcecoord.Y + yoffset)
    return Try_Place(targetcoord, dungeonlevel, monster)


def Place_Boss(dungeonlevel):
    monster = bossmonsters[dungeonlevel.Level]
    playercoord = CM.get_Component('Coord', config.PlayerId)
    sourcex = -playercoord.X
    if sourcex > config.playscreen_width * .25 and \
            sourcex < config.playscreen_width * .75:
        if sourcex < config.playscreen_width * .5:
            sourcex -= int(config.playscreen_width * .25)
        else:
            sourcex += int(config.playscreen_width * .25)
    sourcey = -playercoord.Y
    if sourcey > config.playscreen_height * .25 and \
            sourcey < config.playscreen_height * .75:
        if sourcey < config.playscreen_height * .5:
            sourcey -= int(config.playscreen_height * .25)
        else:
            sourcey += int(config.playscreen_height * .25)
    sourcecoord = Coord(sourcex, sourcey)
    if not Try_Place(sourcecoord, dungeonlevel, monster):
        failure_in_Relation = 0
        maxoffset = 5
        while not Place_in_Relation(sourcecoord, dungeonlevel, monster,
                                    maxoffset=maxoffset, minoffset=0):
            failure_in_Relation += 1
            if failure_in_Relation > maxoffset * 10:
                maxoffset += 1
                failure_in_Relation = 0


def Try_Place(targetcoord, dungeonlevel, monster):
    if targetcoord.X > 0 and targetcoord.X < config.playscreen_width and \
            targetcoord.Y > 0 and targetcoord.Y < config.playscreen_height:
        coords = CM.dict_of('Coord')
        tiles = CM.dict_of('Tile')
        freetoplace = True
        for key, value in coords.iteritems():
            if targetcoord == value and key in tiles:
                if not tiles[key].Passable:
                    freetoplace = False
        if freetoplace:
            monster(targetcoord, dungeonlevel)
            return True
        return False
    else:
        return False
