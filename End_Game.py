from ComponentManager import ComponentManager as CM
from Panel import Panel
import libtcodpy
import config


def Menu(header, options, width):
    pass


def End_Game(finished=False):
    header = ''
    PC = CM.get_Component('Creature', config.PlayerId)
    PL = CM.get_Component('Level', config.PlayerId)
    PA = CM.get_Component('Attack', config.PlayerAttack)
    if finished:
        header = '\n\nYou completed the dungeon! Congradulations ' + \
            config.PlayerName
    else:
        header = '\n\nSadly you died in the dungeon. ' +\
            'Better luck next time ' + \
            config.PlayerId
    header += '\n\nDungeon Level: ' + config.CurrentDungeonLevel + \
        '\nLevel: ' + str(PL.level) + \
        '   Max Hp: ' + str(PC.MaxHp) + \
        '   Defense: ' + str(PC.Defense) + \
        '   Strength: ' + str(PC.Strength) + \
        '   Agility: ' + str(PC.Agility) + '\n'
    statlst = []
    atcklst = []
    atcklst.append('Attack: ' + str(PA.Dice) + 'd' + str(PA.Sides))
    if 'LifeDrain' in PA.Special:
        atcklst.append('   Life Drain: ' + str(PA.Special['LifeDrain']))
    if 'Paralyze' in PA.Special:
        atcklst.append('   Paralyze: %' + str(PA.Special['Paralyze']))
    if 'PierceDefense' in PA.Special:
        atcklst.append('   Pierce Defense: %' +
                       str(PA.Special['PierceDefense']))
    if 'CausePoison' in PA.Special:
        (percent, turns, damage) = PA.Special['CausePoison']
        atcklst.append('   Poison: %' + str(percent) + ' T' + str(turns) +
                       ' D' + str(damage))
    if 'EnhancedDefense' in PC.Special:
        statlst.append('   Enhanced Defense: %' +
                       str(PC.Special['EnhancedDefense']))
    if 'SideSwipe' in PC.Special:
        statlst.append('   Side Swipe Attack')
    if 'Dodge' in PC.Special:
        statlst.append('   Dodge: %' + str(PC.Special['Dodge']))
    if 'ParalyzeResistance' in PC.Special:
        statlst.append('   Paralyze Resistance: %' +
                       str(PC.Special['ParalyzeResistance']))
    if 'CritChance' in PC.Special:
        statlst.append('   Crit Chance: %' + str(PC.Special['CritChance']))
    if 'ReduceCrit' in PC.Special:
        statlst.append('   Reduce Crit: %' + str(PC.Special['ReduceCrit']))
    if 'Fear' in PC.Special:
        statlst.append('   Fear: %' + str(PC.Special['Fear']))
    if 'RandomBlink' in PC.Special:
        statlst.append('   Blink Uses: ' + str(PC.Special['RandomBlink']))
    if 'HealthPotion' in PC.Special:
        statlst.append('   Health Potions: ' + str(PC.Special['HealthPotion']))
    if 'LifeSaver' in PC.Special:
        statlst.append('   %$#: @')
    if 'CardinalLeap' in PC.Special:
        (need, current, distance) = PC.Special['CardinalLeap']
        statlst.append('   Leap: E' + str(need) + ' Dist' + str(distance))
    for item in atcklst:
        header += item
    header += '\n\n'
    cur = 1
    for item in statlst:
        if cur < 3:
            cur += 1
            header += item
        else:
            cur = 1
            header += item + '\n'
    if cur != 1:
        header += '\n'
    width = config.window_width
    options = ['Main Menu', 'Quit']
    header_height = libtcodpy.console_get_height_rect(0, 0, 0,
                                                      config.window_width,
                                                      config.window_height,
                                                      header)
    height = len(options) + header_height
    endpanel = Panel(0, 0, width, height)
    endpanel.write_wrap_ex(0, 0, width, height, header, libtcodpy.LEFT)
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        endpanel.write(0, y, text)
        y += 1
        letter_index += 1
    x = config.window_width / 2 - width / 2
    y = config.window_height / 2 - height / 2
    endpanel.blit(xdst=x, ydst=y, bfade=0.7)
    config.gamewindow.flush
    filename = config.PlayerName
    keepcharacters = (' ', '.', '_')
    filename = "".join(
        c for c in filename if c.isalnum() or c in keepcharacters).rstrip()
    if filename == '':
        filename = 'Empty'
    if finished:
        filename += '\'s Victory Monument'
    else:
        filename += '\'s Tombstone'
    with open(filename + '.txt', mode='w') as f:
        f.write(header)
    choice = None
    while choice is None:
        key = libtcodpy.console_wait_for_keypress(True)
        if key.vk == libtcodpy.KEY_ENTER and key.lalt:
            libtcodpy.console_set_fullscreen(
                not libtcodpy.console_is_fullscreen())

        index = key.c - ord('a')

        if index >= 0 and index < len(options):
            choice = index
    if choice == 0:
        config.game_state = 'finished'
    elif choice == 1:
        config.game_state = 'Quit'
