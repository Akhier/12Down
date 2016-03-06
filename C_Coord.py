class Coord:

    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Name = 'Coord'

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    @classmethod
    def coord(self):
        return (self.X, self.Y)
