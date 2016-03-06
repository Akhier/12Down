from Menu import Menu
import libtcodpy
import config
import Color


def Handle_Keys():
    if config.key.vk == libtcodpy.KEY_ENTER and config.key.lalt:
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    elif config.key.vk == libtcodpy.KEY_ESCAPE:
        return 'exit'

    if config.game_state == 'playing':
        if config.key.vk == libtcodpy.KEY_UP or \
                config.key.vk == libtcodpy.KEY_KP8:
            player_move_or_attack(0, -1)
        elif config.key.vk == libtcodpy.KEY_DOWN or \
                config.key.vk == libtcodpy.KEY_KP2:
            player_move_or_attack(0, 1)
        elif config.key.vk == libtcodpy.KEY_LEFT or \
                config.key.vk == libtcodpy.KEY_KP4:
            player_move_or_attack(-1, 0)
        elif config.key.vk == libtcodpy.KEY_RIGHT or \
                config.key.vk == libtcodpy.KEY_KP6:
            player_move_or_attack(1, 0)
        elif config.key.vk == libtcodpy.KEY_HOME or \
                config.key.vk == libtcodpy.KEY_KP7:
            player_move_or_attack(-1, -1)
        elif config.key.vk == libtcodpy.KEY_PAGEUP or \
                config.key.vk == libtcodpy.KEY_KP9:
            player_move_or_attack(1, -1)
        elif config.key.vk == libtcodpy.KEY_END or \
                config.key.vk == libtcodpy.KEY_KP1:
            player_move_or_attack(-1, 1)
        elif config.key.vk == libtcodpy.KEY_PAGEDOWN or \
                config.key.vk == libtcodpy.KEY_KP3:
            player_move_or_attack(1, 1)
        elif config.key.vk == libtcodpy.KEY_KP5:
            pass

        else:
            key_char = chr(config.key.c)

            # if key_char == 'g':
            #     for object in config.objects:
            #         if object.x == config.player.x and \
            #            object.y == config.player.y and object.item:
            #             object.item.pick_up()
            #             break

            # if key_char == 'i':
            #     chosen_item = inventory_menu('Press the key next to an ' +
            #                                  'item to use it, or any ' +
            #                                  'other to cancel.\n')
            #     if chosen_item is not None:
            #         chosen_item.use()

            # if key_char == 'd':
            #     chosen_item = inventory_menu('Press the key next to an ' +
            #                                  'to drop it, or any ' +
            #                                  'other to cancel.\n')
            #     if chosen_item is not None:
            #         chosen_item.drop()

            if key_char == 'c':
                level_up_xp = config.LEVEL_UP_BASE + \
                    config.player.level * \
                    config.LEVEL_UP_FACTOR
                msgbox('Character information\n\nLevel: ' +
                       str(config.player.level) +
                       '\nExperiance: ' + str(config.player.fighter.xp) +
                       '\nExperiance to level up: ' + str(level_up_xp) +
                       '\nMaximum HP: ' + str(config.player.fighter.max_hp) +
                       '\nAttack: ' + str(config.player.fighter.power) +
                       '\nDefense: ' + str(config.player.fighter.defense),
                       config.CHARACTER_SCREEN_WIDTH)

            # if key_char == '<':
            #     if config.stairs.x == config.player.x and \
            #             config.stairs.y == config.player.y:
            #         next_level()

            return 'didnt-take-turn'


def msgbox(text, width=50):
    Menu(text, [], width)
