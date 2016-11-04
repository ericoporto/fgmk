# -*- coding: utf-8 -*-
"""
Contains the paths expected for game assets
"""

import os

DESCRIPTORS = os.path.join("descriptors")
LEVELS = os.path.join(DESCRIPTORS, "levels")
IMG = os.path.join("img")
AUDIO = os.path.join("audio")
MUSIC = os.path.join(AUDIO, "music")
CHARASETS = os.path.join(DESCRIPTORS, "charaset")
FONT = os.path.join("font")

GAMESETTINGS = 'init.json'
CHARAS = 'charas.json'

ITEMS = 'items.json'

ITEMSFILE = os.path.join(DESCRIPTORS,ITEMS)

INITFILE = os.path.join(DESCRIPTORS,GAMESETTINGS)
