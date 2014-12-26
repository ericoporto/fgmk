import sys
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import tMat
import TileXtra
import TXWdgt





COLISIONLAYER = 3
EVENTSLAYER = 4




class changeTile(QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
    	QDialog.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.gamefolder = gamefolder
        self.edit = edit
        self.parent = parent

        self.initFile = TXWdgt.openInitFile(gamefolder)

        self.useCurrentPlace = "current"

    	self.VBox = QVBoxLayout(self)
    	self.VBox.setAlignment(Qt.AlignTop)

    	self.LabelText1 = QLabel("Select where is the tile to change:")
    	self.LabelText2 = QLabel("Select to what type change:")
    	self.LabelText3 = QLabel("Change to modify colision layer:")
    	self.LabelText4 = QLabel("Select if event should also change:")

        self.comboBox = QComboBox()

        self.colisionList = [ "keep","noColision","collidable"]

        if(self.nothis is False):
            self.levelsList = ["this"]
        else:
            self.levelsList = []

        for level in self.initFile['LevelsList']:
            self.levelsList.append(level)

        for level in self.levelsList:
            self.comboBox.addItem (str(level))

        self.scrollArea = QtGui.QScrollArea()

        if(self.nothis is False):
            if(self.edit == None):
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.parent.myMap
                self.currentTileSet = self.parent.parent.myTileSet
        else:
            self.currentLevel=TileXtra.MapFormat()
            self.currentLevel.load(TXWdgt.getLevelPathFromInitFile(self.gamefolder,self.comboBox.itemText(0)) )
            self.currentTileSet = TileXtra.TileSet( self.currentLevel.tileImage,self.currentLevel.palette)

        self.myMiniMapWidget = TXWdgt.MiniMapWidget(self.currentLevel,self.currentTileSet,self)

        self.eventList = self.currentLevel.getTileListFromLayer(EVENTSLAYER)[:]
        self.eventList.insert(0,"remove")
        self.eventList.insert(0,"keep")
        self.eventList = [str(x) for x in self.eventList]

        self.checkbox = QCheckBox("instead use event location", self)



        self.scrollArea.setWidget(self.myMiniMapWidget)

        self.connect(self.myMiniMapWidget, SIGNAL('selectedTile()'), self.setTeleportPlace)
        self.LineTextPlace = QLineEdit ()

        self.myMiniPaletteWidget = TXWdgt.MiniPaletteWidget(self.currentTileSet,self)
        self.connect(self.myMiniPaletteWidget, SIGNAL('selectedTilePalette()'), self.setTileToChange)
        self.LineTextTile = QLineEdit ()


        self.comboBoxLayers = QComboBox()

        for layer in TileXtra.LayersNameViewable:
            self.comboBoxLayers.addItem (str(layer))

        self.comboBoxColision = QComboBox()

        for item in self.colisionList:
            self.comboBoxColision.addItem (str(item))

        self.comboBoxEvent = QComboBox()

        for item in self.eventList:
            self.comboBoxEvent.addItem (str(item))

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.comboBox.currentIndexChanged.connect(self.updateMap)
        self.checkbox.stateChanged.connect(self.checkboxChanged)

        self.checkbox.setCheckState(Qt.Checked)

        self.LineTextPlace.setReadOnly(True);
        self.LineTextTile.setReadOnly(True);

        if(edit != None):

            self.myMiniPaletteWidget.setImageCurrent(int(edit[0]))

            for idx, val in enumerate(TileXtra.LayersNameViewable):
                if(val==edit[1]):
                    self.comboBoxLayers.setCurrentIndex(idx)

            for idx, val in enumerate(self.colisionList):
                if(val==edit[2]):
                    self.comboBoxColision.setCurrentIndex(idx)

            for idx, val in enumerate(self.eventList):
                if(val==edit[3]):
                    self.comboBoxEvent.setCurrentIndex(idx)

            if(edit[4]!=self.useCurrentPlace):
                self.checkbox.setCheckState(Qt.Unchecked)
                self.LineTextPlace.setText("{0};{1};{2}".format(edit[4],edit[5],edit[6]))

                for idx, val in enumerate(self.levelsList):
                    if(val==edit[6]):
                        self.comboBox.setCurrentIndex(idx)

            else:
                self.checkbox.setCheckState(Qt.Checked)


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
        textToReturn = "{0};{1};{2}".format(position[0], position[1], str(self.comboBox.currentText()) )
        self.LineTextPlace.setText(textToReturn)
        self.checkbox.setCheckState(Qt.Unchecked)

    def setTileToChange(self):
        tile = self.myMiniPaletteWidget.getValue()
        textToReturn = "{0}".format(tile)
        self.LineTextTile.setText(textToReturn)

    def updateMap(self,levelIndex):

        if (str(self.comboBox.itemText(levelIndex)) != "this"):
            self.currentLevel=TileXtra.MapFormat()
            self.currentLevel.load(TXWdgt.getLevelPathFromInitFile(self.gamefolder,self.comboBox.itemText(levelIndex)) )
            self.currentTileSet = TileXtra.TileSet( self.currentLevel.tileImage,self.currentLevel.palette)
        else:
            if(self.edit == None):
                self.currentLevel = self.parent.parent.parent.myMap
                self.currentTileSet = self.parent.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.parent.myMap
                self.currentTileSet = self.parent.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self,self.currentLevel,self.currentTileSet )
        self.myMiniPaletteWidget.drawPalette(self.currentTileSet )

    def getValue(self):
        text = str(self.LineTextTile.text())+";"+str(self.comboBoxLayers.currentText())+";"+str(self.comboBoxColision.currentText())+";"+str(self.comboBoxEvent.currentText())+";"+str(self.LineTextPlace.text())
        return text

