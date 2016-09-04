# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_tile, tMat
from fgmk.dock import tools_wdgt

class PaletteWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, tileSetInstance=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent=parent

        self.VBox = QtWidgets.QVBoxLayout(self)

        self.tileSetInstance = tileSetInstance

        scrollArea = QtWidgets.QScrollArea()

        self.PaletteItems = QtWidgets.QWidget()
        self.Grid = QtWidgets.QGridLayout()

        self.PaletteItems.setLayout(self.Grid)
        scrollArea.setWidget(self.PaletteItems)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.PaletteTileList = []

        self.drawPalette(tileSetInstance)

        self.CurrentTT = base_tile.QTile(self)
        self.CurrentTT.initTile(tileSetInstance.tileset, len(
            tileSetInstance.tileset) - 1, 0, tileSetInstance.boxsize, [5, 0, 0, 0, 0], 4)

        self.VBox.addWidget(scrollArea)
        self.VBox.addWidget(self.CurrentTT)

        self.setMinimumSize(tileSetInstance.boxsize * 6 +
                            32, tileSetInstance.boxsize + 32)

    def drawPalette(self, tileSetInstance):
        self.tileSetInstance = tileSetInstance

        if len(self.PaletteTileList) > 1:
            for wdgt in self.PaletteTileList:
                wdgt.deleteLater()
                wdgt = None
            self.PaletteTileList = []

        i = 0
        for key in sorted(tileSetInstance.tileset):
            self.PaletteTileList.append(base_tile.QTile(self))
            self.Grid.addWidget(self.PaletteTileList[-1], i / 6, i % 6)
            self.PaletteTileList[-1].initTile(
                tileSetInstance.tileset, i, 0, tileSetInstance.boxsize, [key, 0, 0, 0, 0], 1)
            self.PaletteTileList[-1].clicked.connect(self.setTileCurrent)
            self.PaletteTileList[-1].doubleClicked.connect(self.paletteItemDoubleClicked)
            i+=1

        self.PaletteItems.resize(6 * tileSetInstance.boxsize, tMat.divideRoundUp(
            len(tileSetInstance.tileset), 6) * tileSetInstance.boxsize)

    def paletteItemDoubleClicked(self):
        self.parent.myToolsWidget.changeLeftClickToolTo(tools_wdgt.tools['pen'])

    def setTileCurrent(self, ev):
        self.parent.changeTileCurrent(self.sender().tileType[0])

    def setImageCurrent(self, imageIndex):
        self.CurrentTT.initTile(self.tileSetInstance.tileset, 0, 0,
                                self.tileSetInstance.boxsize, [imageIndex, 0, 0, 0, 0], 4)
        self.CurrentTT.show()
