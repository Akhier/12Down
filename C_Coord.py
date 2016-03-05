class Coord:

    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Name = 'Coord'

    @classmethod
    def coord(self):
        return (self.X, self.Y)