class teleport(QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, selectStartPosition=None,  **kwargs):
    	QDialog.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.selectStartPosition = selectStartPosition
        self.gamefolder = gamefolder
        self.edit = edit
        self.parent = parent

        self.initFile = TXWdgt.openInitFile(gamefolder)

    	self.VBox = QVBoxLayout(self)
    	self.VBox.setAlignment(Qt.AlignTop)

    	self.LabelText = QLabel("Select where to teleport:")

        self.comboBox = QComboBox()

        if(self.nothis is False):
            self.levelsList = ["this"]
        else:
            self.levelsList = []


        for level in self.initFile['LevelsList']:
            self.levelsList.append(level)

        for level in self.levelsList:
            self.comboBox.addItem (str(level))

        self.scrollArea = QtGui.QScrollArea()

        if(self.nothis is False):
            if(self.selectStartPosition==None):
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
            self.currentLevel=TileXtra.MapFormat()
            self.currentLevel.load(TXWdgt.getLevelPathFromInitFile(self.gamefolder,self.comboBox.itemText(0)) )
            self.currentTileSet = TileXtra.TileSet( self.currentLevel.tileImage,self.currentLevel.palette)

        self.myMiniMapWidget = TXWdgt.MiniMapWidget(self.currentLevel,self.currentTileSet,self)

        self.scrollArea.setWidget(self.myMiniMapWidget)

        self.connect(self.myMiniMapWidget, SIGNAL('selectedTile()'), self.setTeleportPlace)
        self.LineText = QLineEdit ()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.comboBox.currentIndexChanged.connect(self.updateMap)

        self.LineText.setReadOnly(True);

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.comboBox)
        self.VBox.addWidget(self.scrollArea)
        self.VBox.addWidget(self.LineText)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 200, 350, 650)

        if(selectStartPosition == None):
            self.setWindowTitle('Select where to teleport...')
        else:
            self.setWindowTitle(selectStartPosition)

        if(edit != None):
            self.LineText.setText("{0};{1}".format(edit[0],edit[1]))

            for idx, val in enumerate(self.levelsList):
                if(val==edit[2]):
                    self.comboBox.setCurrentIndex(idx)
                    break

            self.updateMap(idx)


    def setTeleportPlace(self):
        position = self.myMiniMapWidget.getValue()
        textToReturn = "{0};{1}".format(position[0],position[1])
        self.LineText.setText(textToReturn)

    def updateMap(self,levelIndex):
        if (str(self.comboBox.itemText(levelIndex)) != "this"):
            self.currentLevel=TileXtra.MapFormat()
            self.currentLevel.load(TXWdgt.getLevelPathFromInitFile(self.gamefolder,self.comboBox.itemText(levelIndex)) )
            self.currentTileSet = TileXtra.TileSet( self.currentLevel.tileImage,self.currentLevel.palette)
        else:
            if(self.selectStartPosition==None):
                if(self.edit == None):
                    self.currentLevel = self.parent.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.parent.myTileSet
                else:
                    self.currentLevel = self.parent.parent.myMap
                    self.currentTileSet = self.parent.parent.myTileSet
            else:
                self.currentLevel = self.parent.myMap
                self.currentTileSet = self.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self,self.currentLevel,self.currentTileSet )

    def getValue(self):
        text = str(self.LineText.text())+";"+str(self.comboBox.currentText())
        return text

