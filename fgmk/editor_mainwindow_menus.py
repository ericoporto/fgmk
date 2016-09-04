# -*- coding: utf-8 -*-
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import tMat, fifl, current_project, miniWdgt
from fgmk.util.layer_logic import COLISIONLAYER as COLISIONLAYER
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER
import os
from os import listdir
import platform
import subprocess

def openFolder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


class newProject(QtWidgets.QDialog):
    """
    The New Project menu. When you click New Project... entry in menu, this
    will be open in a new window.
    """

    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.returnValue = {"name": "NewFile", "baseFolder": ""}

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        HBoxFolder = QtWidgets.QHBoxLayout()
        self.LineEditFolder = QtWidgets.QLineEdit()
        self.LineEditFolder.setReadOnly(True)
        self.LineEditFolder.setText(str(self.returnValue["baseFolder"]))
        self.buttonFolder = QtWidgets.QPushButton("Browse")
        self.buttonFolder.clicked.connect(self.selectGameFolder)
        HBoxFolder.addWidget(self.LineEditFolder)
        HBoxFolder.addWidget(self.buttonFolder)

        HBoxName = QtWidgets.QHBoxLayout()
        self.LineEditName = QtWidgets.QLineEdit()
        self.LineEditName.setText(str(self.returnValue["name"]))
        self.LineEditName.editingFinished.connect(self.validateLineEditName)
        HBoxName.addWidget(QtWidgets.QLabel("Name:"))
        HBoxName.addWidget(self.LineEditName)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        #self.VBox.addWidget(QtWidgets.QLabel("THIS FUNCTION IS NOT COMPLETE YET"))
        self.VBox.addWidget(QtWidgets.QLabel("Select folder to create game:"))
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(QtWidgets.QLabel("Set game name:"))
        self.VBox.addLayout(HBoxName)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('New game current_project...')

    def validateLineEditName(self):
        tempStr = str(self.LineEditName.text())
        tempStr = tempStr.title()
        tempStr = tempStr.replace(" ", "")
        self.LineEditName.setText(tempStr)
        self.returnValue["name"] = self.LineEditName.text()
        self.validateIsOk()

    def selectGameFolder(self):
        self.LineEditFolder.setText(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.returnValue["baseFolder"] = self.LineEditFolder.text()
        self.validateIsOk()

    def validateIsOk(self):
        if self.returnValue["name"] != "" and self.returnValue["baseFolder"] != "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def getValue(self):
        return self.returnValue


class newFile(QtWidgets.QDialog):
    """
    The New File menu. When you click New File... entry in menu, this
    will be open in a new window.
    """
    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        gamefolder = ""
        if "gamefolder" in current_project.settings:
            gamefolder = os.path.join(current_project.settings["gamefolder"])
            if not os.path.isdir(gamefolder):
                gamefolder = ""

        palette = None
        if os.path.isfile(os.path.join(gamefolder,fifl.LEVELS,'default.pal.json')):
            palette = os.path.join(gamefolder,fifl.LEVELS,'default.pal.json')

        self.returnValue = {"name": "NewFile",
                            "width": 15, "height": 15,
                            "gameFolder": gamefolder,
                            'palette':palette }

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.OutCheckbox = QtWidgets.QCheckBox("Map for other game project")
        self.OutCheckbox.stateChanged.connect(self.otherFolder)

        self.LabelFolder = QtWidgets.QLabel("Select game Project folder:")
        HBoxFolder = QtWidgets.QHBoxLayout()
        self.LineEditFolder = QtWidgets.QLineEdit()
        self.LineEditFolder.setReadOnly(True)
        self.LineEditFolder.setText(str(self.returnValue["gameFolder"]))
        self.buttonFolder = QtWidgets.QPushButton("Browse")
        self.buttonFolder.clicked.connect(self.selectGameFolder)
        HBoxFolder.addWidget(self.LineEditFolder)
        HBoxFolder.addWidget(self.buttonFolder)

        self.ComboSizes = [15,20,25,30,40,50,80,100]
        HBoxSize = QtWidgets.QHBoxLayout()
        self.ComboBoxWidth = QtWidgets.QComboBox()
        self.ComboBoxHeight = QtWidgets.QComboBox()

        for i in range(len(self.ComboSizes)):
            item = str(self.ComboSizes[i])
            self.ComboBoxWidth.insertItem(i,item)
            self.ComboBoxHeight.insertItem(i,item)

        self.ComboBoxWidth.currentIndexChanged.connect(self.HWChanged)
        self.ComboBoxHeight.currentIndexChanged.connect(self.HWChanged)

        HBoxSize.addWidget(QtWidgets.QLabel("Width:"))
        HBoxSize.addWidget(self.ComboBoxWidth)
        HBoxSize.addWidget(QtWidgets.QLabel("Height:"))
        HBoxSize.addWidget(self.ComboBoxHeight)

        HBoxName = QtWidgets.QHBoxLayout()
        self.LineEditName = QtWidgets.QLineEdit()
        self.LineEditName.setText(str(self.returnValue["name"]))
        self.LineEditName.editingFinished.connect(self.validateLineEditName)
        self.LineEditName.textEdited.connect(self.validateLineEditName)
        HBoxName.addWidget(QtWidgets.QLabel("Name:"))
        HBoxName.addWidget(self.LineEditName)

        LabelPalette = QtWidgets.QLabel("Select palette for map:")
        HBoxPalette = QtWidgets.QHBoxLayout()
        self.ComboBoxPalette = QtWidgets.QComboBox()
        self.ComboBoxPalette.currentIndexChanged.connect(self.updatePalPreview)
        self.palettePreview = miniWdgt.tinyPreviewPalWidget()
        HBoxPalette.addWidget(LabelPalette)
        HBoxPalette.addWidget(self.ComboBoxPalette)

        self.VBox.addWidget(QtWidgets.QLabel("Set map properties:"))
        self.VBox.addLayout(HBoxSize)
        self.VBox.addLayout(HBoxName)
        self.VBox.addLayout(HBoxPalette)
        self.VBox.addWidget(self.palettePreview)

        self.VBox.addWidget(self.OutCheckbox)
        self.VBox.addWidget(self.LabelFolder)
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 400)
        self.setWindowTitle('New map...')

        self.otherFolder(False)
        self.findMapPalettes()
        self.updatePalPreview()

    def updatePalPreview(self, index=0):
        #updates the palette preview widget based on the combobox palette
        gamefolder = self.returnValue["gameFolder"]
        if self.ComboBoxPalette.count() >0:
            pi = self.ComboBoxPalette.currentIndex()
            p = os.path.join(gamefolder, fifl.LEVELS, self.palettes[pi] + '.pal.json')
            self.returnValue["palette"] = p
            self.palettePreview.updatePal(p,gamefolder)
        else:
            self.palettePreview.clear()

    def otherFolder(self, state):
        if(state):
            self.LabelFolder.show()
            self.LineEditFolder.show()
            self.buttonFolder.show()
            self.returnValue["gameFolder"] = ''
            self.findMapPalettes()
        else:
            gamefolder = ""
            if "gamefolder" in current_project.settings:
                gamefolder = os.path.join(current_project.settings["gamefolder"])
                if not os.path.isdir(gamefolder):
                    gamefolder = ""
            self.LineEditFolder.setText(gamefolder)
            self.returnValue["gameFolder"] = gamefolder
            self.LabelFolder.hide()
            self.LineEditFolder.hide()
            self.buttonFolder.hide()
            try:
                self.findMapPalettes()
            except FileNotFoundError:
                self.palettePreview.clear()
                self.palettes = []
                self.ComboBoxPalette.clear()
                self.ComboBoxPalette.setEnabled(False)
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def validateLineEditName(self):
        tempStr = str(self.LineEditName.text())
        tempStr = tempStr.title()
        tempStr = tempStr.replace(" ", "")
        self.LineEditName.setText(tempStr)
        self.returnValue["name"] = self.LineEditName.text()
        self.validateIsOk()

    def findMapPalettes(self):
        gamefolder = self.returnValue["gameFolder"]
        if(gamefolder!=''):
            self.ComboBoxPalette.clear()
            levels = os.path.join(gamefolder, fifl.LEVELS)
            filelist = [f for f in listdir(levels) if os.path.isfile(os.path.join(levels, f)) and f.endswith(".pal.json")]
            self.palettes = [f[:-9] for f in filelist]
            for i in range(len(self.palettes)):
                item = str(self.palettes[i])
                self.ComboBoxPalette.insertItem(i,item)

            self.returnValue["palette"] = os.path.join(gamefolder, fifl.LEVELS, self.palettes[0] + '.pal.json')
            self.ComboBoxPalette.setEnabled(True)
        else:
            self.palettes = []
            self.ComboBoxPalette.clear()
            self.ComboBoxPalette.setEnabled(False)
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def HWChanged(self, index):
        # Whenever a combobox is changed, we update the value to return
        # These combobox are relative to Height, Width
        wi = self.ComboBoxWidth.currentIndex()
        hi = self.ComboBoxHeight.currentIndex()
        w = self.ComboSizes[wi]
        h = self.ComboSizes[hi]
        self.returnValue['width'] = w
        self.returnValue['height'] = h

    def selectGameFolder(self):
        self.LineEditFolder.setText(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Project Directory")))
        self.returnValue["gameFolder"] = self.LineEditFolder.text()
        self.findMapPalettes()
        self.validateIsOk()

    def validateIsOk(self):
        if self.returnValue["name"] != "" and self.returnValue["gameFolder"] != "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def getValue(self):
        return self.returnValue
