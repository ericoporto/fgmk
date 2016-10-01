# -*- coding: utf-8 -*-
"""
.. module:: fgmk.action_dialog

This module has a class for every possible action. The file actionsList.json
lists all actions and their parameters.
Each class is a QDialog that will be presented when adding an action or editing
it. They all must implement a getValue function that will return the parameters
as a string, with each parameter separated by a ; in the string.
"""
import os.path
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import tMat, game_init, current_project, tile_set, miniWdgt
from fgmk.ff import mapfile, charaset_format, charas_format
from fgmk.util.layer_logic import COLISIONLAYER as COLISIONLAYER
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER

class ActionDialog(QtWidgets.QDialog):
    """ActionDialog is the base of every Actions menu

    Each action should extend from this class, and provide a getValue() method
    to return parameters as a string, separated by `;` - like `param1;param2` or
    just `param1`.


    """
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, myMap=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.gamefolder = gamefolder
        self.edit = edit
        self.parent = parent
        self.myMap = myMap

        MainVBox =  QtWidgets.QVBoxLayout(self)
        MainVBox.setAlignment(QtCore.Qt.AlignTop)
        self.VBox = QtWidgets.QVBoxLayout()
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        MainVBox.addLayout(self.VBox)
        MainVBox.addWidget(self.buttonBox)

class showText(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Write the text in the box below:")
        self.downLabelText = QtWidgets.QLabel(
            "tip: you can type var:varname to get the content of that variable.")

        self.LineText = QtWidgets.QPlainTextEdit()

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.LineText)
        self.VBox.addWidget(self.downLabelText)


        if(self.edit != None):
            self.LineText.setPlainText(self.edit[0])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('showText: Text box that waits player interaction...')

    def getValue(self):
        text = str(self.LineText.toPlainText())
        textListLf = text.split("\n")
        textToReturn = textListLf[0]
        for line in textListLf[1:]:
            textToReturn += '\\n' + line
        return textToReturn


class alert(ActionDialog):
    def __init__(self,  **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Write the text in the box below:")
        self.downLabelText = QtWidgets.QLabel(
            "tip: you can type var:varname to get the content of that variable.")

        self.LineEdit = QtWidgets.QLineEdit()

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.LineEdit)
        self.VBox.addWidget(self.downLabelText)


        if(self.edit != None):
            self.LineEdit.setText(self.edit[0])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('alert: Write text to show in text box...')

    def getValue(self):
        text = str(self.LineEdit.text())
        textListLf = text.split("\n")
        textToReturn = textListLf[0]
        for line in textListLf[1:]:
            textToReturn += '\\n' + line
        return textToReturn


class teleport(ActionDialog):
    def __init__(self, **kwargs):
        #if selectStartPosition is here, we should not pass it along
        self.selectStartPosition =  kwargs.pop('selectStartPosition',None)
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.initFile = game_init.openInitFile(self.gamefolder)

        if(self.selectStartPosition == None):
            self.setWindowTitle('teleport: Select where to teleport...')
            indicative = 1
        else:
            self.setWindowTitle(self.selectStartPosition)
            indicative = 2

        self.LabelText = QtWidgets.QLabel('Select where to teleport:')

        self.levelSelector = miniWdgt.levelSelector(nothis=self.nothis)

        self.scrollArea = QtWidgets.QScrollArea()

        if(self.nothis is False):
            if(self.selectStartPosition == None):
                self.currentLevel = self.myMap
                self.currentTileSet = self.myMap.parent.myTileSet
            else:
                self.currentLevel = self.parent.myMap
                self.currentTileSet = self.parent.myTileSet
        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.levelSelector.itemText(0)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)

        self.myMiniMapWidget = miniWdgt.MiniMapWidget(
            self.currentLevel, self.currentTileSet, None, indicative)

        self.scrollArea.setWidget(self.myMiniMapWidget)

        self.myMiniMapWidget.selectedTile.connect(self.setTeleportPlace)

        self.LineText = QtWidgets.QLineEdit()
        self.levelSelector.currentIndexChanged.connect(self.updateMap)

        self.LineText.setReadOnly(True)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.levelSelector)
        self.VBox.addWidget(self.scrollArea)
        self.VBox.addWidget(self.LineText)

        self.setGeometry(300, 200, 350, 650)

        if(self.edit != None):
            self.LineText.setText("{0};{1}".format(self.edit[0], self.edit[1]))
            self.levelSelector.edit(self.edit[2])
            self.myMiniMapWidget.changeSelectXY(int(self.edit[0]), int(self.edit[1]))

    def setTeleportPlace(self):
        position = self.myMiniMapWidget.getValue()
        textToReturn = "{0};{1}".format(position[0], position[1])
        self.LineText.setText(textToReturn)

    def updateMap(self, levelIndex):
        if (str(self.levelSelector.itemText(levelIndex)) != "this"):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.levelSelector.itemText(levelIndex)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            if(self.selectStartPosition == None):
                if(self.edit == None):
                    #Journey to get the map
                    #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                    self.currentLevel = self.myMap
                    self.currentTileSet = self.myMap.parent.myTileSet
                else:
                    #Journey to get the map
                    #ActionsWidget -> tinyActionsWdgt -> EventsWidget -> Editor
                    self.currentLevel = self.myMap
                    self.currentTileSet = self.myMap.parent.myTileSet
            else:
                self.currentLevel = self.parent.myMap
                self.currentTileSet = self.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)

    def getValue(self):
        text = str(self.LineText.text()) + ";" + \
            str(self.levelSelector.currentText())
        return text


