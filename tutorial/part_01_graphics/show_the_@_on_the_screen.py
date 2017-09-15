#!/usr/bin/env python
import libtcodpy as tcod

# Size of the terminal window in characters
SCREEN_WIDTH = 80  # characters wide
SCREEN_HEIGHT = 50  # characters tall

LIMIT_FPS = 20  # 20 frames-per-second maximum

# Setup displayed font
font_filename = 'arial10x10.png'
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
tcod.console_set_custom_font(font_filename, font_flags)

# Setup window
window_title = 'python/libtcod tutorial'
fullscreen = False
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)

# Limit frames per second
tcod.sys_set_fps(LIMIT_FPS)

# Game loop
while not tcod.console_is_window_closed():
    tcod.console_set_default_foreground(0, tcod.white)
    tcod.console_put_char(0, 1, 1, '@', tcod.BKGND_NONE)
    tcod.console_flush()