class showText(QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
    	QDialog.__init__(self, parent, **kwargs)

    	self.VBox = QVBoxLayout(self)
    	self.VBox.setAlignment(Qt.AlignTop)

    	self.LabelText = QLabel("Write the text in the box below:")

        self.LineText = QPlainTextEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(self.LabelText)
        self.VBox.addWidget(self.LineText)
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
            textToReturn += '\\n'+line
        return textToReturn

class fadeIn(QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
    	QDialog.__init__(self, parent, **kwargs)

        self.VBox = QVBoxLayout(self)
        self.VBox.setAlignment(Qt.AlignTop)
        self.LabelText = QLabel("Select the effect to use:")
        self.ListEffect = QListWidget()

        effects = [["pixelize","pixelizeFadeIn"],["black","blackFadeIn"],["white","whiteFadeIn"]]

        for effect in effects:
            item = QListWidgetItem(effect[0])
            item.setWhatsThis(effect[1])
            self.ListEffect.addItem(item)

        self.checkbox = QCheckBox("keep effect after")
        self.checkbox.setCheckState(Qt.Unchecked)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

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
                if(val[1]==edit[0]):
                    self.ListEffect.setItemSelected(self.ListEffect.item(idx), True)

            if(edit[1]=='keepEffect'):
                self.checkbox.setCheckState(Qt.Checked)

    def getValue(self):
        effecToReturn = str(self.ListEffect.selectedItems()[0].whatsThis())
        keepEffect = 'doNotKeep'
        if self.checkbox.isChecked():
            keepEffect = 'keepEffect'
        return effecToReturn+';'+keepEffect

class fadeOut(QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
    	QDialog.__init__(self, parent, **kwargs)

        self.VBox = QVBoxLayout(self)
        self.VBox.setAlignment(Qt.AlignTop)
        self.LabelText = QLabel("Select the effect to use:")
        self.ListEffect = QListWidget()

        effects = [["pixelize","pixelizeFadeOut"],["black","blackFadeOut"],["white","whiteFadeOut"]]

        for effect in effects:
            item = QListWidgetItem(effect[0])
            item.setWhatsThis(effect[1])
            self.ListEffect.addItem(item)

        self.checkbox = QCheckBox("keep effect after")
        self.checkbox.setCheckState(Qt.Unchecked)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

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
                if(val[1]==edit[0]):
                    self.ListEffect.setItemSelected(self.ListEffect.item(idx), True)

            if(edit[1]=='keepEffect'):
                self.checkbox.setCheckState(Qt.Checked)


    def getValue(self):
        effecToReturn = str(self.ListEffect.selectedItems()[0].whatsThis())
        keepEffect = 'doNotKeep'
        if self.checkbox.isChecked():
            keepEffect = 'keepEffect'
        return effecToReturn+';'+keepEffect

class noEffect(QDialog):
    def __init__(self, gamefolder, parent=None, edit=None, nothis=False, **kwargs):
    	QDialog.__init__(self, parent, **kwargs)

        self.accept

    def getValue(self):
        return ""
