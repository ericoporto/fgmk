# -*- coding: utf-8 -*-
import json
import os.path
from os import listdir
from fgmk import fifl, current_project


def getLevelPathFromInitFile(gamefolder, levelname):
    initFile = openInitFile(gamefolder)
    return os.path.join(str(gamefolder), fifl.LEVELS, initFile['LevelsList'][str(levelname)])


def openInitFile(gamefolder):
    fname = os.path.join(str(gamefolder), fifl.DESCRIPTORS, fifl.GAMESETTINGS)

    if os.path.isfile(fname):
        f = open(fname, "r")
        initFileJsonTree = json.load(f)
        f.close()
        return initFileJsonTree
    else:
        return None

def playerInitCharaset():
    initJsonTree = getInitFile()
    return initJsonTree['Player']['charaSet']


def saveInitFile(gamefolder, initFileJsonTree):
    f = open(os.path.join(str(gamefolder),
                          fifl.DESCRIPTORS, fifl.GAMESETTINGS), "w")
    initFileJsonTree = json.dump(initFileJsonTree, f, indent=4, sort_keys=True)
    f.close()
    return initFileJsonTree


def getInitFile():
    gamefolder = os.path.join(current_project.settings["gamefolder"])
    if os.path.isdir(gamefolder):
        return openInitFile(gamefolder)
    else:
        return {}


def regenerateLevelList():
    initFileJsonTree = getInitFile()
    if 'LevelsList' not in initFileJsonTree:
        return

    gamefolder = os.path.join(current_project.settings["gamefolder"])

    if(initFileJsonTree != None):
        levels = os.path.join(gamefolder, fifl.LEVELS)
        filelist = [f for f in listdir(levels) if os.path.isfile(os.path.join(levels, f)) and f.endswith(".map.json")]
        originalLevelList = initFileJsonTree["LevelsList"]

        LevelsList = {}
        for file in filelist:
            filewoext = file.split(os.extsep, 1)[0]
            LevelsList[filewoext] = file

        unmatched_maps = set(LevelsList.items()) ^ set(originalLevelList.items())

        if(len(unmatched_maps)!=0):
            initFileJsonTree["LevelsList"] = []
            initFileJsonTree["LevelsList"] = LevelsList
            saveInitFile(gamefolder, initFileJsonTree)
            return True

        return False

def getAllVariables():
    # charas.json -> ['Charas'][charanames]['actions']['list']
    # *.map.json -> ['Level']['eventsActions'][events]
    return 'allvariables'
