from math import hypot


def get_distance(coord, coord2):
    return hypot(coord.X - coord2.X, coord.Y - coord2.Y)
