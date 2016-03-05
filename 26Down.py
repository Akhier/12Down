from Console import Console
from Panel import Panel
import libtcodpy


gamewindow = Console(80, 50, '26Down - By Akhier Dragonheart')
playscreen = Panel(0, 0, 60, 40, border=True)
messagescreen = Panel(0, 40, 60, 10, border=True)
statscreen = Panel(60, 0, 20, 50, border=True)
while not gamewindow.is_window_closed:
    libtcodpy.console_wait_for_keypress(True)
    gamewindow.clear
    playscreen.blit()
    messagescreen.blit()
    statscreen.blit()
    gamewindow.flush
