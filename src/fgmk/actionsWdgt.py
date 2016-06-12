import sys
import json
import os.path
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
from fgmk import tMat, actionDialog, TileXtra, fifl


class ActionsWidget(QDialog):

    def __init__(self, psSettings, parent=None, ischaras=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.psSettings = psSettings
        self.ischaras = ischaras

        self.VBox = QVBoxLayout(self)
        self.VBox.setAlignment(Qt.AlignTop)

        filepath = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "actions/actionsList.json")
        f = open(filepath, "r")
        e = json.load(f)
        f.close()

        self.parent = parent
        self.actionButton = []

        for action in e["actionList"]:
            self.actionButton.append(QPushButton(action, self))
            self.VBox.addWidget(self.actionButton[-1])
            self.actionButton[-1].clicked.connect(self.getAction)

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Select Action to add...')

        self.show()

    def getAction(self):

        buttonThatSent = self.sender()
        self.returnValue = buttonThatSent.text()

        if(self.returnValue == "END" or self.returnValue == "ELSE"):
            self.returnValue = [str(self.returnValue), ""]
            self.accept()
        else:
            newDialogFromName = getattr(actionDialog, str(self.returnValue))
            if(self.ischaras is False):
                self.myActionsDialog = newDialogFromName(
                    self.psSettings["gamefolder"], self)
            else:
                self.myActionsDialog = newDialogFromName(
                    self.psSettings["gamefolder"], self, None, True)

            if self.myActionsDialog.exec_() == QtWidgets.QDialog.Accepted:
                returnActDlg = str(self.myActionsDialog.getValue())

                # self.returnValue.append('|')
                self.returnValue = [str(self.returnValue), str(returnActDlg)]
                self.accept()

    def getValue(self):
        return self.returnValue
