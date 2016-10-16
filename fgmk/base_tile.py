# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
from PIL import Image
from PIL.ImageQt import ImageQt

from fgmk import tMat, getdata, current_project, tile_set
from fgmk.util import img_util


class QTile(QtWidgets.QLabel):
    def __init(self, parent):
        #super().__init__(parent)
        QtWidgets.QLabel.__init__(self, parent)

    tileType = []
    tileX = 0
    tileY = 0
    boxSize = 32
    pal = False

    clicked = QtCore.pyqtSignal(object)
    rightClicked = QtCore.pyqtSignal(object)
    middleClicked = QtCore.pyqtSignal(object)
    mouseMoved = QtCore.pyqtSignal(object)
    mouseReleased = QtCore.pyqtSignal(object)
    doubleClicked = QtCore.pyqtSignal()

    def Rescale(self, tileset,  scale=1):
        self.scale = scale
        self.updateTileImageInMap(self.tileType[0], 0, tileset, self.scale)

    def initTile(self, tileset, x, y, boxSize, tileType, scale=1, pal=False):
        self.tileType = tileType
        self.tileX = x
        self.tileY = y
        self.boxSize = boxSize
        self.scale = scale
        self.pal = pal
        self.updateTileImageInMap(self.tileType[0], 0, tileset, self.scale)

    def updateTileImageInMap(self, ChangeTileType, layer, tileset,  scale=1):
        self.tileType[layer] = ChangeTileType
        self.scale = scale
        self.updateTileType(tileset)

    def updateTileType(self, tileset, tileType=None):
        if(tileType!=None):
            self.tileType = tileType
        scale = self.scale
        if(scale == 2):
            tempscale = 1
        elif(scale == 0.5):
            tempscale = 2
        else:
            tempscale = 0

        Composite = tile_set.clearTile.tileset[0][tempscale]

        for i in range(len(self.tileType) - 2):
            if(self.tileType[i]):
                Composite = img_util.alpha_composite(
                    Composite, tileset[self.tileType[i]][tempscale])

        if(self.pal==False):
            if(self.tileType[i + 1]):
                Composite = img_util.alpha_composite(Composite, tile_set.colisionSet.tileset[
                                                 self.tileType[i + 1]][tempscale])
        else:
            if(self.tileType[i + 1]):
                Composite = img_util.alpha_composite(Composite, tile_set.animSet.tileset[
                                                 self.tileType[i + 1]][tempscale])

        if(self.tileType[i + 2]):
            Composite = img_util.alpha_composite(Composite, tile_set.eventSet.tileset[
                                             self.tileType[i + 2]][tempscale])

        if(scale != 1 and scale != 0.5 and scale != 2):
            Composite = Composite.resize(
                (int(self.boxSize * scale), int(self.boxSize * scale)), Image.NEAREST)

        Composite = Composite.resize(
            (int(self.boxSize * scale), int(self.boxSize * scale)), Image.NEAREST)

        pixmap = QtGui.QPixmap.fromImage(ImageQt(Composite))
        self.setPixmap(pixmap)

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit(ev)
        elif ev.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(ev)
        elif ev.button() == QtCore.Qt.MiddleButton:
            self.middleClicked.emit(ev)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()

    def mouseMoveEvent(self, ev):
        self.mouseMoved.emit(ev)

    def mouseReleaseEvent(self, ev):
        self.mouseReleased.emit(ev)

    ##def wheelEvent(self, ev):
    #    self.emit(SIGNAL('scroll(int)'), ev.delta())
