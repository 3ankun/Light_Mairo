SCREEN_HEIGHT = 600
SCREEN_WIDTH = 801

SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

ORIGINAL_CAPTION = "SuperMario"

GFX = None

## COLORS ##

#            R    G    B
GRAY         = (100, 100, 100)
NAVYBLUE     = ( 60,  60, 100)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
FOREST_GREEN = ( 31, 162,  35)
BLUE         = (  0,   0, 255)
YELLOW       = (255, 255,   0)
ORANGE       = (255, 128,   0)
PURPLE       = (255,   0, 255)
CYAN         = (  0, 255, 255)
BLACK        = (  0,   0,   0)
NEAR_BLACK    = ( 19,  15,  48)
COMBLUE      = (233, 232, 255)
GOLD         = (255, 215,   0)

BGCOLOR = WHITE

SIZE_MULTIPLIER = 2.5

STAND = 'standing'
WALK = 'walk'
JUMP = 'jump'
FALL = 'fall'

SMALL_ACCEL = .2
SMALL_TURNAROUND = .35

GRAVITY = .4
JUMP_GRAVITY = .2

JUMP_VEL = -8

BACK_SIZE_MULTIPLER = 2.679
GROUND_HEIGHT = SCREEN_HEIGHT - 62

import os
import pygame as pg

# 音效资源容器
SOUNDS = {}

# 音效加载函数
def load_sounds(directory, accept=(".wav", ".mp3", ".ogg")):
    sounds = {}
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        if ext.lower() in accept:
            path = os.path.join(directory, file)
            sounds[name] = pg.mixer.Sound(path)
    return sounds