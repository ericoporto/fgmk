# -*- coding: utf-8 -*-
import os.path
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import tMat, game_init, current_project, tile_set, miniWdgt
from fgmk.ff import mapfile, charaset_format, charas_format
from fgmk.util.layer_logic import COLISIONLAYER as COLISIONLAYER
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER

"""
This module has a class for every possible action. The file actionsList.json
lists all actions and their parameters.
Each class is a QDialog that will be presented when adding an action or editing
it. They all must implement a getValue function that will return the parameters
as a string, with each parameter separated by a ; in the string.
"""

class actionDialog(QtWidgets.QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, myMap=None, myTileSet=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.gamefolder = gamefolder
        self.edit = edit
        self.parent = parent
        self.myMap = myMap
        self.myTileSet = myTileSet

class changeTile(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.initFile = game_init.openInitFile(self.gamefolder)

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
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
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

        if(self.edit != None):

            self.myMiniPaletteWidget.setImageCurrent(int(self.edit[0]))

            for idx, val in enumerate(mapfile.LayersNameViewable):
                if(val == self.edit[1]):
                    self.comboBoxLayers.setCurrentIndex(idx)

            for idx, val in enumerate(self.colisionList):
                if(val == self.edit[2]):
                    self.comboBoxColision.setCurrentIndex(idx)

            for idx, val in enumerate(self.eventList):
                if(val == self.edit[3]):
                    self.comboBoxEvent.setCurrentIndex(idx)

            if(self.edit[4] != self.useCurrentPlace):
                self.checkbox.setCheckState(QtCore.Qt.Unchecked)
                self.LineTextPlace.setText(
                    "{0};{1};{2}".format(self.edit[4], self.edit[5], self.edit[6]))

                for idx, val in enumerate(self.levelsList):
                    if(val == self.edit[6]):
                        self.comboBox.setCurrentIndex(idx)

                self.myMiniMapWidget.changeSelectXY(int(self.edit[4]), int(self.edit[5]))

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
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.parent.myTileSet
            else:
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)
        self.myMiniPaletteWidget.drawPalette(self.currentTileSet)

    def getValue(self):
        text = str(self.LineTextTile.text()) + ";" + str(self.comboBoxLayers.currentText()) + ";" + str(
            self.comboBoxColision.currentText()) + ";" + str(self.comboBoxEvent.currentText()) + ";" + str(self.LineTextPlace.text())
        return text


class changeAllTiles(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.initFile = game_init.openInitFile(self.gamefolder)

        self.useCurrentPlace = "current"

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText1 = QtWidgets.QLabel("Select the map for tile change:")
        self.LabelText2 = QtWidgets.QLabel("What type to change from?")
        self.LabelText3 = QtWidgets.QLabel("To what type change to?")
        self.LabelText4 = QtWidgets.QLabel("Change to modify colision layer:")
        self.LabelText5 = QtWidgets.QLabel("Select if event should also change:")

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
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.parent.myTileSet
            else:
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.comboBox.itemText(0)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)

        self.myMiniMapWidget = miniWdgt.MiniMapWidget(
            self.currentLevel, self.currentTileSet, self, indicativeToUse=0)

        self.eventList = self.currentLevel.getTileListFromLayer(EVENTSLAYER)[:]
        self.eventList.insert(0, "remove")
        self.eventList.insert(0, "keep")
        self.eventList = [str(x) for x in self.eventList]

        self.scrollArea.setWidget(self.myMiniMapWidget)

        self.oriMPWidget = miniWdgt.MiniPaletteWidget(self.currentTileSet, self)
        self.newMPWidget = miniWdgt.MiniPaletteWidget(self.currentTileSet, self)

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

        if(self.edit != None):
            self.oriMPWidget.setImageCurrent(int(self.edit[0]))
            self.newMPWidget.setImageCurrent(int(self.edit[1]))
            for idx, val in enumerate(mapfile.LayersNameViewable):
                if(val == self.edit[2]):
                    self.comboBoxLayers.setCurrentIndex(idx)

            for idx, val in enumerate(self.colisionList):
                if(val == self.edit[3]):
                    self.comboBoxColision.setCurrentIndex(idx)

            for idx, val in enumerate(self.eventList):
                if(val == self.edit[4]):
                    self.comboBoxEvent.setCurrentIndex(idx)

            for idx, val in enumerate(self.levelsList):
                if(val == self.edit[5]):
                    self.comboBox.setCurrentIndex(idx)

        self.VBox.addWidget(self.LabelText1)
        self.VBox.addWidget(self.comboBox)
        self.VBox.addWidget(self.scrollArea)
        self.VBox.addWidget(self.LabelText2)
        self.VBox.addWidget(self.oriMPWidget)
        self.VBox.addWidget(self.LabelText3)
        self.VBox.addWidget(self.newMPWidget)
        self.VBox.addWidget(self.comboBoxLayers)

        self.VBox.addWidget(self.LabelText4)
        self.VBox.addWidget(self.comboBoxColision)
        self.VBox.addWidget(self.LabelText5)
        self.VBox.addWidget(self.comboBoxEvent)

        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 200, 350, 650)
        self.setWindowTitle('Select what tile and where to change to...')

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
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.parent.myTileSet
            else:
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)
        self.oriMPWidget.drawPalette(self.currentTileSet)
        self.newMPWidget.drawPalette(self.currentTileSet)

    def getValue(self):
        oriTile = "{0}".format(self.oriMPWidget.getValue())
        newTile = "{0}".format(self.newMPWidget.getValue())
        text = str(oriTile) + ";" +str(newTile) + ";" + str(self.comboBoxLayers.currentText()) + ";" + str(
            self.comboBoxColision.currentText()) + ";" + str(self.comboBoxEvent.currentText()) + ";" + str(self.comboBox.currentText())
        return text


