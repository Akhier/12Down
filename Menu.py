from Panel import Panel
import libtcodpy
import config


def Menu(header, options, width):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options')
    header_height = libtcodpy.console_get_height_rect(0, 0, 0,
                                                      config.window_width,
                                                      config.window_height,
                                                      header)
    if header == '':
        header_height = 0
    height = len(options) + header_height
    menupanel = Panel(0, 0, width, height)
    menupanel.write_wrap_ex(0, 0, width, height, header, libtcodpy.LEFT)
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        menupanel.write(0, y, text)
        y += 1
        letter_index += 1

    x = config.window_width / 2 - width / 2
    y = config.window_height / 2 - height / 2
    menupanel.blit(xdst=x, ydst=y, bfade=0.7)

    config.gamewindow.flush
    key = libtcodpy.console_wait_for_keypress(True)

    if key.vk == libtcodpy.KEY_ENTER and key.lalt:
        libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())

    index = key.c - ord('a')
    if index >= 0 and index < len(options):
        return index
    return None