class teleportInPlace(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)
        self.initFile = game_init.openInitFile(self.gamefolder)
        self.setWindowTitle('teleportInPlace: Select map to teleport...')

        self.LabelText = QtWidgets.QLabel('Select where to teleport:')
        self.levelSelector = miniWdgt.levelSelector(nothis=self.nothis)

        self.myMiniMapViewer = miniWdgt.MiniMapViewer(
                                    mapAtStart=self.levelSelector.itemText(0),
                                    nothis=self.nothis,
                                    myMap=self.myMap,
                                    indicative=0)

        self.levelSelector.currentIndexChanged.connect(self.updateMap)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.levelSelector)
        self.VBox.addWidget(self.myMiniMapViewer)


        self.setGeometry(300, 200, 350, 650)

        if(self.edit != None):
            self.levelSelector.edit(self.edit[0])

    def updateMap(self, levelIndex):
        self.myMiniMapViewer.updateMap(self.levelSelector.itemText(levelIndex))

    def getValue(self):
        text = str(self.levelSelector.currentText())
        return text


class addItem(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Select item to add:")
        self.ListItem = miniWdgt.miniItemsList()

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListItem)


        self.setGeometry(300, 40, 350, 350)
        self.setWindowTitle('addItem: select item to add')

        if(self.edit != None):
            self.ListItem.setItem(self.edit[0])

    def getValue(self):
        itemToReturn = str(self.ListItem.getItem())
        return itemToReturn


class dropItem(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Select item to drop:")
        self.ListItem = miniWdgt.miniItemsList()

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListItem)


        self.setGeometry(300, 40, 350, 350)
        self.setWindowTitle('dropItem: select item to drop')

        if(self.edit != None):
            self.ListItem.setItem(self.edit[0])

    def getValue(self):
        itemToReturn = str(self.ListItem.getItem())
        return itemToReturn


