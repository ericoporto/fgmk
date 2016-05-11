import sys
import json
import os.path
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import tMat
import actionDialog
import TileXtra
import fifl

def getLevelPathFromInitFile(gamefolder,levelname):
    initFile=openInitFile(gamefolder)
    return os.path.join(str(gamefolder), fifl.LEVELS,initFile['LevelsList'][str(levelname)])

def openInitFile(gamefolder):
    f = open(os.path.join(str(gamefolder), fifl.DESCRIPTORS,fifl.GAMESETTINGS ), "r" )
    initFileJsonTree = json.load(f)
    f.close()
    return initFileJsonTree

def saveInitFile(gamefolder, initFileJsonTree):
    f = open(os.path.join(str(gamefolder), fifl.DESCRIPTORS,fifl.GAMESETTINGS ), "w" )
    initFileJsonTree = json.dump(initFileJsonTree, f, indent=4, sort_keys=True)
    f.close()
    return initFileJsonTree

def selectStartingPosition(parent, psSettings):
    myTeleporDialog = actionDialog.teleport(psSettings["gamefolder"],parent, None, False, "select starting position")
    if myTeleporDialog.exec_() == QtGui.QDialog.Accepted:
        returnActDlg = str(myTeleporDialog.getValue())
        position=returnActDlg.split(';')
        initFileJsonTree = openInitFile(psSettings["gamefolder"])
        initFileJsonTree["Player"]["initPosX"] = int(position[0])*32
        initFileJsonTree["Player"]["initPosY"] = (int(position[1])-1)*32
        if(str(position[2]) != "this"):
            initFileJsonTree["World"]["initLevel"] = str(position[2])
        else:
            initFileJsonTree["World"]["initLevel"] = str(parent.myMap.levelName)
        return [initFileJsonTree,str(position[2])]



class CommandCTTileType(QUndoCommand):
    def __init__(self, child, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, description):
        super(CommandCTTileType, self).__init__(description)

        self.sender = senderTileWdgt
        self.tileX = self.sender.tileX
        self.tileY = self.sender.tileY
        self.Layer = layer
        self.changeTypeTo = changeTypeTo
        self.oldType = self.sender.tileType[layer]

        self.pmyMapWidget = child.myMapWidget
        self.pMap = pMap
        self.ptileset = ptileset

    def redo(self):
        self.pMap.setTile( self.tileX, self.tileY, self.Layer, self.changeTypeTo)
        self.sender.updateTileImageInMap( self.changeTypeTo, self.Layer, self.ptileset, self.pmyMapWidget.myScale)
        #print("Type= ", self.changeTypeTo, "  X= " ,self.tileX, "  Y= " , self.tileY)


    def undo(self):
        self.pMap.setTile( self.tileX, self.tileY, self.Layer, self.oldType)
        self.sender.updateTileImageInMap( self.oldType, self.Layer, self.ptileset , self.pmyMapWidget.myScale)
        #print("Type= ", self.oldType, "  X= " ,self.tileX, "  Y= " , self.tileY)


class CommandCGroupTType(QUndoCommand):
    def __init__(self, child, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, listToChange, description):
        super(CommandCGroupTType, self).__init__(description)

        self.tileX = senderTileWdgt.tileX
        self.tileY = senderTileWdgt.tileY
        self.Layer = layer
        self.changeTypeTo = changeTypeTo

        self.pmyMapWidget = child.myMapWidget
        self.pMap = pMap
        self.ptileset = ptileset

        self.listToChange = listToChange

    def redo(self):
        for change in self.listToChange:
            tile = self.pmyMapWidget.TileList[change[1]][change[0]]
            self.pMap.setTile( change[0], change[1], self.Layer, change[3])
            tile.updateTileImageInMap( change[3], self.Layer, self.ptileset , self.pmyMapWidget.myScale)
            #print("Type= ", change[3], "  X= " , change[0], "  Y= " , change[1])

    def undo(self):
        for change in self.listToChange:
            tile = self.pmyMapWidget.TileList[change[1]][change[0]]
            self.pMap.setTile( change[0], change[1], self.Layer, change[2])
            tile.updateTileImageInMap( change[2], self.Layer, self.ptileset , self.pmyMapWidget.myScale)
            #print("Type= ", change[2], "  X= " ,change[0], "  Y= " , change[1])