class teleport(actionDialog):
    def __init__(self, **kwargs):
        #if selectStartPosition is here, we should not pass it along
        self.selectStartPosition =  kwargs.pop('selectStartPosition',None)
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.initFile = game_init.openInitFile(self.gamefolder)

        if(self.selectStartPosition == None):
            self.setWindowTitle('Select where to teleport...')
            indicative = 1
        else:
            self.setWindowTitle(self.selectStartPosition)
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
                    #Journey to get the map
                    #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                    self.currentLevel = self.parent.parent.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.parent.parent.myTileSet
                else:
                    #Journey to get the map
                    #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                    self.currentLevel = self.parent.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.parent.myTileSet
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



        if(self.edit != None):
            self.LineText.setText("{0};{1}".format(self.edit[0], self.edit[1]))

            for idx, val in enumerate(self.levelsList):
                if(val == self.edit[2]):
                    self.comboBox.setCurrentIndex(idx)
                    break

            self.updateMap(idx)
            self.myMiniMapWidget.changeSelectXY(int(self.edit[0]), int(self.edit[1]))

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
                    #Journey to get the map
                    #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                    self.currentLevel = self.parent.parent.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.parent.parent.myTileSet
                else:
                    #Journey to get the map
                    #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                    self.currentLevel = self.parent.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.myMap
                self.currentTileSet = self.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)

    def getValue(self):
        text = str(self.LineText.text()) + ";" + \
            str(self.comboBox.currentText())
        return text


class teleportInPlace(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.initFile = game_init.openInitFile(self.gamefolder)

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
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.parent.myTileSet
            else:
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet

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

        if(self.edit != None):
            for idx, val in enumerate(self.levelsList):
                if(val == self.edit[0]):
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
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.parent.myTileSet
            else:
                #Journey to get the map
                #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet


        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)

    def getValue(self):
        text = str(self.comboBox.currentText())
        return text


class END(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.buttonBox)

    def getValue(self):
        return ""


class ELSE(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.buttonBox)

    def getValue(self):
        return ""


