from ComponentManager import ComponentManager as CM
from S_CreateStairs import create_stairs
import S_PlaceMonsters as PM
import S_MoveCreature as MC
from Message import Message
from C_Flags import Seen
import random
import config
import Color


def Attack_Creature(attackid, attackerid, defenderid):
    attack = CM.get_Component('Attack', attackid)
    attacker = CM.get_Component('Creature', attackerid)
    defender = CM.get_Component('Creature', defenderid)
    attackertile = CM.get_Component('Tile', attackerid)
    defendertile = CM.get_Component('Tile', defenderid)
    attackercoord = CM.get_Component('Coord', attackerid)
    defendercoord = CM.get_Component('Coord', defenderid)
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
    if 'PlusAgility' in attack.Special:
        agimod += attack.Special['PlusAgility']
    baseroll = random.randint(1, 20)
    roll = baseroll + agimod
    dodge = False
    if roll > 10 and 'Dodge' in defender.Special:
        dodgechance = defender.Special['Dodge']
        chance = random.randint(1, 100)
        if chance <= dodgechance:
            direction = MC.Get_Direction_To(attackercoord, defendercoord)
            dodge = MC.Walk_Direction(defenderid, direction)
            if dodge:
                if defenderid == config.PlayerId:
                    Message('You dodge the ' + attackertile.TileName +
                            '\'s attack!',
                            color=Color.yellow)
                else:
                    Message('The ' + defendertile.TileName +
                            ' dodges your attack!',
                            color=Color.light_red)
    if (roll > 10 or baseroll == 20) and not dodge and baseroll != 1:
        damageroll = 0
        for i in range(attack.Dice):
            damageroll = random.randint(1, attack.Sides)
        damage = int(damageroll * strmod)
        if damage < 1:
            damage = 1
        crithappend = False
        if 'CritChance' in attacker.Special:
            critmod = 1
            if 'ReduceCrit' in defender.Special:
                critmod = critmod * (defender.Special['ReduceCrit'] / 100)
            if random.randint(1, 100) <= attacker.Special['CritChance']:
                damage = damage * (critmod + 1)
                crithappend = True

        for i in range(defender.Defense):
            if damage > 0:
                chance = random.randint(1, 100)
                percentchance = 25
                if 'EnhancedDefense' in defender.Special:
                    percentchance += defender.Special['EnhancedDefense']
                if 'PierceDefense' in attack.Special:
                    percentchance -= attack.Special['PierceDefense']
                if chance <= percentchance:
                    damage -= 1
            if damage <= 0:
                damage = 0
                break
        defender.CurHp -= damage
        if damage > 0 and 'Poison' in attack.Special:
            (percentchance, turns, damage) = attack.Special['Poison']
            chance = random.randint(1, 100)
            modpercentchance = 0
            if 'PoisonResistance' in defender.Special:
                modpercentchance = defender.Special['PoisonResistance']
            if percentchance <= 0:
                if defenderid == config.PlayerId:
                    Message('You completely resist the poison!',
                            color=Color.yellow)
                else:
                    Message('The ' + defender.TileName +
                            ' completely resists the poison!',
                            color=Color.yellow)
            if chance <= percentchance:
                if chance > percentchance - modpercentchance:
                    if defenderid == config.PlayerId:
                        Message('You resist the poison!',
                                color=Color.yellow)
                    else:
                        Message('The ' + defender.TileName +
                                ' resists the poison!',
                                color=Color.yellow)
                else:
                    if 'Poisoned' in defender.Special:
                        (turnsleft, damageturn, sourceid) = defender.Special[
                            'Poisoned']
                        if damageturn > damage:
                            newdamage = damageturn
                        else:
                            newdamage = damage
                        if turnsleft > turns:
                            newturns = turnsleft
                        else:
                            newturns = turns
                        defender.Special['Poisoned'] = (
                            newturns, newdamage, attackerid)
                    else:
                        newturns = turns
                        newdamage = damage
                        defender.Special['Poisoned'] = (
                            newturns, newdamage, attackerid)
                    if defenderid == config.PlayerId:
                        Message('You are now poisoned for ' +
                                str(newturns) + ' turns!',
                                color=Color.dark_green)
                    else:
                        Message('The ' + defender.TileName +
                                ' has been poisoned!',
                                color=Color.dark_green)
        if damage > 0 and 'LifeDrain' in attack.Special:
            drain = attack.Special['LifeDrain']
            if drain < damage:
                attacker.CurHp += drain
            else:
                attacker.CurHp += damage
            if attacker.CurHp > attacker.MaxHp * 2:
                attacker.CurHp = attacker.MaxHp * 2
        hit = 'hit'
        if crithappend:
            hit = 'crit'
        if attackerid == config.PlayerId:
            if damage > 0:
                Message('You ' + hit + ' the ' + defendertile.TileName +
                        ' for ' + str(damage) + '!', color=Color.sky)
            else:
                Message('You hit the ' + defendertile.TileName +
                        ' but deal no damage', color=Color.light_red)
        elif defenderid == config.PlayerId:
            if damage > 0:
                Message('The ' + attackertile.TileName + ' ' + hit +
                        's you for ' + str(damage) + '!', color=Color.red)
            else:
                Message('The ' + attackertile.TileName +
                        ' hits you but deals no damage!', color=Color.yellow)
        check_death(attackerid, defenderid)

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
    idtoattacks = []
    for key, value in coords.iteritems():
        if value == coordtoattack and key in creatures:
            idtoattacks.append(key)
    for key in idtoattacks:
        Attack_Creature(attackid, attackerid, key)


def check_death(attackerid, defenderid):
    attacker = CM.get_Component('Creature', attackerid)
    defender = CM.get_Component('Creature', defenderid)
    if defender.CurHp <= 0:
        attacker.Xp += defender.Xp
        if 'LifeSaver' in defender.Special:
            defender.Special['LifeSaver'] -= 1
            if defender.Special['LifeSaver'] <= 0:
                defender.Special.pop('LifeSaver', None)
            defender.CurHp = defender.MaxHp
            if 'Poisoned' in defender.Special:
                defender.Special.pop('Poisoned', None)
            MC.Teleport_Random(defenderid)
        else:
            dungeonlevelid = config.DungeonLevelIds[
                config.CurrentDungeonLevel]
            dungeonlevel = CM.get_Component('DungeonLevel', dungeonlevelid)
            dungeonlevel.MonstersKilled += 1
            defenderdeath = CM.get_Component('Death', defenderid)
            for effect in defenderdeath.Effects:
                effect(defenderid)
            if defenderid in dungeonlevel.MonsterIds:
                dungeonlevel.MonsterIds.remove(defenderid)
                dungeonlevel.FeatureIds.append(defenderid)
                CM.add_Component(defenderid, 'Seen', Seen(seen=True))
            if dungeonlevel.MonstersKilled >= 10 and \
                    not dungeonlevel.StairsPresent:
                dungeonlevel.StairsPresent = True
                create_stairs(dungeonlevelid)
                Message('After having slayed many a monster the stairs ' +
                        'have magically appeared at the center!',
                        color=Color.gold)
            elif dungeonlevel.MonstersKilled == 5:
                PM.Place_Boss(dungeonlevel)
                Message('A strong presence can now be felt in the Dungeon',
                        color=Color.light_purple)
