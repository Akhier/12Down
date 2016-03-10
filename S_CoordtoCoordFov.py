from ComponentManager import ComponentManager as CM
from S_BresenhamLineAlgo import get_line


def coord_to_coord_fov(coord, coord2):
    line = get_line((coord.X, coord.Y), (coord.X, coord.Y))
    line = line[1:-1]
    coords = CM.dict_of('Coord')
    tiles = CM.dict_of('Tile')
    for key, value in coords.iteritems():
        if value in line:
            if key in tiles:
                if not tiles.Passable:
                    return False
    return True