class changeTile(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.initFile = game_init.openInitFile(self.gamefolder)

        self.useCurrentPlace = "current"

        self.LabelText1 = QtWidgets.QLabel("Select where is the tile to change:")
        self.LabelText2 = QtWidgets.QLabel("Select to what type change:")
        self.LabelText3 = QtWidgets.QLabel("Change to modify colision layer:")
        self.LabelText4 = QtWidgets.QLabel("Select if event should also change:")

        self.levelSelector = miniWdgt.levelSelector(nothis=self.nothis)

        self.colisionList = ["keep", "noColision", "collidable"]

        self.scrollArea = QtWidgets.QScrollArea()

        if(self.nothis is False):
            self.currentLevel = self.myMap
            self.currentTileSet = self.myMap.parent.myTileSet
        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.levelSelector.itemText(0)))
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

        self.levelSelector.currentIndexChanged.connect(self.updateMap)
        self.checkbox.stateChanged.connect(self.checkboxChanged)

        self.checkbox.setCheckState(QtCore.Qt.Checked)

        self.LineTextPlace.setReadOnly(True)
        self.LineTextTile.setReadOnly(True)

        if(self.edit != None):
            if(self.edit[4] != self.useCurrentPlace):
                self.checkbox.setCheckState(QtCore.Qt.Unchecked)
                self.LineTextPlace.setText(
                    "{0};{1};{2}".format(self.edit[4], self.edit[5], self.edit[6]))

                self.levelSelector.edit(self.edit[6])

                self.myMiniMapWidget.changeSelectXY(int(self.edit[4]), int(self.edit[5]))

            else:
                self.checkbox.setCheckState(QtCore.Qt.Checked)

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



        self.VBox.addWidget(self.LabelText1)
        self.VBox.addWidget(self.levelSelector)
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

        self.setGeometry(300, 200, 350, 650)
        self.setWindowTitle('changeTile: Select what tile and where to change to...')

        self.setTileToChange()

    def checkboxChanged(self, newState):
        if(newState == 2):
            self.LineTextPlace.setText(self.useCurrentPlace)

    def setTeleportPlace(self):
        position = self.myMiniMapWidget.getValue()
        textToReturn = "{0};{1};{2}".format(
            position[0], position[1], str(self.levelSelector.currentText()))
        self.LineTextPlace.setText(textToReturn)
        self.checkbox.setCheckState(QtCore.Qt.Unchecked)

    def setTileToChange(self):
        tile = self.myMiniPaletteWidget.getValue()
        textToReturn = "{0}".format(tile)
        self.LineTextTile.setText(textToReturn)

    def updateMap(self, levelIndex):

        if (str(self.levelSelector.itemText(levelIndex)) != "this"):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.levelSelector.itemText(levelIndex)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            self.currentLevel = self.myMap
            self.currentTileSet = self.myMap.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)
        self.myMiniPaletteWidget.drawPalette(self.currentTileSet)

    def getValue(self):
        text = str(self.LineTextTile.text()) + ";" + str(self.comboBoxLayers.currentText()) + ";" + str(
            self.comboBoxColision.currentText()) + ";" + str(self.comboBoxEvent.currentText()) + ";" + str(self.LineTextPlace.text())
        return text


class changeAllTiles(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.initFile = game_init.openInitFile(self.gamefolder)

        self.useCurrentPlace = "current"

        self.LabelText1 = QtWidgets.QLabel("Select the map for tile change:")
        self.LabelText2 = QtWidgets.QLabel("What type to change from?")
        self.LabelText3 = QtWidgets.QLabel("To what type change to?")
        self.LabelText4 = QtWidgets.QLabel("Change to modify colision layer:")
        self.LabelText5 = QtWidgets.QLabel("Select if event should also change:")

        self.levelSelector = miniWdgt.levelSelector(nothis=self.nothis)

        self.colisionList = ["keep", "noColision", "collidable"]

        self.scrollArea = QtWidgets.QScrollArea()

        if(self.nothis is False):
            self.currentLevel = self.myMap
            self.currentTileSet = self.myMap.parent.myTileSet
        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.levelSelector.itemText(0)))
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

        self.levelSelector.currentIndexChanged.connect(self.updateMap)

        if(self.edit != None):
            self.levelSelector.edit(self.edit[5])
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


        self.VBox.addWidget(self.LabelText1)
        self.VBox.addWidget(self.levelSelector)
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



        self.setGeometry(300, 200, 350, 650)
        self.setWindowTitle('changeAllTiles: Select what tile and where to change to...')

    def updateMap(self, levelIndex):

        if (str(self.levelSelector.itemText(levelIndex)) != "this"):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.levelSelector.itemText(levelIndex)))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            self.currentLevel = self.myMap
            self.currentTileSet = self.myMap.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)
        self.oriMPWidget.drawPalette(self.currentTileSet)
        self.newMPWidget.drawPalette(self.currentTileSet)

    def getValue(self):
        oriTile = "{0}".format(self.oriMPWidget.getValue())
        newTile = "{0}".format(self.newMPWidget.getValue())
        text = str(oriTile) + ";" +str(newTile) + ";" + str(self.comboBoxLayers.currentText()) + ";" + str(
            self.comboBoxColision.currentText()) + ";" + str(self.comboBoxEvent.currentText()) + ";" + str(self.levelSelector.currentText())
        return text


