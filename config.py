from S_RecursiveShadowCasting import Fov_RSC
from S_MakeMap import MapGen
from Console import Console
from Panel import Panel
import libtcodpy


DungeonLevelIds = []
CurrentDungeonLevel = 0
PlayerId = False
PlayerAttack = False
game_msgs = []
window_width = 80
window_height = 50
window_title = '26Down - By Akhier Dragonheart'
playscreen_width = int(window_width * .75)
playscreen_height = int(window_height * .8)
playscreen_x = 0
playscreen_y = 0
visible = []
messagescreen_width = playscreen_width
messagescreen_height = window_height - playscreen_height
messagescreen_x = playscreen_x
messagescreen_y = playscreen_height
message_width = messagescreen_width - 2
message_height = messagescreen_height - 2
statscreen_width = window_width - playscreen_width
statscreen_height = window_height
statscreen_x = playscreen_width
statscreen_y = playscreen_y
xptolevel = 66.6
xpscale = 1.5
gamewindow = Console(window_width, window_height,
                     window_title)
playscreen = Panel(playscreen_x, playscreen_y,
                   playscreen_width, playscreen_height)
messagescreen = Panel(messagescreen_x, messagescreen_y,
                      messagescreen_width, messagescreen_height,
                      border=True)
statscreen = Panel(statscreen_x, statscreen_y,
                   statscreen_width, statscreen_height,
                   border=True)
fov = Fov_RSC(playscreen_width, playscreen_height)
fov_recompute = True
mapgen = MapGen(playscreen_width, playscreen_height)
player_action = None
game_state = False
mouse = False
key = False
CENTER = libtcodpy.CENTER
LEFT = libtcodpy.LEFT
RIGHT = libtcodpy.RIGHT
