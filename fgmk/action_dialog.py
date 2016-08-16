# -*- coding: utf-8 -*-
import os.path
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import tMat, game_init, current_project, mapfile, tile_set, miniWdgt
from fgmk.layer_wdgt import COLISIONLAYER as COLISIONLAYER
from fgmk.layer_wdgt import EVENTSLAYER as EVENTSLAYER


class changeTile(QtWidgets.QDialog):

    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.gamefolder = gamefolder
        self.edit = edit
        self.parent = parent

        self.initFile = game_init.openInitFile(gamefolder)

        self.useCurrentPlace = "current"

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText1 = QtWidgets.QLabel("Select where is the tile to change:")
        self.LabelText2 = QtWidgets.QLabel("Select to what type change:")
        self.LabelText3 = QtWidgets.QLabel("Change to modify colision layer:")
        self.LabelText4 = QtWidgets.QLabel("Select if event should also change:")

        self.comboBox = QtWidgets.QComboBox()

        self.colisionList = ["keep", "noColision", "collidable"]

        if(self.nothis is False):
            self.levelsList = ["this"]
        else:
            self.levelsList = []

        for level in self.initFile['LevelsList']:
            self.levelsList.append(level)

        for level in self.levelsList:
            self.comboBox.addItem(str(level))

        self.scrollArea = QtWidgets.QScrollArea()

        if(self.nothis is False):
            if(self.edit == None):
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.parent.myMap
                self.currentTileSet = self.parent.parent.myTileSet
        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.comboBox.itemText(0)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)

        self.myMiniMapWidget = miniWdgt.MiniMapWidget(
            self.currentLevel, self.currentTileSet, self)

        self.eventList = self.currentLevel.getTileListFromLayer(EVENTSLAYER)[:]
        self.eventList.insert(0, "remove")
        self.eventList.insert(0, "keep")
        self.eventList = [str(x) for x in self.eventList]

        self.checkbox = QtWidgets.QCheckBox("instead use event location", self)

        self.scrollArea.setWidget(self.myMiniMapWidget)

        self.myMiniMapWidget.selectedTile.connect(self.setTeleportPlace)
        self.LineTextPlace = QtWidgets.QLineEdit()

        self.myMiniPaletteWidget = miniWdgt.MiniPaletteWidget(
            self.currentTileSet, self)
        self.myMiniPaletteWidget.selectedTilePalette.connect(self.setTileToChange)
        self.LineTextTile = QtWidgets.QLineEdit()

        self.comboBoxLayers = QtWidgets.QComboBox()

        for layer in mapfile.LayersNameViewable:
            self.comboBoxLayers.addItem(str(layer))

        self.comboBoxColision = QtWidgets.QComboBox()

        for item in self.colisionList:
            self.comboBoxColision.addItem(str(item))

        self.comboBoxEvent = QtWidgets.QComboBox()

        for item in self.eventList:
            self.comboBoxEvent.addItem(str(item))

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.comboBox.currentIndexChanged.connect(self.updateMap)
        self.checkbox.stateChanged.connect(self.checkboxChanged)

        self.checkbox.setCheckState(QtCore.Qt.Checked)

        self.LineTextPlace.setReadOnly(True)
        self.LineTextTile.setReadOnly(True)

        if(edit != None):

            self.myMiniPaletteWidget.setImageCurrent(int(edit[0]))

            for idx, val in enumerate(mapfile.LayersNameViewable):
                if(val == edit[1]):
                    self.comboBoxLayers.setCurrentIndex(idx)

            for idx, val in enumerate(self.colisionList):
                if(val == edit[2]):
                    self.comboBoxColision.setCurrentIndex(idx)

            for idx, val in enumerate(self.eventList):
                if(val == edit[3]):
                    self.comboBoxEvent.setCurrentIndex(idx)

            if(edit[4] != self.useCurrentPlace):
                self.checkbox.setCheckState(QtCore.Qt.Unchecked)
                self.LineTextPlace.setText(
                    "{0};{1};{2}".format(edit[4], edit[5], edit[6]))

                for idx, val in enumerate(self.levelsList):
                    if(val == edit[6]):
                        self.comboBox.setCurrentIndex(idx)

                self.myMiniMapWidget.changeSelectXY(int(edit[4]), int(edit[5]))

            else:
                self.checkbox.setCheckState(QtCore.Qt.Checked)

        self.VBox.addWidget(self.LabelText1)
        self.VBox.addWidget(self.comboBox)
        self.VBox.addWidget(self.scrollArea)
        self.VBox.addWidget(self.LineTextPlace)
        self.VBox.addWidget(self.checkbox)
        self.VBox.addWidget(self.LabelText2)
        self.VBox.addWidget(self.myMiniPaletteWidget)
        self.VBox.addWidget(self.LineTextTile)
        self.VBox.addWidget(self.comboBoxLayers)

        self.VBox.addWidget(self.LabelText3)
        self.VBox.addWidget(self.comboBoxColision)
        self.VBox.addWidget(self.LabelText4)
        self.VBox.addWidget(self.comboBoxEvent)

        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 200, 350, 650)
        self.setWindowTitle('Select what tile and where to change to...')

        self.setTileToChange()

    def checkboxChanged(self, newState):
        if(newState == 2):
            self.LineTextPlace.setText(self.useCurrentPlace)

    def setTeleportPlace(self):
        position = self.myMiniMapWidget.getValue()
        textToReturn = "{0};{1};{2}".format(
            position[0], position[1], str(self.comboBox.currentText()))
        self.LineTextPlace.setText(textToReturn)
        self.checkbox.setCheckState(QtCore.Qt.Unchecked)

    def setTileToChange(self):
        tile = self.myMiniPaletteWidget.getValue()
        textToReturn = "{0}".format(tile)
        self.LineTextTile.setText(textToReturn)

    def updateMap(self, levelIndex):

        if (str(self.comboBox.itemText(levelIndex)) != "this"):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.comboBox.itemText(levelIndex)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            if(self.edit == None):
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.parent.myMap
                self.currentTileSet = self.parent.parent.myTileSet

        self.myMiniMapWidget.DrawMap(
            self, self.currentLevel, self.currentTileSet)
        self.myMiniPaletteWidget.drawPalette(self.currentTileSet)

    def getValue(self):
        text = str(self.LineTextTile.text()) + ";" + str(self.comboBoxLayers.currentText()) + ";" + str(
            self.comboBoxColision.currentText()) + ";" + str(self.comboBoxEvent.currentText()) + ";" + str(self.LineTextPlace.text())
        return text


