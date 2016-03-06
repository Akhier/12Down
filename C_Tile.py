class Tile:

    def __init__(self, name, char, passable, seethrough, color=False):
        self.TileName = name
        self.Char = char
        self.Passable = passable
        self.Seethrough = seethrough
        self.Color = color
        self.Name = 'Tile'
