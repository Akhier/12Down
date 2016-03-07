from ComponentManager import ComponentManager as CM
from Message import Message
import Color


class Death:

    def __init__(self, deathmessage, char, effects=[]):
        self.DeathMessage = deathmessage
        self.Char = char
        self.Effects = effects


def death_cleanup(creatureid):
    creaturetile = CM.get_Component('Tile', creatureid)
    creaturedeath = CM.get_Component('Death', creatureid)
    creaturetile.Char = creaturedeath.Char
    creaturetile.Passable = True
    Message(creaturedeath.DeathMessage, Color.darker_red)
    CM.remove_Components(['Creature', 'Action'], creatureid)
