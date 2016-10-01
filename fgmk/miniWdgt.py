# -*- coding: utf-8 -*-
import os.path
from PyQt5 import QtWidgets, QtCore
from fgmk import base_tile, tMat, tile_set, current_project, fifl, game_init
from fgmk.ff import item_format, palette_format, mapfile

class tinyPreviewPalWidget(QtWidgets.QWidget):
    selectedTilePalette = QtCore.pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)

        scrollArea = QtWidgets.QScrollArea()

        #number of collumns
        self.cn = 12

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

        self.VBox.addWidget(scrollArea)
        self.setMinimumSize(32 * (self.cn + 1) * self.scale, 32 * (1 + 1) * self.scale)

    def updatePal(self, palfile,gamefolder):
        mypal = palette_format.PaletteFormat()
        mypal.load(palfile)
        tilePalette=mypal.gettiles()
        imageFile=os.path.join(gamefolder,mypal.getimg())

        self.tileSetInstance = tile_set.TileSet(imageFile,tilePalette)

        if len(self.PaletteTileList) > 0:
            for wdgt in self.PaletteTileList:
                self.Grid.removeWidget(wdgt)
                wdgt.deleteLater()
                wdgt.setParent(None)
                wdgt = None
            self.PaletteTileList = []

        for i in range(len(self.tileSetInstance.tileset)):
            self.PaletteTileList.append(base_tile.QTile())
            self.Grid.addWidget(self.PaletteTileList[-1], i / self.cn, i % self.cn)
            self.PaletteTileList[-1].initTile(self.tileSetInstance.tileset,
                                              i, 0, self.tileSetInstance.boxsize, [i, 0, 0, 0, 0], self.scale)


        width= self.cn * self.tileSetInstance.boxsize  * self.scale
        height= tMat.divideRoundUp(len(self.tileSetInstance.tileset), self.cn) * self.tileSetInstance.boxsize  * self.scale
        self.PaletteItems.resize(width,height)

    def clear(self):
        if len(self.PaletteTileList) > 1:
            for wdgt in self.PaletteTileList:
                self.Grid.removeWidget(wdgt)
                wdgt.deleteLater()
                wdgt.setParent(None)
                wdgt = None
            self.PaletteTileList = []

