# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from fgmk import base_tile, tMat, tile_set

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

        if len(self.PaletteTileList) > 1:
            for wdgt in self.PaletteTileList:
                wdgt.deleteLater()
                wdgt = None
            self.PaletteTileList = []

        for i in range(len(tileSetInstance.tileset)):
            self.PaletteTileList.append(base_tile.QTile(self))
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

    def TileClicked(self):
        sender = self.sender()
        self.changeSelectXY(sender.tileX, sender.tileY)

        self.selectedTile.emit()

    def getValue(self):
        return self.selectedPosition
