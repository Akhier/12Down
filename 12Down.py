from Play_Game import Play_Game
from New_Game import New_Game
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
    if config.game_state == 'Quit':
        choice = 1
    else:
        choice = Menu('', ['New game', 'Quit'], 14)
    if choice == 0:
        New_Game()
        Play_Game()
    elif choice == 1:
        break
