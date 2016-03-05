from Console import Console
import libtcodpy


gamewindow = Console(80, 50, '26Down - By Akhier Dragonheart')
while not gamewindow.is_window_closed:
    libtcodpy.console_wait_for_keypress(True)