class teleport(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, selectStartPosition=None,  **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.selectStartPosition = selectStartPosition
        self.gamefolder = gamefolder
        self.edit = edit
        self.parent = parent

        self.initFile = game_init.openInitFile(gamefolder)

        if(selectStartPosition == None):
            self.setWindowTitle('Select where to teleport...')
            indicative = 1
        else:
            self.setWindowTitle(selectStartPosition)
            indicative = 2

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText = QtWidgets.QLabel('Select where to teleport:')

        self.comboBox = QtWidgets.QComboBox()

        if(self.nothis is False):
            self.levelsList = ["this"]
        else:
            self.levelsList = []

        for level in self.initFile['LevelsList']:
            self.levelsList.append(level)

        for level in self.levelsList:
            self.comboBox.addItem(str(level))

        self.scrollArea = QtWidgets.QScrollArea()

        if(self.nothis is False):
            if(self.selectStartPosition == None):
                if(self.edit == None):
                    self.currentLevel = self.parent.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.parent.myTileSet
                else:
                    self.currentLevel = self.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.myMap
                self.currentTileSet = self.parent.myTileSet
        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.comboBox.itemText(0)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)

        self.myMiniMapWidget = miniWdgt.MiniMapWidget(
            self.currentLevel, self.currentTileSet, None, indicative)

        self.scrollArea.setWidget(self.myMiniMapWidget)

        self.myMiniMapWidget.selectedTile.connect(self.setTeleportPlace)

        self.LineText = QtWidgets.QLineEdit()
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.comboBox.currentIndexChanged.connect(self.updateMap)

        self.LineText.setReadOnly(True)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.comboBox)
        self.VBox.addWidget(self.scrollArea)
        self.VBox.addWidget(self.LineText)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 200, 350, 650)



        if(edit != None):
            self.LineText.setText("{0};{1}".format(edit[0], edit[1]))

            for idx, val in enumerate(self.levelsList):
                if(val == edit[2]):
                    self.comboBox.setCurrentIndex(idx)
                    break

            self.updateMap(idx)
            self.myMiniMapWidget.changeSelectXY(int(edit[0]), int(edit[1]))

    def setTeleportPlace(self):
        position = self.myMiniMapWidget.getValue()
        textToReturn = "{0};{1}".format(position[0], position[1])
        self.LineText.setText(textToReturn)

    def updateMap(self, levelIndex):
        if (str(self.comboBox.itemText(levelIndex)) != "this"):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.comboBox.itemText(levelIndex)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            if(self.selectStartPosition == None):
                if(self.edit == None):
                    self.currentLevel = self.parent.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.parent.myTileSet
                else:
                    self.currentLevel = self.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.myMap
                self.currentTileSet = self.parent.myTileSet

        self.myMiniMapWidget.DrawMap(
            self.currentLevel, self.currentTileSet)

    def getValue(self):
        text = str(self.LineText.text()) + ";" + \
            str(self.comboBox.currentText())
        return text


