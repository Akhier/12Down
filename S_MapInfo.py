from ComponentManager import ComponentManager as CM


def char_map(mapid):
    Map = CM.get_Component('Map', mapid)
    Tiles = tiles_in_map(Map)
    Chars = [[False for y in range(Map.Height)]
             for x in range(Map.Width)]
    for y in range(Map.Height):
        for x in range(Map.Width):
            Chars[x][y] = Tiles[x][y].Char
    return Chars


def seethrough_map(mapid):
    Map = CM.get_Component('Map', mapid)
    Tiles = tiles_in_map(Map)
    Seethrough = [[False for y in range(Map.Height)]
                  for x in range(Map.Width)]
    for y in range(Map.Height):
        for x in range(Map.Width):
            Seethrough[x][y] = Tiles[x][y].Seethrough
    return Seethrough


def tiles_in_map(Map):
    Tiles = [[False for y in range(Map.Height)]
             for x in range(Map.Width)]
    for y in range(Map.Height):
        for x in range(Map.Width):
            Tiles[x][y] = CM.get_Component('Tile', Map.TileIds[x][y])
    return Tiles
