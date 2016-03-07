from ComponentManager import ComponentManager as CM
from S_MapInfo import seethrough_map, char_map
import libtcodpy
import config
import Color


def Render():
    dungeonlevelid = config.DungeonLevelIds[config.CurrentDungeonLevel]
    dungeonlevel = CM.get_Component('DungeonLevel', dungeonlevelid)
    curmapid = dungeonlevel.MapId
    playercoord = CM.get_Component('Coord', config.PlayerId)
    playercreature = CM.get_Component('Creature', config.PlayerId)
    playertile = CM.get_Component('Tile', config.PlayerId)
    if config.fov_recompute:
        config.fov_recompute = False
        curmap = CM.get_Component('Map', curmapid)
        charmap = char_map(curmapid)
        config.visible = config.fov.Calculate_Sight(seethrough_map(curmapid),
                                                    playercoord.X,
                                                    playercoord.Y,
                                                    playercreature.VisionRange)
        for y in range(config.playscreen_height):
            for x in range(config.playscreen_width):
                s = CM.get_Component('Seen', curmap.TileIds[x][y])
                if not config.visible[x][y]:
                    if s.seen:
                        config.playscreen.write_ex(x, y, charmap[x][y],
                                                   Color.map_tile_seen)
                else:
                    config.playscreen.write_ex(x, y, charmap[x][y],
                                               Color.map_tile_visible)
                    s.seen = True
    for itemid in dungeonlevel.ItemIds:
        coord = CM.get_Component('Coord', itemid)
        x = coord.X
        y = coord.Y
        s = CM.get_Component('Seen', itemid)
        if config.visible[coord.X][coord.Y]:
            item = CM.get_Component('Tile', itemid)
            config.playscreen.write_ex(x, y, item.Char, item.Color)
            s.seen = True
        elif s.seen:
            config.playscreen.write_ex(x, y, '~', Color.map_tile_seen)
    for featureid in dungeonlevel.FeatureIds:
        coord = CM.get_Component('Coord', featureid)
        x = coord.X
        y = coord.Y
        s = CM.get_Component('Seen', featureid)
        if config.visible[coord.X][coord.Y] or s.seen:
            feature = CM.get_Component('Tile', featureid)
            config.playscreen.write_ex(x, y, feature.Char, feature.Color)
            s.seen = True
    for monsterid in dungeonlevel.MonsterIds:
        coord = CM.get_Component('Coord', monsterid)
        x = coord.X
        y = coord.Y
        if config.visible[coord.X][coord.Y]:
            monster = CM.get_Component('Tile', monsterid)
            config.playscreen.write_ex(x, y, monster.Char, monster.Color)
    config.playscreen.write_ex(playercoord.X, playercoord.Y,
                               playertile.Char, playertile.Color)
    config.messagescreen.clear
    y = 1
    for (line, messagecolor) in config.game_msgs:
        config.messagescreen.set_default_foreground(messagecolor)
        config.messagescreen.write(1, y, line)
        config.messagescreen.set_default_foreground(Color.white)
        y += 1
    render_bar(2, 2, config.statscreen_width - 4, 'HP', playercreature.CurHp,
               playercreature.MaxHp, Color.light_red, Color.darker_red)
    config.playscreen.blit()
    config.messagescreen.blit()
    config.statscreen.blit()


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)
    config.statscreen.set_default_background(back_color)
    config.statscreen.rect(x, y, total_width, 1, False,
                           flag=libtcodpy.BKGND_SET)
    config.statscreen.set_default_background(bar_color)
    if bar_width > 0:
        config.statscreen.rect(x, y, bar_width, 1, False,
                               flag=libtcodpy.BKGND_SET)
    config.statscreen.set_default_foreground(Color.white)
    config.statscreen.write(x + total_width / 2, y, name + ': ' +
                            str(value) + '/' + str(maximum),
                            align=config.CENTER)