class newProject(QDialog):
    def __init__(self, parent=None, **kwargs):
        QDialog.__init__(self, parent, **kwargs)

        self.returnValue = { "name" : "NewFile", "baseFolder" : "" }

        self.VBox = QVBoxLayout(self)
        self.VBox.setAlignment(Qt.AlignTop)

        HBoxFolder = QHBoxLayout()
        self.LineEditFolder = QLineEdit ()
        self.LineEditFolder.setReadOnly(True);
        self.LineEditFolder.setText(str(self.returnValue["baseFolder"]))
        self.buttonFolder = QPushButton("Browse")
        self.buttonFolder.clicked.connect(self.selectGameFolder)
        HBoxFolder.addWidget(self.LineEditFolder)
        HBoxFolder.addWidget(self.buttonFolder)

        HBoxName = QHBoxLayout()
        self.LineEditName = QLineEdit ()
        self.LineEditName.setText(str(self.returnValue["name"]))
        self.LineEditName.editingFinished.connect(self.validateLineEditName)
        HBoxName.addWidget(QLabel("Name:"))
        HBoxName.addWidget(self.LineEditName)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(QLabel("THIS FUNCTION IS NOT COMPLETE YET"))
        self.VBox.addWidget(QLabel("Select folder to create game:"))
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(QLabel("Set game name:"))
        self.VBox.addLayout(HBoxName)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('New game project...')

    def validateLineEditName(self):
        tempStr = str(self.LineEditName.text())
        tempStr=tempStr.title()
        tempStr=tempStr.replace(" ", "")
        self.LineEditName.setText(tempStr)
        self.returnValue["name"] = self.LineEditName.text()
        self.validateIsOk()

    def selectGameFolder(self):
        self.LineEditFolder.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")) )
        self.returnValue["baseFolder"] = self.LineEditFolder.text()
        self.validateIsOk()

    def validateIsOk(self):
        if self.returnValue["name"] != "" and self.returnValue["baseFolder"] != "":
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def getValue(self):
        return self.returnValue

class newFile(QDialog):
    def __init__(self, parent=None, **kwargs):
        QDialog.__init__(self, parent, **kwargs)

        self.returnValue = { "name" : "NewFile", "width" : 15, "height" : 15, "gameFolder" : ""

        }

        self.VBox = QVBoxLayout(self)
        self.VBox.setAlignment(Qt.AlignTop)

        HBoxFolder = QHBoxLayout()
        self.LineEditFolder = QLineEdit ()
        self.LineEditFolder.setReadOnly(True);
        self.LineEditFolder.setText(str(self.returnValue["gameFolder"]))
        self.buttonFolder = QPushButton("Browse")
        self.buttonFolder.clicked.connect(self.selectGameFolder)
        HBoxFolder.addWidget(self.LineEditFolder)
        HBoxFolder.addWidget(self.buttonFolder)

        HBoxSize = QHBoxLayout()
        self.LineEditWidth = QLineEdit ()
        self.LineEditWidth.setInputMask("000")
        self.LineEditWidth.setText(str(self.returnValue["width"]))
        self.LineEditWidth.editingFinished.connect(self.validateLineEditWidth)
        self.LineEditHeight = QLineEdit ()
        self.LineEditHeight.setInputMask("000")
        self.LineEditHeight.setText(str(self.returnValue["height"]))
        self.LineEditHeight.editingFinished.connect(self.validateLineEditHeight)
        HBoxSize.addWidget(QLabel("Width:"))
        HBoxSize.addWidget(self.LineEditWidth)
        HBoxSize.addWidget(QLabel("Height:"))
        HBoxSize.addWidget(self.LineEditHeight)

        HBoxName = QHBoxLayout()
        self.LineEditName = QLineEdit ()
        self.LineEditName.setText(str(self.returnValue["name"]))
        self.LineEditName.editingFinished.connect(self.validateLineEditName)
        HBoxName.addWidget(QLabel("Name:"))
        HBoxName.addWidget(self.LineEditName)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(QLabel("Select game folder:"))
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(QLabel("Set map properties:"))
        self.VBox.addLayout(HBoxSize)
        self.VBox.addLayout(HBoxName)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('New map...')

    def validateLineEditWidth(self):
        if int(self.LineEditWidth.text()) < 15:
            self.LineEditWidth.setText("15")
        elif int(self.LineEditWidth.text()) > 100:
            self.LineEditWidth.setText("100")
        else:
            self.LineEditWidth.setText(str(int(self.LineEditWidth.text())))
        self.returnValue["width"] = int(self.LineEditWidth.text())
        self.validateIsOk()

    def validateLineEditHeight(self):
        if int(self.LineEditHeight.text()) < 15:
            self.LineEditHeight.setText("15")
        elif int(self.LineEditHeight.text()) > 100:
            self.LineEditHeight.setText("100")
        else:
            self.LineEditHeight.setText(str(int(self.LineEditHeight.text())))
        self.returnValue["height"] = int(self.LineEditHeight.text())
        self.validateIsOk()

    def validateLineEditName(self):
        tempStr = str(self.LineEditName.text())
        tempStr=tempStr.title()
        tempStr=tempStr.replace(" ", "")
        self.LineEditName.setText(tempStr)
        self.returnValue["name"] = self.LineEditName.text()
        self.validateIsOk()

    def selectGameFolder(self):
        self.LineEditFolder.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")) )
        self.returnValue["gameFolder"] = self.LineEditFolder.text()
        self.validateIsOk()

    def validateIsOk(self):
        if self.returnValue["name"] != "" and self.returnValue["gameFolder"] != "":
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def getValue(self):
        return self.returnValue

