from C_Coord import Coord
from enum import Enum


class Direction(Enum):
    N = Coord(0, -1)
    S = Coord(0, 1)
    E = Coord(-1, 0)
    W = Coord(1, 0)
    NW = Coord(-1, -1)
    NE = Coord(1, -1)
    SW = Coord(-1, 1)
    SE = Coord(1, 1)
