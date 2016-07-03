import os.path
from os import listdir
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import actionDialog, TXWdgt, fifl, proj

def regenerateLevelList():
    psSettings = proj.settings
    gamefolder = os.path.join(psSettings["gamefolder"])
    if os.path.isdir(gamefolder):
        initFileJsonTree = TXWdgt.openInitFile(gamefolder)
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
            TXWdgt.saveInitFile(gamefolder, initFileJsonTree)
            return True

        return False


def selectStartingPosition(parent):
    psSettings = proj.settings
    gamefolder = os.path.join(psSettings["gamefolder"])
    initFileJsonTree = TXWdgt.openInitFile(gamefolder)

    if(initFileJsonTree != None):
        initx = int(initFileJsonTree["Player"]["initPosX"]/32)
        inity = int(initFileJsonTree["Player"]["initPosY"]/32+1)
        level = initFileJsonTree["World"]["initLevel"]
        edit = None
        if(level in initFileJsonTree["LevelsList"]):
            levelfilename = initFileJsonTree["LevelsList"][level]

            if os.path.isfile(os.path.join(gamefolder, fifl.LEVELS, levelfilename)):
                edit = [initx, inity, level]

        myTeleporDialog = actionDialog.teleport(
            psSettings["gamefolder"], parent, edit, False, "select starting position")
        if myTeleporDialog.exec_() == QtWidgets.QDialog.Accepted:
            returnActDlg = str(myTeleporDialog.getValue())
            position = returnActDlg.split(';')
            initFileJsonTree["Player"]["initPosX"] = int(position[0]) * 32
            initFileJsonTree["Player"]["initPosY"] = (int(position[1]) - 1) * 32
            if(str(position[2]) != "this"):
                initFileJsonTree["World"]["initLevel"] = str(position[2])
            else:
                initFileJsonTree["World"]["initLevel"] = str(
                    parent.myMap.levelName)
            return [initFileJsonTree, str(position[2])]
