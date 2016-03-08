from ComponentManager import ComponentManager as CM
from Enum_Direction import Direction
from random import shuffle, randint
from C_Coord import Coord
import config


def Walk_Direction(creatureid, direction):
    cCoord = CM.get_Component('Coord', creatureid)
    newCoord = Coord(cCoord.X + direction.X, cCoord.Y + direction.Y)
    Coords = CM.dict_of('Coord')
    walkable = True
    for key, value in Coords.iteritems():
        if value == newCoord:
            if CM.check_Component('Tile', key):
                tile = CM.get_Component('Tile', key)
                if not tile.Passable:
                    walkable = False
    if walkable:
        cCoord.X = newCoord.X
        cCoord.Y = newCoord.Y
        return True
    else:
        return False


def Get_Direction_To(sourcecoord, targetcoord):
    sx = sourcecoord.X
    sy = sourcecoord.Y
    tx = targetcoord.X
    ty = targetcoord.Y
    if tx == sx and ty < sy:
        return Direction.N
    elif tx == sx and ty > sy:
        return Direction.S
    elif tx < sx and ty == sy:
        return Direction.W
    elif tx > sx and ty == sy:
        return Direction.E
    elif tx < sx and ty < sy:
        return Direction.NW
    elif tx > sx and ty < sy:
        return Direction.NE
    elif tx < sx and ty > sy:
        return Direction.SW
    elif tx > sx and ty > sy:
        return Direction.SE
    else:
        return Direction.C


def Get_Alt_Direction_To(direction):
    if direction == Direction.N:
        d = [Direction.NW, Direction.NE]
        shuffle(d)
        return d
    elif direction == Direction.S:
        d = [Direction.SW, Direction.SE]
        shuffle(d)
        return d
    elif direction == Direction.W:
        d = [Direction.NW, Direction.SW]
        shuffle(d)
        return d
    elif direction == Direction.E:
        d = [Direction.NE, Direction.SE]
        shuffle(d)
        return d
    elif direction == Direction.NW:
        d = [Direction.N, Direction.W]
        shuffle(d)
        return d
    elif direction == Direction.NE:
        d = [Direction.N, Direction.E]
        shuffle(d)
        return d
    elif direction == Direction.SW:
        d = [Direction.S, Direction.W]
        shuffle(d)
        return d
    elif direction == Direction.SE:
        d = [Direction.S, Direction.E]
        shuffle(d)
        return d


def Get_Opposite_Direction(direction):
    if direction == Direction.N:
        return Direction.S
    elif direction == Direction.S:
        return Direction.N
    elif direction == Direction.W:
        return Direction.E
    elif direction == Direction.E:
        return Direction.W
    elif direction == Direction.NW:
        return Direction.SE
    elif direction == Direction.NE:
        return Direction.SW
    elif direction == Direction.SW:
        return Direction.NE
    elif direction == Direction.SE:
        return Direction.NW


def Teleport_Random(creatureid):
    cCoord = CM.get_Component('Coord', creatureid)
    x = randint(1, config.playscreen_width - 1)
    y = randint(1, config.playscreen_height - 1)
    newCoord = Coord(x, y)
    Coords = CM.dict_of('Coord')
    walkable = True
    for key, value in Coords.iteritems():
        if value == newCoord:
            if CM.check_Component('Tile', key):
                tile = CM.get_Component('Tile', key)
                if not tile.Passable:
                    walkable = False
    if walkable:
        cCoord.X = newCoord.X
        cCoord.Y = newCoord.Y
    else:
        Random_Teleport(creatureid)
