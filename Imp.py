from ComponentManager import ComponentManager as CM
from EntityManager import EntityManager as EM
from C_Death import Death, death_cleanup
from S_MapInfo import seethrough_map
from S_Combat import Attack_Coord
from C_Creature import Creature
from C_Attack import Attack
from Message import Message
import S_MoveCreature as MC
from C_Tile import Tile
from math import hypot
from Menu import Menu
import config
import Color


def make_imp(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Imp', 'i', False, True,
                          color=Color.red))
    CM.add_Component(newmonsterid, 'Death',
                     Death('The dead imp quickly fades from reality.',
                           '.', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(20, 0, 10, 18, 4, 79))
    CM.add_Component(newmonsterid, 'Action', Imp_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_blue_imp(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Blue Imp', 'I', False, True,
                          color=Color.blue))
    deatheffects = [death_cleanup, blue_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Blue Imp\'s body bursts into a ' +
                           'flame and burns away to nothing.',
                           '.', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(25, 1, 10, 20, 4, 316))
    CM.add_Component(newmonsterid, 'Action', Imp_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def blue_choice(blueid):
    choice = None
    while choice is None:
        choice = Menu('The Blue imp leaves almost nothing behind. ' +
                      'Now claim your reward!',
                      ['Sparkly dust of course',
                       'A whiff of Sulphur',
                       'Demons are best left alone'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        if 'RandomBlink' in playercreature.Special:
            playercreature.Special['RandomBlink'] += 3
        else:
            playercreature.Special['RandomBlink'] = 5
        Message('These sparkles should let you blink around! (ctrl + b)')
    if choice == 1:
        if 'PoisonResistance' in playercreature.Special:
            playercreature.Special['PoisonResistance'] += 10
        else:
            playercreature.Special['PoisonResistance'] = 25
        if 'Poisoned' in playercreature.Special:
            (turns, damage, sourceid) = playercreature.Special['Poisoned']
            turns += 1
            damage += 1
            playercreature.Special['Poisoned'] = (turns, damage, blueid)
        else:
            playercreature.Special['Poisoned'] = (3, 1, blueid)
        Message('Did you not notice they where poisioness?')
    if choice == 2:
        playerlevel = CM.get_Component('Level', config.PlayerId)
        playerlevel.level -= 3
        if playerlevel.level <= 0:
            playerlevel.level = 1
        config.xptolevel = int(config.xptolevel / config.xpscale /
                               config.xpscale / config.xpscale)
        if playercreature.BaseDefense < 10:
            playercreature.BaseDefense += 1
        if playercreature.BaseStrength < 10:
            playercreature.BaseStrength += 1
        if playercreature.BaseAgility < 10:
            playercreature.BaseAgility += 1
        Message('Smart choice but lose some levels! (it\'s a good thing)')


class Imp_AI:

    def __init__(self, impid):
        self.ImpId = impid
        self.BasicAttackId = EM.new_Id
        CM.add_Component(self.BasicAttackId, 'Attack',
                         Attack(2, 4, special={'CausePoison': (50, 3, 1)}))

    def take_turn(self):
        impcreature = CM.get_Component('Creature', self.ImpId)
        impcoord = CM.get_Component('Coord', self.ImpId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        levelid = config.DungeonLevelIds[config.CurrentDungeonLevel]
        level = CM.get_Component('DungeonLevel', levelid)
        seethrough = seethrough_map(level.MapId)
        disttoplayer = hypot(impcoord.X - playercoord.X,
                             impcoord.Y - playercoord.Y)
        if disttoplayer < impcreature.VisionRange:
            vision = config.fov.Coords_in_Sight(seethrough, impcoord.X,
                                                impcoord.Y,
                                                impcreature.VisionRange)
            if playercoord in vision:
                if int(disttoplayer) <= 1:
                    Attack_Coord(self.BasicAttackId, self.ImpId,
                                 playercoord)
                    MC.Walk_Direction_Persistantly(
                        self.ImpId, MC.Get_Direction_To(impcoord, playercoord))
                else:
                    MC.Blink_Random_Failable(self.ImpId, 0, 2)