class END(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

    def getValue(self):
        return ""


class ELSE(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

    def getValue(self):
        return ""


class IF(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

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

        self.VBox.addWidget(self.var1LabelText)
        self.VBox.addWidget(note)
        self.VBox.addWidget(self.var1LineEdit)
        self.VBox.addWidget(self.operLabelText)
        self.VBox.addWidget(self.operLineEdit)
        self.VBox.addWidget(self.var2LabelText)
        self.VBox.addWidget(self.var2LineEdit)

        if(self.edit != None):
            self.var1LineEdit.setText(self.edit[0])
            self.operLineEdit.setText(self.edit[1])
            self.var2LineEdit.setText(self.edit[2])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('IF: conditional...')

    def getValue(self):
        text = str(self.var1LineEdit.text()) + ";" + \
            str(self.operLineEdit.text()) + ";" + str(self.var2LineEdit.text())
        return text


class setVar(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.varLabelText = QtWidgets.QLabel("Write var name:")
        self.valLabelText = QtWidgets.QLabel("Write value:")

        self.varNameLineEdit = QtWidgets.QLineEdit()
        self.valueLineEdit = QtWidgets.QLineEdit()

        self.VBox.addWidget(self.varLabelText)
        self.VBox.addWidget(self.varNameLineEdit)
        self.VBox.addWidget(self.valLabelText)
        self.VBox.addWidget(self.valueLineEdit)

        if(self.edit != None):
            self.varNameLineEdit.setText(self.edit[0])
            self.valueLineEdit.setText(self.edit[1])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('setVar: Change var to value')

    def getValue(self):
        text = str(self.varNameLineEdit.text()) + \
            ";" + str(self.valueLineEdit.text())
        return text


class varPlusOne(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.varLabelText = QtWidgets.QLabel("Write var name")

        self.varNameLineEdit = QtWidgets.QLineEdit()

        self.VBox.addWidget(self.varLabelText)
        self.VBox.addWidget(self.varNameLineEdit)

        if(self.edit != None):
            self.varNameLineEdit.setText(self.edit[0])

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('varPlusOne: You can add 1 to a var.')

    def getValue(self):
        text = str(self.varNameLineEdit.text())
        return text





class fadeIn(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Select the effect to use:")
        self.ListEffect = QtWidgets.QListWidget()

        effects = [["pixelize", "pixelizeFadeIn"], [
            "black", "blackFadeIn"], ["white", "whiteFadeIn"]]

        for effect in effects:
            item = QtWidgets.QListWidgetItem(effect[0])
            item.setWhatsThis(effect[1])
            self.ListEffect.addItem(item)

        self.ListEffect.setCurrentRow(0)

        self.checkbox = QtWidgets.QCheckBox("keep effect after")
        self.checkbox.setCheckState(QtCore.Qt.Unchecked)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListEffect)
        self.VBox.addWidget(self.checkbox)


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


class fadeOut(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Select the effect to use:")
        self.ListEffect = QtWidgets.QListWidget()

        effects = [["pixelize", "pixelizeFadeOut"], [
            "black", "blackFadeOut"], ["white", "whiteFadeOut"]]

        for effect in effects:
            item = QtWidgets.QListWidgetItem(effect[0])
            item.setWhatsThis(effect[1])
            self.ListEffect.addItem(item)

        self.ListEffect.setCurrentRow(0)

        self.checkbox = QtWidgets.QCheckBox("keep effect after")
        self.checkbox.setCheckState(QtCore.Qt.Unchecked)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.ListEffect)
        self.VBox.addWidget(self.checkbox)


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

class rain(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Select either start or stop:")
        self.ListEffect = QtWidgets.QListWidget()

        self.radiostart = QtWidgets.QRadioButton("start", self)
        self.radiostop = QtWidgets.QRadioButton("stop", self)

        self.radiostart.setChecked(True)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.radiostart)
        self.VBox.addWidget(self.radiostop)


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

class changePlayerAnimation(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

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

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.comboBoxAnim)


        if(self.edit != None):
            for idx, val in enumerate(self.animationList):
                if( str(val) == str(self.edit[0]) ):
                    self.comboBoxAnim.setCurrentIndex(idx)
                    break

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('changePlayerAnimation: Change animation of player...')

    def getValue(self):
        text = str(self.comboBoxAnim.currentText())
        return text


class waitCycle(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.LabelText = QtWidgets.QLabel("Select time to wait in cycles")

        self.waitList = [1,2,3,4,5,10,20,30,60]
        self.comboBoxWait = QtWidgets.QComboBox()

        for item in self.waitList:
            self.comboBoxWait.addItem(str(item))

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.comboBoxWait)


        if(self.edit != None):
            for idx, val in enumerate(self.waitList):
                if(str(val) == str(self.edit[0])):
                    self.comboBoxWait.setCurrentIndex(idx)
                    break

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('waitCycle: Block wait for cycles...')

    def getValue(self):
        text = str(self.comboBoxWait.currentText())
        return text


class noEffect(ActionDialog):
    def __init__(self, **kwargs):
        #super().__init__(parent, **kwargs)
        ActionDialog.__init__(self, **kwargs)

        self.accept

    def getValue(self):
        return ""
