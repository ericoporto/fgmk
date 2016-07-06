import json
import os.path
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import tMat,  TileXtra, fifl, proj


def getLevelPathFromInitFile(gamefolder, levelname):
    initFile = openInitFile(gamefolder)
    return os.path.join(str(gamefolder), fifl.LEVELS, initFile['LevelsList'][str(levelname)])


def openInitFile(gamefolder):
    fname = os.path.join(str(gamefolder), fifl.DESCRIPTORS, fifl.GAMESETTINGS)

    if os.path.isfile(fname):
        f = open(fname, "r")
        initFileJsonTree = json.load(f)
        f.close()
        return initFileJsonTree
    else:
        return None


def saveInitFile(gamefolder, initFileJsonTree):
    f = open(os.path.join(str(gamefolder),
                          fifl.DESCRIPTORS, fifl.GAMESETTINGS), "w")
    initFileJsonTree = json.dump(initFileJsonTree, f, indent=4, sort_keys=True)
    f.close()
    return initFileJsonTree


class CommandCTTileType(QtWidgets.QUndoCommand):

    def __init__(self, child, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, description):
        super().__init__(description)

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
        self.pMap.setTile(self.tileX, self.tileY,
                          self.Layer, self.changeTypeTo)
        self.sender.updateTileImageInMap(
            self.changeTypeTo, self.Layer, self.ptileset, self.pmyMapWidget.myScale)
        #print("Type= ", self.changeTypeTo, "  X= " ,self.tileX, "  Y= " , self.tileY)

    def undo(self):
        self.pMap.setTile(self.tileX, self.tileY, self.Layer, self.oldType)
        self.sender.updateTileImageInMap(
            self.oldType, self.Layer, self.ptileset, self.pmyMapWidget.myScale)
        #print("Type= ", self.oldType, "  X= " ,self.tileX, "  Y= " , self.tileY)


class CommandCGroupTType(QtWidgets.QUndoCommand):

    def __init__(self, child, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, listToChange, description):
        super().__init__(description)

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
            self.pMap.setTile(change[0], change[1], self.Layer, change[3])
            tile.updateTileImageInMap(
                change[3], self.Layer, self.ptileset, self.pmyMapWidget.myScale)
            #print("Type= ", change[3], "  X= " , change[0], "  Y= " , change[1])

    def undo(self):
        for change in self.listToChange:
            tile = self.pmyMapWidget.TileList[change[1]][change[0]]
            self.pMap.setTile(change[0], change[1], self.Layer, change[2])
            tile.updateTileImageInMap(
                change[2], self.Layer, self.ptileset, self.pmyMapWidget.myScale)
            #print("Type= ", change[2], "  X= " ,change[0], "  Y= " , change[1])