class ActionsWidget(QDialog):
    def __init__(self, psSettings, parent=None, ischaras=False, **kwargs):
        QDialog.__init__(self, parent, **kwargs)
        self.psSettings=psSettings
        self.ischaras = ischaras

        self.VBox = QVBoxLayout(self)
        self.VBox.setAlignment(Qt.AlignTop)

        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"actions/actionsList.json")
        f = open( filepath, "rb" )
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
            self.returnValue = [str(self.returnValue),""]
            self.accept()
        else:
            newDialogFromName = getattr(actionDialog, str(self.returnValue))
            if(self.ischaras is False):
                self.myActionsDialog = newDialogFromName(self.psSettings["gamefolder"],self)
            else:
                self.myActionsDialog = newDialogFromName(self.psSettings["gamefolder"],self,None,True)

            if self.myActionsDialog.exec_() == QtGui.QDialog.Accepted:
                returnActDlg = str(self.myActionsDialog.getValue())

                #self.returnValue.append('|')
                self.returnValue = [str(self.returnValue),str(returnActDlg)]
                self.accept()

    def getValue(self):
        return self.returnValue


class MiniPaletteWidget(QWidget):
    def __init__(self, pMyTileset, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.VBox = QVBoxLayout(self)

        self.tileSetInstance = pMyTileset

        scrollArea = QtGui.QScrollArea()

        self.scale = 1
        self.PaletteItems = QtGui.QWidget()
        self.Grid = QGridLayout()

        self.PaletteItems.setLayout(self.Grid)
        scrollArea.setWidget(self.PaletteItems)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.PaletteTileList = []

        self.drawPalette(self.tileSetInstance)

        self.currentTile = 0
        self.CurrentTT = TileXtra.ExtendedQLabel(self)
        self.CurrentTT.initTile(self.tileSetInstance.tileset, len(self.tileSetInstance.tileset)-1  , 0 , self.tileSetInstance.boxsize, [self.currentTile,0,0,0,0], self.scale*2)

        self.VBox.addWidget(scrollArea)
        self.VBox.addWidget(self.CurrentTT)

        self.setMinimumSize (self.tileSetInstance.boxsize*(6+1)*self.scale,self.tileSetInstance.boxsize*(1+1)*self.scale)

    def drawPalette(self, tileSetInstance):
        self.tileSetInstance = tileSetInstance

        if len(self.PaletteTileList) > 1:
            for wdgt in self.PaletteTileList:
                wdgt.deleteLater()
                wdgt = None
            self.PaletteTileList = []

        for i in range(len(tileSetInstance.tileset) ):
            self.PaletteTileList.append(TileXtra.ExtendedQLabel(self))
            self.Grid.addWidget(self.PaletteTileList[-1], i/6, i%6)
            self.PaletteTileList[-1].initTile( tileSetInstance.tileset, i , 0 , tileSetInstance.boxsize, [i,0,0,0,0], self.scale)
            self.connect(self.PaletteTileList[-1], SIGNAL('clicked()'), self.setTileCurrent)

        self.PaletteItems.resize(6*tileSetInstance.boxsize,TileXtra.divideRoundUp(len(tileSetInstance.tileset),6)*tileSetInstance.boxsize)

    def setTileCurrent(self):
        self.setImageCurrent(self.sender().tileType[0])
        self.emit(SIGNAL('selectedTilePalette()'))

    def setImageCurrent(self, imageIndex):
        self.currentTile = imageIndex
        self.CurrentTT.initTile( self.tileSetInstance.tileset, 0 , 0 ,  self.tileSetInstance.boxsize, [imageIndex,0,0,0,0], self.scale*2)
        self.CurrentTT.show()

    def getValue(self):
        return self.currentTile


class MiniMapWidget(QWidget):
    def __init__(self, pMyMap, pMyTileset, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.Grid = QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.pMyMap = pMyMap
        self.pMyTileset = pMyTileset

        self.TileWidth = 0
        self.TileHeight = 0
        self.myScale = 0.5

        self.TileList = []
        self.selectedPosition = [0,0]
        self.DrawMap(parent,pMyMap,pMyTileset)

    def DrawMap(self, parent,pMyMap,pMyTileset):
        self.setVisible(False)
        self.pMyMap = pMyMap
        self.pMyTileset = pMyTileset

        LayersMapTiles = self.pMyMap .LayersMapTiles
        tileset = self.pMyTileset.tileset
        boxsize = self.pMyTileset.boxsize


        if len(self.TileList) > 1:
            for collum in self.TileList:
                for wdgt in collum:
                    wdgt.deleteLater()
                    wdgt = None
            self.TileList = []

        self.TileHeight = len(LayersMapTiles[0])
        self.TileWidth = len(LayersMapTiles[0][0])

        # for i in height
        for iy in xrange(self.TileHeight):
            # for j in width
            self.TileList.append([])
            for jx in range(self.TileWidth):
                self.TileList[iy].append(TileXtra.ExtendedQLabel(self))
                self.Grid.addWidget(self.TileList[iy][jx], iy, jx)
                self.TileList[iy][jx].initTile( tileset, jx , iy, boxsize, LayersMapTiles[:,iy,jx], self.myScale)
                self.connect(self.TileList[iy][jx], SIGNAL('clicked()'), self.TileClicked)

        self.resize(self.TileWidth*boxsize*self.myScale, self.TileHeight*boxsize*self.myScale)
        self.setVisible(True)

    def TileClicked(self):

        sender = self.sender()
        self.selectedPosition = [sender.tileX, sender.tileY]

        LayersMapTiles = self.pMyMap.LayersMapTiles
        boxsize = self.pMyTileset.boxsize
        scale = self.myScale

        for i in range(self.TileWidth):
            for j in range(self.TileHeight):

                if (j==self.selectedPosition[1]):
                    self.Grid.setRowMinimumHeight(j,boxsize*scale+1)
                elif (j==self.selectedPosition[1]-1):
                    self.Grid.setRowMinimumHeight(j,boxsize*scale+1)
                else:
                    self.Grid.setRowMinimumHeight(j,boxsize*scale)

                if (i==self.selectedPosition[0]):
                    self.Grid.setColumnMinimumWidth(i,boxsize*scale+1)
                elif (i==self.selectedPosition[0]-1):
                    self.Grid.setColumnMinimumWidth(i,boxsize*scale+1)
                else:
                    self.Grid.setColumnMinimumWidth(i,boxsize*scale)


        self.resize(len(LayersMapTiles[0])*boxsize*self.myScale+2,len(LayersMapTiles[0][0])*boxsize*self.myScale+2)
        self.emit(SIGNAL('selectedTile()'))

    def getValue(self):
        return self.selectedPosition