class teleportInPlace(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False,  **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.gamefolder = gamefolder
        self.edit = edit
        self.parent = parent

        self.initFile = game_init.openInitFile(gamefolder)

        self.setWindowTitle('Select map to teleport...')
        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText = QtWidgets.QLabel('Select where to teleport:')

        self.comboBox = QtWidgets.QComboBox()

        if(self.nothis is False):
            self.levelsList = ["this"]
        else:
            self.levelsList = []

        for level in self.initFile['LevelsList']:
            self.levelsList.append(level)

        for level in self.levelsList:
            self.comboBox.addItem(str(level))

        self.scrollArea = QtWidgets.QScrollArea()

        if(self.nothis is False):
            if(self.edit == None):
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.parent.myMap
                self.currentTileSet = self.parent.parent.myTileSet

        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.comboBox.itemText(0)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)

        self.myMiniMapWidget = miniWdgt.MiniMapWidget(
            self.currentLevel, self.currentTileSet, None, 0)

        self.scrollArea.setWidget(self.myMiniMapWidget)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.comboBox.currentIndexChanged.connect(self.updateMap)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.comboBox)
        self.VBox.addWidget(self.scrollArea)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 200, 350, 650)

        if(edit != None):
            for idx, val in enumerate(self.levelsList):
                if(val == edit[0]):
                    self.comboBox.setCurrentIndex(idx)
                    break

            self.updateMap(idx)

    def updateMap(self, levelIndex):
        if (str(self.comboBox.itemText(levelIndex)) != "this"):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.comboBox.itemText(levelIndex)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            if(self.edit == None):
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.parent.myMap
                self.currentTileSet = self.parent.parent.myTileSet


        self.myMiniMapWidget.DrawMap(
            self.currentLevel, self.currentTileSet)

    def getValue(self):
        text = str(self.comboBox.currentText())
        return text


class END(QtWidgets.QDialog):

    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.buttonBox)

    def getValue(self):
        return ""


class ELSE(QtWidgets.QDialog):

    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.buttonBox)

    def getValue(self):
        return ""


class IF(QtWidgets.QDialog):

    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        notefont = QtGui.QFont()
        notefont.setItalic(True)
        note = QtWidgets.QLabel("Use var:varname when referencing variables")
        note.setFont(notefont)

        self.var1LabelText = QtWidgets.QLabel("Write var or value:")
        self.operLabelText = QtWidgets.QLabel("Operation:")
        self.var2LabelText = QtWidgets.QLabel("Write var or value:")

        self.var1LineEdit = QtWidgets.QLineEdit()
        self.operLineEdit = QtWidgets.QLineEdit()
        self.var2LineEdit = QtWidgets.QLineEdit()

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.var1LabelText)
        self.VBox.addWidget(note)
        self.VBox.addWidget(self.var1LineEdit)
        self.VBox.addWidget(self.operLabelText)
        self.VBox.addWidget(self.operLineEdit)
        self.VBox.addWidget(self.var2LabelText)
        self.VBox.addWidget(self.var2LineEdit)
        self.VBox.addWidget(self.buttonBox)

        if(edit != None):
            self.var1LineEdit.setText(edit[0])
            self.operLineEdit.setText(edit[1])
            self.var2LineEdit.setText(edit[2])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('IF conditional...')

    def getValue(self):
        text = str(self.var1LineEdit.text()) + ";" + \
            str(self.operLineEdit.text()) + ";" + str(self.var2LineEdit.text())
        return text


class setVar(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.varLabelText = QtWidgets.QLabel("Write var name:")
        self.valLabelText = QtWidgets.QLabel("Write value:")

        self.varNameLineEdit = QtWidgets.QLineEdit()
        self.valueLineEdit = QtWidgets.QLineEdit()

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.varLabelText)
        self.VBox.addWidget(self.varNameLineEdit)
        self.VBox.addWidget(self.valLabelText)
        self.VBox.addWidget(self.valueLineEdit)
        self.VBox.addWidget(self.buttonBox)

        if(edit != None):
            self.varNameLineEdit.setText(edit[0])
            self.valueLineEdit.setText(edit[1])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Change var to value')

    def getValue(self):
        text = str(self.varNameLineEdit.text()) + \
            ";" + str(self.valueLineEdit.text())
        return text


class varPlusOne(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.varLabelText = QtWidgets.QLabel("Write var name")

        self.varNameLineEdit = QtWidgets.QLineEdit()

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.varLabelText)
        self.VBox.addWidget(self.varNameLineEdit)
        self.VBox.addWidget(self.buttonBox)

        if(edit != None):
            self.varNameLineEdit.setText(edit[0])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('You can add 1 to a var.')

    def getValue(self):
        text = str(self.varNameLineEdit.text())
        return text


