from Color import light_red
from Menu import Menu
import config


while not config.gamewindow.is_window_closed:
    config.gamewindow.set_default_foreground(light_red)
    config.gamewindow.write(config.window_width / 2,
                            config.window_height / 2 - 4,
                            '26Down', align=config.CENTER)
    config.gamewindow.write(config.window_width / 2,
                            config.window_height - 2,
                            'By Akhier', align=config.CENTER)
    choice = Menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)
    if choice == 0:
        pass   # New Game then Play Game
    if choice == 1:
        pass   # try Load Game except Menu error then Play Game
    elif choice == 2:
        break
