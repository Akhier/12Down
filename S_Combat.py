from ComponentManager import ComponentManager as CM
import random


def Attack_Creature(attackid, attackerid, defenderid):
    attack = CM.get_Component('Attack', attackid)
    attacker = CM.get_Component('Creature', attackerid)
    defender = CM.get_Component('Creature', defenderid)
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
                if chance <= 50:
                    damage -= 1
            if damage <= 0:
                damage = 0
                break
        defender.CurHp -= damage
        if defender.CurHp <= 0:
            pass   # Make Creature Die Here


def Attack_Coord(attackid, attackerid, coordtoattack):
    coords = CM.dict_of('Coord')
    creatures = CM.dict_of('Creature')
    for key, value in coords.iteritems():
        if value == coordtoattack and key in creatures:
            Attack_Creature(attackid, attackerid, key)