class alert(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText = QtWidgets.QLabel("Write the text in the box below:")
        self.downLabelText = QtWidgets.QLabel(
            "tip: you can type var:varname to get the content of that variable.")

        self.LineEdit = QtWidgets.QLineEdit()

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.LineEdit)
        self.VBox.addWidget(self.downLabelText)
        self.VBox.addWidget(self.buttonBox)

        if(edit != None):
            self.LineEdit.setText(edit[0])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Write text to show in text box...')

    def getValue(self):
        text = str(self.LineEdit.text())
        textListLf = text.split("\n")
        textToReturn = textListLf[0]
        for line in textListLf[1:]:
            textToReturn += '\\n' + line
        return textToReturn

class showText(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText = QtWidgets.QLabel("Write the text in the box below:")
        self.downLabelText = QtWidgets.QLabel(
            "tip: you can type var:varname to get the content of that variable.")

        self.LineText = QtWidgets.QPlainTextEdit()

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.LineText)
        self.VBox.addWidget(self.downLabelText)
        self.VBox.addWidget(self.buttonBox)

        if(edit != None):
            self.LineText.setPlainText(edit[0])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Write text to show in text box...')

    def getValue(self):
        text = str(self.LineText.toPlainText())
        textListLf = text.split("\n")
        textToReturn = textListLf[0]
        for line in textListLf[1:]:
            textToReturn += '\\n' + line
        return textToReturn


class fadeIn(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.LabelText = QtWidgets.QLabel("Select the effect to use:")
        self.ListEffect = QtWidgets.QListWidget()

        effects = [["pixelize", "pixelizeFadeIn"], [
            "black", "blackFadeIn"], ["white", "whiteFadeIn"]]

        for effect in effects:
            item = QtWidgets.QListWidgetItem(effect[0])
            item.setWhatsThis(effect[1])
            self.ListEffect.addItem(item)

        self.checkbox = QtWidgets.QCheckBox("keep effect after")
        self.checkbox.setCheckState(QtCore.Qt.Unchecked)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListEffect)
        self.VBox.addWidget(self.checkbox)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 350)
        self.setWindowTitle('fadeIn: select the effect to apply')

        if(edit != None):
            for idx, val in enumerate(effects):
                if(val[1] == edit[0]):
                    self.ListEffect.setCurrentRow(idx)

            if(edit[1] == 'keepEffect'):
                self.checkbox.setCheckState(QtCore.Qt.Checked)

    def getValue(self):
        effecToReturn = str(self.ListEffect.selectedItems()[0].whatsThis())
        keepEffect = 'doNotKeep'
        if self.checkbox.isChecked():
            keepEffect = 'keepEffect'
        return effecToReturn + ';' + keepEffect


class fadeOut(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.LabelText = QtWidgets.QLabel("Select the effect to use:")
        self.ListEffect = QtWidgets.QListWidget()

        effects = [["pixelize", "pixelizeFadeOut"], [
            "black", "blackFadeOut"], ["white", "whiteFadeOut"]]

        for effect in effects:
            item = QtWidgets.QListWidgetItem(effect[0])
            item.setWhatsThis(effect[1])
            self.ListEffect.addItem(item)

        self.checkbox = QtWidgets.QCheckBox("keep effect after")
        self.checkbox.setCheckState(QtCore.Qt.Unchecked)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListEffect)
        self.VBox.addWidget(self.checkbox)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 350)
        self.setWindowTitle('fadeOut: select the effect to apply')

        if(edit != None):
            for idx, val in enumerate(effects):
                if(val[1] == edit[0]):
                    self.ListEffect.setCurrentRow(idx)

            if(edit[1] == 'keepEffect'):
                self.checkbox.setCheckState(QtCore.Qt.Checked)

    def getValue(self):
        effecToReturn = str(self.ListEffect.selectedItems()[0].whatsThis())
        keepEffect = 'doNotKeep'
        if self.checkbox.isChecked():
            keepEffect = 'keepEffect'
        return effecToReturn + ';' + keepEffect

class rain(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.LabelText = QtWidgets.QLabel("Select either start or stop:")
        self.ListEffect = QtWidgets.QListWidget()

        self.radiostart = QtWidgets.QRadioButton("start", self)
        self.radiostop = QtWidgets.QRadioButton("stop", self)

        self.radiostart.setChecked(True)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.radiostart)
        self.VBox.addWidget(self.radiostop)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 350)
        self.setWindowTitle('rain: choose if starts raining')

        if(edit != None):
            if(edit[0] == 'stop'):
                self.radiostop.setChecked(True)

    def getValue(self):
        rain_state='start'
        if self.radiostop.isChecked():
            rain_state = 'stop'
        return rain_state


class noEffect(QtWidgets.QDialog):

    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.accept

    def getValue(self):
        return ""