class MiniPaletteWidget(QtWidgets.QWidget):
    selectedTilePalette = QtCore.pyqtSignal()

    def __init__(self, pMyTileset, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

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
        self.CurrentTT = base_tile.QTile(self)
        self.CurrentTT.initTile(self.tileSetInstance.tileset, len(self.tileSetInstance.tileset) - 1,
                                0, self.tileSetInstance.boxsize, [self.currentTile, 0, 0, 0, 0], self.scale * 2)

        self.VBox.addWidget(scrollArea)
        self.VBox.addWidget(self.CurrentTT)

        self.setMinimumSize(self.tileSetInstance.boxsize * (6 + 1) *
                            self.scale, self.tileSetInstance.boxsize * (1 + 1) * self.scale)

    def drawPalette(self, tileSetInstance):
        self.tileSetInstance = tileSetInstance

        if len(self.PaletteTileList) > 0:
            for wdgt in self.PaletteTileList:
                self.Grid.removeWidget(wdgt)
                wdgt.deleteLater()
                wdgt.setParent(None)
                wdgt = None
            self.PaletteTileList = []

        for i in range(len(tileSetInstance.tileset)):
            self.PaletteTileList.append(base_tile.QTile())
            self.Grid.addWidget(self.PaletteTileList[-1], i / 6, i % 6)
            self.PaletteTileList[-1].initTile(tileSetInstance.tileset,
                                              i, 0, tileSetInstance.boxsize, [i, 0, 0, 0, 0], self.scale)
            self.PaletteTileList[-1].clicked.connect(self.setTileCurrent)

        self.PaletteItems.resize(6 * tileSetInstance.boxsize, tMat.divideRoundUp(
            len(tileSetInstance.tileset), 6) * tileSetInstance.boxsize)

    def setTileCurrent(self, ev):
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
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

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
        self.indicativeToUse=indicativeToUse

        if(indicativeToUse>0):
            self.xclicked = base_tile.QTile(self)
            self.xclicked.initTile(tile_set.indicativeSet.tileset, 0, 0, 32, [indicativeToUse,0,0,0,0], 0.5)

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
                self.TileList[iy].append(base_tile.QTile(self))
                self.Grid.addWidget(self.TileList[iy][jx], iy, jx)
                self.TileList[iy][jx].initTile(tileset, jx, iy, boxsize, LayersMapTiles[
                                               :, iy, jx], self.myScale)
                self.TileList[iy][jx].clicked.connect(self.TileClicked)

        self.resize(self.TileWidth * boxsize * self.myScale,
                    self.TileHeight * boxsize * self.myScale)
        self.setVisible(True)


        self.changeSelectXY(self.selectedPosition[0], self.selectedPosition[1])

    def changeSelectXY(self, x, y):
        if(self.indicativeToUse>0):
            self.TileList[self.selectedPosition[1]][self.selectedPosition[0]].setVisible(True)

            self.selectedPosition = [x, y]

            self.Grid.removeWidget(self.xclicked)
            self.TileList[self.selectedPosition[1]][self.selectedPosition[0]].setVisible(False)
            self.Grid.addWidget(self.xclicked, self.selectedPosition[1], self.selectedPosition[0])

    def TileClicked(self, ev):
        sender = self.sender()
        self.changeSelectXY(sender.tileX, sender.tileY)

        self.selectedTile.emit()

    def getValue(self):
        return self.selectedPosition


class levelSelector(QtWidgets.QComboBox):
    def __init__(self,parent=None, nothis=False, **kwargs):
        QtWidgets.QComboBox.__init__(self, parent, **kwargs)

        self.nothis = nothis
        self.initFile = game_init.openInitFile(current_project.settings['gamefolder'])
        if(self.nothis is False):
            self.levelsList = ["this"]
        else:
            self.levelsList = []

        for level in self.initFile['LevelsList']:
            self.levelsList.append(level)
        for level in self.levelsList:
            self.addItem(str(level))

    def edit(self, param):
        for idx, val in enumerate(self.levelsList):
            if(val == param):
                self.setCurrentIndex(idx)


class MiniMapViewer(QtWidgets.QWidget):
    selectedTile = QtCore.pyqtSignal()
    def __init__(self,parent=None, mapAtStart=None, nothis=False, myMap=None, indicative=1, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.myMap = myMap
        self.mapAtStart = mapAtStart
        self.nothis = nothis
        self.gamefolder = current_project.settings["gamefolder"]

        if(self.nothis is False):
            self.currentLevel = self.myMap
            self.currentTileSet = self.myMap.parent.myTileSet

        elif(self.mapAtStart != None):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, self.mapAtStart))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                self.gamefolder, self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            self.currentLevel = mapfile.MapFormat()
            self.currentTileSet = tile_set.TileSet(os.path.join(
                self.gamefolder, self.currentLevel.tileImage),
                self.currentLevel.palette)

        self.scrollArea = QtWidgets.QScrollArea()
        self.myMiniMapWidget = MiniMapWidget(self.currentLevel, self.currentTileSet, None, indicative)
        self.myMiniMapWidget.selectedTile.connect(self.emitSelectedTile)
        self.scrollArea.setWidget(self.myMiniMapWidget)
        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.VBox.addWidget(self.scrollArea)

    def getValue(self):
        return self.myMiniMapWidget.getValue()

    def updateMap(self, mapname):
        if (str(mapname) != "this"):
            self.currentLevel = mapfile.MapFormat()
            self.currentLevel.load(game_init.getLevelPathFromInitFile(
                self.gamefolder, mapname))
            self.currentTileSet = tile_set.TileSet(os.path.join(
                self.gamefolder, self.currentLevel.tileImage),
                self.currentLevel.palette)
        else:
            self.currentLevel = self.myMap
            self.currentTileSet = self.myMap.parent.myTileSet

        self.myMiniMapWidget.DrawMap(self.currentLevel, self.currentTileSet)

    def emitSelectedTile(self):
        self.selectedTile.emit()



class miniItemsList(QtWidgets.QWidget):
    def __init__(self,parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.itemf = item_format.ItemsFormat(os.path.join(current_project.settings['gamefolder'],fifl.ITEMSFILE))
        self.itemsList = QtWidgets.QListWidget(self)
        self.itemsList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.load()
        VBox = QtWidgets.QVBoxLayout(self)
        VBox.addWidget(self.itemsList)
        self.setLayout(VBox)

    def load(self):
        self.itemsList.clear()
        items = self.itemf.getitemsname()
        for i in range(len(items)):
            item = items[i]
            self.itemsList.addItem(item)

        self.itemsList.setCurrentRow(0)

    def getItem(self):
        listitem = self.itemsList.currentItem()
        if(listitem != None):
            return listitem.text()
        else:
            return None

    def setItem(self,itemname):
        for i in range(self.itemsList.count()):
            item = self.itemsList.item(i)
            if(item.text()==itemname):
                self.itemsList.setCurrentRow(i)
                return
