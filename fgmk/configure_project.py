# -*- coding: utf-8 -*-
import os.path
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import game_init, action_dialog, current_project, fifl

def selectStartingPosition(parent):
    psSettings = current_project.settings
    gamefolder = os.path.join(psSettings["gamefolder"])
    initFileJsonTree = game_init.openInitFile(gamefolder)

    if(initFileJsonTree != None):
        initx = int(initFileJsonTree["Player"]["initPosX"]/32)
        inity = int(initFileJsonTree["Player"]["initPosY"]/32+1)
        level = initFileJsonTree["World"]["initLevel"]
        edit = None
        if(level in initFileJsonTree["LevelsList"]):
            levelfilename = initFileJsonTree["LevelsList"][level]

            if os.path.isfile(os.path.join(gamefolder, fifl.LEVELS, levelfilename)):
                edit = [initx, inity, level]

        myTeleporDialog = action_dialog.teleport(
            gamefolder=psSettings["gamefolder"],
            parent=parent,
            edit=edit,
            nothis=False, 
            selectStartPosition="select starting position")
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
