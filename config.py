from S_RecursiveShadowCasting import Fov_RSC
from S_MakeMap import MapGen
from Console import Console
from Panel import Panel
import libtcodpy


Id = []
Component = {}
window_width = 80
window_height = 50
window_title = '26Down - By Akhier Dragonheart'
playscreen_width = int(window_width * .75)
playscreen_height = int(window_height * .8)
playscreen_x = 0
playscreen_y = 0
messagescreen_width = playscreen_width
messagescreen_height = window_height - playscreen_height
messagescreen_x = playscreen_x
messagescreen_y = playscreen_height
statscreen_width = window_width - playscreen_width
statscreen_height = window_height
statscreen_x = playscreen_width
statscreen_y = playscreen_y
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
mapgen = MapGen(playscreen_width, playscreen_height)
CENTER = libtcodpy.CENTER
LEFT = libtcodpy.LEFT
RIGHT = libtcodpy.RIGHT