class newProject(QtWidgets.QDialog):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

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

        self.VBox.addWidget(QtWidgets.QLabel("THIS FUNCTION IS NOT COMPLETE YET"))
        self.VBox.addWidget(QtWidgets.QLabel("Select folder to create game:"))
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(QtWidgets.QLabel("Set game name:"))
        self.VBox.addLayout(HBoxName)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('New game project...')

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

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        gamefolder = ""
        if "gamefolder" in proj.settings:
            gamefolder = os.path.join(proj.settings["gamefolder"])
            if not os.path.isdir(gamefolder):
                gamefolder = ""

        self.returnValue = {"name": "NewFile", "width": 15, "height": 15, "gameFolder": gamefolder

                            }

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        HBoxFolder = QtWidgets.QHBoxLayout()
        self.LineEditFolder = QtWidgets.QLineEdit()
        self.LineEditFolder.setReadOnly(True)
        self.LineEditFolder.setText(str(self.returnValue["gameFolder"]))
        self.buttonFolder = QtWidgets.QPushButton("Browse")
        self.buttonFolder.clicked.connect(self.selectGameFolder)
        HBoxFolder.addWidget(self.LineEditFolder)
        HBoxFolder.addWidget(self.buttonFolder)

        HBoxSize = QtWidgets.QHBoxLayout()
        self.LineEditWidth = QtWidgets.QLineEdit()
        self.LineEditWidth.setInputMask("000")
        self.LineEditWidth.setText(str(self.returnValue["width"]))
        self.LineEditWidth.editingFinished.connect(self.validateLineEditWidth)
        self.LineEditHeight = QtWidgets.QLineEdit()
        self.LineEditHeight.setInputMask("000")
        self.LineEditHeight.setText(str(self.returnValue["height"]))
        self.LineEditHeight.editingFinished.connect(
            self.validateLineEditHeight)
        HBoxSize.addWidget(QtWidgets.QLabel("Width:"))
        HBoxSize.addWidget(self.LineEditWidth)
        HBoxSize.addWidget(QtWidgets.QLabel("Height:"))
        HBoxSize.addWidget(self.LineEditHeight)

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

        self.VBox.addWidget(QtWidgets.QLabel("Select game folder:"))
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(QtWidgets.QLabel("Set map properties:"))
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
        tempStr = tempStr.title()
        tempStr = tempStr.replace(" ", "")
        self.LineEditName.setText(tempStr)
        self.returnValue["name"] = self.LineEditName.text()
        self.validateIsOk()

    def selectGameFolder(self):
        self.LineEditFolder.setText(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.returnValue["gameFolder"] = self.LineEditFolder.text()
        self.validateIsOk()

    def validateIsOk(self):
        if self.returnValue["name"] != "" and self.returnValue["gameFolder"] != "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def getValue(self):
        return self.returnValue


class MiniPaletteWidget(QtWidgets.QWidget):
    selectedTilePalette = QtCore.pyqtSignal()

    def __init__(self, pMyTileset, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)

        self.tileSetInstance = pMyTileset

        scrollArea = QtWidgets.QScrollArea()

        self.scale = 1
        self.PaletteItems = QtWidgets.QWidget()
        self.Grid = QtWidgets.QGridLayout()

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
        self.CurrentTT.initTile(self.tileSetInstance.tileset, len(self.tileSetInstance.tileset) - 1,
                                0, self.tileSetInstance.boxsize, [self.currentTile, 0, 0, 0, 0], self.scale * 2)

        self.VBox.addWidget(scrollArea)
        self.VBox.addWidget(self.CurrentTT)

        self.setMinimumSize(self.tileSetInstance.boxsize * (6 + 1) *
                            self.scale, self.tileSetInstance.boxsize * (1 + 1) * self.scale)

    def drawPalette(self, tileSetInstance):
        self.tileSetInstance = tileSetInstance

        if len(self.PaletteTileList) > 1:
            for wdgt in self.PaletteTileList:
                wdgt.deleteLater()
                wdgt = None
            self.PaletteTileList = []

        for i in range(len(tileSetInstance.tileset)):
            self.PaletteTileList.append(TileXtra.ExtendedQLabel(self))
            self.Grid.addWidget(self.PaletteTileList[-1], i / 6, i % 6)
            self.PaletteTileList[-1].initTile(tileSetInstance.tileset,
                                              i, 0, tileSetInstance.boxsize, [i, 0, 0, 0, 0], self.scale)
            self.PaletteTileList[-1].clicked.connect(self.setTileCurrent)

        self.PaletteItems.resize(6 * tileSetInstance.boxsize, tMat.divideRoundUp(
            len(tileSetInstance.tileset), 6) * tileSetInstance.boxsize)

    def setTileCurrent(self):
        self.setImageCurrent(self.sender().tileType[0])
        self.selectedTilePalette.emit()

    def setImageCurrent(self, imageIndex):
        self.currentTile = imageIndex
        self.CurrentTT.initTile(self.tileSetInstance.tileset, 0, 0,  self.tileSetInstance.boxsize, [
                                imageIndex, 0, 0, 0, 0], self.scale * 2)
        self.CurrentTT.show()

    def getValue(self):
        return self.currentTile


class MiniMapWidget(QtWidgets.QWidget):
    selectedTile = QtCore.pyqtSignal()

    def __init__(self, pMyMap, pMyTileset, parent=None, indicativeToUse=1, **kwargs):
        super().__init__(parent, **kwargs)

        self.Grid = QtWidgets.QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.pMyMap = pMyMap
        self.pMyTileset = pMyTileset

        self.TileWidth = 0
        self.TileHeight = 0
        self.myScale = 0.5

        self.xclicked = TileXtra.ExtendedQLabel(self)
        self.xclicked.initTile(TileXtra.indicativeSet.tileset, 0, 0, 32, [indicativeToUse,0,0,0,0], 0.5)

        self.TileList = []
        self.selectedPosition = [0, 0]
        self.DrawMap(pMyMap, pMyTileset)

    def DrawMap(self, pMyMap, pMyTileset):
        self.setVisible(False)

        if(self.pMyMap != pMyMap):
            self.pMyMap = pMyMap
            self.selectedPosition = [0, 0]

        self.pMyTileset = pMyTileset

        LayersMapTiles = self.pMyMap.LayersMapTiles
        tileset = self.pMyTileset.tileset
        boxsize = self.pMyTileset.boxsize

        self.TileHeight = len(LayersMapTiles[0])
        self.TileWidth = len(LayersMapTiles[0][0])

        if len(self.TileList) > 1:
            for collum in self.TileList:
                for wdgt in collum:
                    self.Grid.removeWidget(wdgt)
                    wdgt.deleteLater()
                    wdgt.setParent(None)
                    wdgt = None
            self.TileList = []

        # for i in height
        for iy in range(self.TileHeight):
            # for j in width
            self.TileList.append([])
            for jx in range(self.TileWidth):
                self.TileList[iy].append(TileXtra.ExtendedQLabel(self))
                self.Grid.addWidget(self.TileList[iy][jx], iy, jx)
                self.TileList[iy][jx].initTile(tileset, jx, iy, boxsize, LayersMapTiles[
                                               :, iy, jx], self.myScale)
                self.TileList[iy][jx].clicked.connect(self.TileClicked)

        self.resize(self.TileWidth * boxsize * self.myScale,
                    self.TileHeight * boxsize * self.myScale)
        self.setVisible(True)


        self.changeSelectXY(self.selectedPosition[0], self.selectedPosition[1])

    def changeSelectXY(self, x, y):
        self.TileList[self.selectedPosition[1]][self.selectedPosition[0]].setVisible(True)

        self.selectedPosition = [x, y]

        self.Grid.removeWidget(self.xclicked)
        self.TileList[self.selectedPosition[1]][self.selectedPosition[0]].setVisible(False)
        self.Grid.addWidget(self.xclicked, self.selectedPosition[1], self.selectedPosition[0])

    def TileClicked(self):
        sender = self.sender()
        self.changeSelectXY(sender.tileX, sender.tileY)

        self.selectedTile.emit()

    def getValue(self):
        return self.selectedPosition
