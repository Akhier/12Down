class DungeonLevel:

    def __init__(self, level, mapid):
        self.MapId = mapid
        self.MonsterIds = []
        self.ItemIds = []
        self.FeatureIds = []
        self.Level = level
        self.MonstersKilled = 0
        self.StairsPresent = False
