from ComponentManager import ComponentManager as CM
from S_DistanceBetweenCoords import get_distance
from S_CoordtoCoordFov import coord_to_coord_fov
from EntityManager import EntityManager as EM
from C_Death import Death, death_cleanup
from S_Combat import Attack_Coord
from C_Creature import Creature
from C_Attack import Attack
from Message import Message
import S_MoveCreature as MC
from C_Tile import Tile
from Menu import Menu
import config
import Color


def make_lion(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Lion', 'l', False, True,
                          color=Color.yellow))
    CM.add_Component(newmonsterid, 'Death',
                     Death('Dead on the floor a lion lays.',
                           '~', effects=[death_cleanup]))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(30, 2, 10, 15, 6, 81))
    CM.add_Component(newmonsterid, 'Action', Lion_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def make_dire_lion(coord, dungeonlevel):
    newmonsterid = EM.new_Id()
    CM.add_Component(newmonsterid, 'Coord', coord)
    CM.add_Component(newmonsterid, 'Tile',
                     Tile('Dire Lion', 'L', False, True,
                          color=Color.dark_yellow))
    deatheffects = [death_cleanup, dire_choice]
    CM.add_Component(newmonsterid, 'Death',
                     Death('The Dire Lions no longer able to support ' +
                           'itself slumps to the ground.',
                           '~', effects=deatheffects))
    CM.add_Component(newmonsterid, 'Creature',
                     Creature(30, 6, 12, 20, 6, 324))
    CM.add_Component(newmonsterid, 'Action', Lion_AI(newmonsterid))
    dungeonlevel.MonsterIds.append(newmonsterid)


def dire_choice(direid):
    choice = None
    while choice is None:
        choice = Menu('The Dire and dead, only 2 letters ' +
                      'different now the same. ' +
                      'Now claim your reward!',
                      ['You could probably sharpen your weapon on its bones',
                       'Maybe reinforce your gear with its fur?',
                       'How about a collar made of it\'s mane'], 60)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    if choice == 0:
        playerattack = CM.get_Component('Attack', config.PlayerAttack)
        playerattack.Dice += 1
        playerattack.Sides -= 1
        if 'PierceDefense' in playerattack.Special:
            playerattack.Special['PierceDefense'] += 5
        else:
            playerattack.Special['PierceDefense'] = 10
        Message('Well that improves things')
    if choice == 1:
        if 'EnhancedDefense' in playercreature.Special:
            playercreature.Special['EnhancedDefense'] += 10
        else:
            playercreature.Special['EnhancedDefense'] = 20
        if playercreature.BaseDefense < 10:
            playercreature.BaseDefense += 2
        else:
            playercreature.BaseDefense += 1
        Message('Just a bit more defensive')
    if choice == 2:
        playercreature['Fear'] = 5
        Message('With this things might fear you. That\'s a good thing!')


class Lion_AI:

    def __init__(self, lionid):
        self.LionId = lionid
        self.BasicAttackId = EM.new_Id
        tile = CM.get_Component('Tile', lionid)
        if tile.TileName == 'Lion':
            CM.add_Component(self.BasicAttackId, 'Attack', Attack(2, 6))
        else:
            CM.add_Component(self.BasicAttackId, 'Attack',
                             Attack(2, 6, special={'PierceDefense': 10}))
        self.playerinvision = False

    def take_turn(self):
        lioncreature = CM.get_Component('Creature', self.LionId)
        lioncoord = CM.get_Component('Coord', self.LionId)
        playercoord = CM.get_Component('Coord', config.PlayerId)
        disttoplayer = get_distance(lioncoord, playercoord)
        if disttoplayer <= lioncreature.VisionRange and \
                not self.playerinvision:
            self.playerinvision = coord_to_coord_fov(lioncoord, playercoord)
        if self.playerinvision:
            if disttoplayer <= lioncreature.VisionRange:
                if int(disttoplayer) <= 1:
                    Attack_Coord(self.BasicAttackId, self.LionId,
                                 playercoord)
                else:
                    direction = MC.Get_Direction_To(lioncoord, playercoord)
                    MC.Walk_Direction_Persistantly(self.LionId, direction)
            else:
                self.lion_else(lioncreature, lioncoord)
        else:
            self.lion_else(lioncreature, lioncoord)

    def lion_else(self, lioncreature, lioncoord):
        coord = CM.dict_of('Coord')
        tile = CM.dict_of('Tile')
        dist = (lioncreature.VisionRange, False)
        for key, coord in coord.iteritems():
            if get_distance(coord, lioncoord) <= \
                lioncreature.VisionRange and key != self.LionId and \
                    (tile[key].TileName == 'Lion' or
                        tile[key].TileName == 'Dire Lion'):
                newdist = get_distance(lioncoord, coord)
                if newdist < dist:
                    dist = (newdist, coord)
        if dist[1]:
            if dist[0] < 2:
                direction = MC.Get_Direction_To(dist[1], lioncoord)
            else:
                direction = MC.Get_Direction_To(lioncoord, dist[1])
            MC.Walk_Direction_Persistantly(self.LionId, direction)
