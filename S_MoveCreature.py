from ComponentManager import ComponentManager as CM
from C_Coord import Coord


def Walk_Direction(creatureid, direction):
    cCoord = CM.get_Component('Coord', creatureid)
    newCoord = Coord(cCoord.X + direction.X, cCoord.Y + direction.Y)
    Coords = CM.dict_of('Coord')
    walkable = True
    for key, value in Coords:
        if value == newCoord:
            try:
                tile = CM.get_Component('Tile', key)
                if not tile.Passable:
                    walkable = False
            except:
                pass
    if walkable:
        cCoord = newCoord
