#!/usr/bin/env python
import libtcodpy as tcod


# ######################################################################
# Constants and Initial settings
# ######################################################################
# Size of the terminal window in characters
SCREEN_WIDTH = 80  # characters wide
SCREEN_HEIGHT = 50  # characters tall
LIMIT_FPS = 20  # 20 frames-per-second maximum


# Setup displayed font
font_filename = 'arial10x10.png'  # needs to be in same folder as this file
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
tcod.console_set_custom_font(font_filename, font_flags)


# Setup window
window_title = 'Python 3 libtcod tutorial'
fullscreen = False
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)


# Limit frames per second
tcod.sys_set_fps(LIMIT_FPS)


# Setup player's initial position
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2


# ######################################################################
# User Interface Control
# ######################################################################
def handle_keys():
    """Handles keyboard input

    Updates:
        player_x: x coordinate of player position
        player_y: y coordinate of player position

    Returns:
        bool: True if exit the game is requested else False
    """
    global player_x, player_y

    exit_game = False

    # key = tcod.console_check_for_keypress()  # real-time
    key = tcod.console_wait_for_keypress(True)  # turn-based

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    elif key.vk == tcod.KEY_ESCAPE:
        exit_game = True  # exit game

    # movement keys
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player_y = player_y - 1

    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player_y = player_y + 1

    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player_x = player_x - 1

    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player_x = player_x + 1

    return exit_game


# ######################################################################
# Main Game Loop
# ######################################################################
exit_game = False
while not tcod.console_is_window_closed() and exit_game is not True:
    tcod.console_set_default_foreground(0, tcod.white)
    tcod.console_put_char(0, player_x, player_y, '@', tcod.BKGND_NONE)
    tcod.console_flush()
    tcod.console_put_char(0, player_x, player_y, ' ', tcod.BKGND_NONE)

    # handle keys
    exit_game = handle_keys()
