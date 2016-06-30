from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import actionDialog, TXWdgt


def selectStartingPosition(parent, psSettings):
    myTeleporDialog = actionDialog.teleport(
        psSettings["gamefolder"], parent, None, False, "select starting position")
    if myTeleporDialog.exec_() == QtWidgets.QDialog.Accepted:
        returnActDlg = str(myTeleporDialog.getValue())
        position = returnActDlg.split(';')
        initFileJsonTree = TXWdgt.openInitFile(psSettings["gamefolder"])
        initFileJsonTree["Player"]["initPosX"] = int(position[0]) * 32
        initFileJsonTree["Player"]["initPosY"] = (int(position[1]) - 1) * 32
        if(str(position[2]) != "this"):
            initFileJsonTree["World"]["initLevel"] = str(position[2])
        else:
            initFileJsonTree["World"]["initLevel"] = str(
                parent.myMap.levelName)
        return [initFileJsonTree, str(position[2])]
