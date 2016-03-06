class Creature:

    def __init__(self, hp, defense, strength, agility, visionrange, xp):
        self.MaxHp = hp
        self.CurHp = hp
        self.BaseDefense = defense
        self.BaseStrength = strength
        self.BaseAgility = agility
        self.VisionRange = visionrange
        self.Xp = xp
