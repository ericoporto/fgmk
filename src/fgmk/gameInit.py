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


def saveInitFile(gamefolder, initFileJsonTree):
    f = open(os.path.join(str(gamefolder),
                          fifl.DESCRIPTORS, fifl.GAMESETTINGS), "w")
    initFileJsonTree = json.dump(initFileJsonTree, f, indent=4, sort_keys=True)
    f.close()
    return initFileJsonTree


def regenerateLevelList():
    psSettings = current_project.settings
    gamefolder = os.path.join(psSettings["gamefolder"])
    if os.path.isdir(gamefolder):
        initFileJsonTree = openInitFile(gamefolder)
    else:
        return

    if(initFileJsonTree != None):
        levels = os.path.join(gamefolder, fifl.LEVELS)
        filelist = [f for f in listdir(levels) if os.path.isfile(os.path.join(levels, f))]
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
