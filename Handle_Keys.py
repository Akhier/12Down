from Enum_Direction import Direction as Dir
from S_MoveCreature import Walk_Direction
from Menu import Menu
import libtcodpy
import config


def Handle_Keys():
    if config.key.vk == libtcodpy.KEY_ENTER and config.key.lalt:
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    elif config.key.vk == libtcodpy.KEY_ESCAPE:
        return 'exit'

    if config.game_state == 'playing':
        if config.key.vk == libtcodpy.KEY_UP or \
                config.key.vk == libtcodpy.KEY_KP8:
            if Walk_Direction(config.PlayerId, Dir.N):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_DOWN or \
                config.key.vk == libtcodpy.KEY_KP2:
            if Walk_Direction(config.PlayerId, Dir.S):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_LEFT or \
                config.key.vk == libtcodpy.KEY_KP4:
            if Walk_Direction(config.PlayerId, Dir.W):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_RIGHT or \
                config.key.vk == libtcodpy.KEY_KP6:
            if Walk_Direction(config.PlayerId, Dir.E):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_HOME or \
                config.key.vk == libtcodpy.KEY_KP7:
            if Walk_Direction(config.PlayerId, Dir.NW):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_PAGEUP or \
                config.key.vk == libtcodpy.KEY_KP9:
            if Walk_Direction(config.PlayerId, Dir.NE):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_END or \
                config.key.vk == libtcodpy.KEY_KP1:
            if Walk_Direction(config.PlayerId, Dir.SW):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_PAGEDOWN or \
                config.key.vk == libtcodpy.KEY_KP3:
            if Walk_Direction(config.PlayerId, Dir.SE):
                config.fov_recompute = True
        elif config.key.vk == libtcodpy.KEY_KP5:
            pass

        # else:
        #     key_char = chr(config.key.c)

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

            # if key_char == '<':
            #     if config.stairs.x == config.player.x and \
            #             config.stairs.y == config.player.y:
            #         next_level()

            return 'didnt-take-turn'


def msgbox(text, width=50):
    Menu(text, [], width)
