from ComponentManager import ComponentManager as CM
from Message import Message
import random
import config
import Color


def Attack_Creature(attackid, attackerid, defenderid):
    attack = CM.get_Component('Attack', attackid)
    attacker = CM.get_Component('Creature', attackerid)
    defender = CM.get_Component('Creature', defenderid)
    attackertile = CM.get_Component('Tile', attackerid)
    defendertile = CM.get_Component('Tile', defenderid)
    tempstr = int(attacker.Strength)
    tempnum = 0
    strmod = 0.0
    while tempstr > 0:
        tempnum += 10
        if tempstr > 10:
            strmod = 10 / tempnum + strmod
        else:
            strmod = tempstr / tempnum + strmod
        tempstr = tempstr - 10
    agimod = attacker.Agility - defender.Agility
    roll = random.randint(1, 20) + agimod
    if roll > 10:
        damageroll = random.randint(attack.MinDamage,
                                    attack.MaxDamage)
        damage = int(damageroll * strmod)
        for i in range(defender.Defense):
            if damage > 0:
                chance = random.randint(1, 100)
                if chance <= 25:
                    damage -= 1
            if damage <= 0:
                damage = 0
                break
        defender.CurHp -= damage
        if attackerid == config.PlayerId:
            if damage > 0:
                Message('You hit the ' + defendertile.TileName + ' for ' +
                        str(damage) + '!', color=Color.sky)
            else:
                Message('You hit the ' + defendertile.TileName +
                        ' but deal no damage', color=Color.light_red)
        elif defenderid == config.PlayerId:
            if damage > 0:
                Message('The ' + attackertile.TileName + ' hits you for ' +
                        str(damage) + '!', color=Color.red)
            else:
                Message('The ' + attackertile.TileName +
                        ' hits you but deals no damage!', color=Color.sky)
        if defender.CurHp <= 0:
            Message('The ' + defendertile.TileName + ' Dies!',
                    color=Color.darker_red)
    else:
        if attackerid == config.PlayerId:
            Message('You miss the ' + defendertile.TileName + '!')
        elif defenderid == config.PlayerId:
            Message('The ' + attackertile.TileName + ' misses you.')
        else:
            Message('The ' + attackertile.TileName + ' misses the ' +
                    defendertile.TileName + '.')


def Attack_Coord(attackid, attackerid, coordtoattack):
    coords = CM.dict_of('Coord')
    creatures = CM.dict_of('Creature')
    for key, value in coords.iteritems():
        if value == coordtoattack and key in creatures:
            Attack_Creature(attackid, attackerid, key)