class IF(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

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

        if(self.edit != None):
            self.var1LineEdit.setText(self.edit[0])
            self.operLineEdit.setText(self.edit[1])
            self.var2LineEdit.setText(self.edit[2])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('IF conditional...')

    def getValue(self):
        text = str(self.var1LineEdit.text()) + ";" + \
            str(self.operLineEdit.text()) + ";" + str(self.var2LineEdit.text())
        return text


class setVar(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

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

        if(self.edit != None):
            self.varNameLineEdit.setText(self.edit[0])
            self.valueLineEdit.setText(self.edit[1])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Change var to value')

    def getValue(self):
        text = str(self.varNameLineEdit.text()) + \
            ";" + str(self.valueLineEdit.text())
        return text


class varPlusOne(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

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

        if(self.edit != None):
            self.varNameLineEdit.setText(self.edit[0])

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

class showText(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

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

        if(self.edit != None):
            self.LineText.setPlainText(self.edit[0])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Write text to show in text box...')

    def getValue(self):
        text = str(self.LineText.toPlainText())
        textListLf = text.split("\n")
        textToReturn = textListLf[0]
        for line in textListLf[1:]:
            textToReturn += '\\n' + line
        return textToReturn


class fadeIn(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

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

        if(self.edit != None):
            for idx, val in enumerate(effects):
                if(val[1] == self.edit[0]):
                    self.ListEffect.setCurrentRow(idx)

            if(self.edit[1] == 'keepEffect'):
                self.checkbox.setCheckState(QtCore.Qt.Checked)

    def getValue(self):
        effecToReturn = str(self.ListEffect.selectedItems()[0].whatsThis())
        keepEffect = 'doNotKeep'
        if self.checkbox.isChecked():
            keepEffect = 'keepEffect'
        return effecToReturn + ';' + keepEffect


class fadeOut(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

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

        if(self.edit != None):
            for idx, val in enumerate(effects):
                if(val[1] == self.edit[0]):
                    self.ListEffect.setCurrentRow(idx)

            if(self.edit[1] == 'keepEffect'):
                self.checkbox.setCheckState(QtCore.Qt.Checked)

    def getValue(self):
        effecToReturn = str(self.ListEffect.selectedItems()[0].whatsThis())
        keepEffect = 'doNotKeep'
        if self.checkbox.isChecked():
            keepEffect = 'keepEffect'
        return effecToReturn + ';' + keepEffect

class rain(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

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

        if(self.edit != None):
            if(self.edit[0] == 'stop'):
                self.radiostop.setChecked(True)

    def getValue(self):
        rain_state='start'
        if self.radiostop.isChecked():
            rain_state = 'stop'
        return rain_state

class changePlayerAnimation(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText = QtWidgets.QLabel("Select animation to change to")

        charasetname = game_init.playerInitCharaset()
        charaset = charaset_format.CharasetFormat()
        charaset.loadGameFolder(self.gamefolder)
        animation_dict_keys = charaset.getAnimations(charasetname)

        # get the list of animations,
        # sort to give a predictable order
        # and then insert the default attribute
        self.animationList = list(animation_dict_keys)
        self.animationList.sort()
        self.animationList.insert(0,'default')

        self.comboBoxAnim = QtWidgets.QComboBox()
        for item in self.animationList:
            self.comboBoxAnim.addItem(str(item))

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.comboBoxAnim)
        self.VBox.addWidget(self.buttonBox)

        if(self.edit != None):
            for idx, val in enumerate(self.animationList):
                if( str(val) == str(self.edit[0]) ):
                    self.comboBoxAnim.setCurrentIndex(idx)
                    break

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Change animation of player...')

    def getValue(self):
        text = str(self.comboBoxAnim.currentText())
        return text


class waitCycle(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelText = QtWidgets.QLabel("Select time to wait in cycles")

        self.waitList = [1,2,3,4,5,10,20,30,60]
        self.comboBoxWait = QtWidgets.QComboBox()

        for item in self.waitList:
            self.comboBoxWait.addItem(str(item))

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.comboBoxWait)
        self.VBox.addWidget(self.buttonBox)

        if(self.edit != None):
            for idx, val in enumerate(self.waitList):
                if(str(val) == str(self.edit[0])):
                    self.comboBoxWait.setCurrentIndex(idx)
                    break

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('Block wait for cycles...')

    def getValue(self):
        text = str(self.comboBoxWait.currentText())
        return text


class addItem(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.LabelText = QtWidgets.QLabel("Select item to add:")
        self.ListItem = miniWdgt.miniItemsList()

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListItem)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 350)
        self.setWindowTitle('addItem: select item to add')

        if(self.edit != None):
            self.ListItem.setItem(self.edit[0])

    def getValue(self):
        itemToReturn = str(self.ListItem.getItem())
        return itemToReturn

class dropItem(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.LabelText = QtWidgets.QLabel("Select item to drop:")
        self.ListItem = miniWdgt.miniItemsList()

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListItem)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 350)
        self.setWindowTitle('dropItem: select item to drop')

        if(self.edit != None):
            self.ListItem.setItem(self.edit[0])

    def getValue(self):
        itemToReturn = str(self.ListItem.getItem())
        return itemToReturn


class noEffect(actionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        actionDialog.__init__(self, **kwargs)

        self.accept

    def getValue(self):
        return ""
