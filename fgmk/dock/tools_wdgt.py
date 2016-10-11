# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_tile, getdata, tile_set
from fgmk.flowlayout import FlowLayout as FlowLayout

leftClickTool = 0
rightClickTool = 1

tools={ "pen": 0,
        "dropper": 1,
        "bucket": 2,
        "line":3,
        "rectangle":4,
        "charaplacer":5,
        "pan":6}

class ToolsWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.scale = 2

        self.toolTileset = tile_set.TileSet(getdata.path('tools.png'))

        self.FBox = FlowLayout(self)

        TOOLSTARTINGTILE = 6
        ToolsName = ["pen", "dropper", "bucket",
                     "line", "rectangle", "charaplacer","pan"]
        ToolsHelp = ["click to change tile to selected tile",
                     "click to get tile type and set to selected tile",
                     "click to fill area with selected tile",
                     "click once to set starting point and again to set ending point",
                     "click once to set first corner and again to set opposing corner",
                     "places a chara on a selected spot",
                     "click and hold to pan the map"]
        self.MaxTools = len(ToolsName)
        self.ToolTile = []

        self.lastLeftClickTool = 0
        self.lastLeftClickTool = 1

        for i in range(self.MaxTools):
            self.ToolTile.append(base_tile.QTile(self))
            self.ToolTile[-1].initTile(self.toolTileset.tileset, 0, 0, self.toolTileset.boxsize, [
                                       0, 0, TOOLSTARTINGTILE + i, 0, 0], self.scale)
            self.ToolTile[-1].setObjectName(ToolsName[i])
            self.ToolTile[-1].setToolTip(ToolsName[i] +
                                         "\nWhen selected, " + ToolsHelp[i])
            self.ToolTile[-1].clicked.connect(self.toolLeftClicked)
            self.ToolTile[-1].rightClicked.connect(self.toolRightClicked)
            self.FBox.addWidget(self.ToolTile[-1])

        self.updateToolTiles()
        self.show()

    def toolLeftClicked(self, ev):
        global leftClickTool

        if str(self.sender().objectName()) == "pen":
            leftClickTool = 0
        elif str(self.sender().objectName()) == "dropper":
            leftClickTool = 1
        elif str(self.sender().objectName()) == "bucket":
            leftClickTool = 2
        elif str(self.sender().objectName()) == "line":
            leftClickTool = 3
        elif str(self.sender().objectName()) == "rectangle":
            leftClickTool = 4
        elif str(self.sender().objectName()) == "charaplacer":
            leftClickTool = 5
        elif str(self.sender().objectName()) == "pan":
            leftClickTool = 6

        self.updateToolTiles()
        self.show()

    def toolRightClicked(self, ev):
        global rightClickTool

        if str(self.sender().objectName()) == "pen":
            rightClickTool = 0
        elif str(self.sender().objectName()) == "dropper":
            rightClickTool = 1
        elif str(self.sender().objectName()) == "bucket":
            rightClickTool = 2
        elif str(self.sender().objectName()) == "line":
            rightClickTool = 3
        elif str(self.sender().objectName()) == "rectangle":
            rightClickTool = 4
        elif str(self.sender().objectName()) == "charaplacer":
            rightClickTool = 5
        elif str(self.sender().objectName()) == "pan":
            rightClickTool = 6

        self.updateToolTiles()
        self.show()

    def switchLCToolToPan(self):
        global leftClickTool
        self.lastLeftClickTool = leftClickTool
        self.changeLeftClickToolTo(tools['pan'])

    def swithcLCToolBack(self):
        self.changeLeftClickToolTo(self.lastLeftClickTool)

    def changeLeftClickToolTo(self, tooltochange):
        global leftClickTool
        leftClickTool = tooltochange
        self.updateToolTiles()
        self.show()

    def rescale(self,newscale):
        self.scale = newscale
        self.updateToolTiles()

    def updateToolTiles(self):
        global leftClickTool
        global rightClickTool

        LEFTCLICKTILE = 1
        LEFTCLICKLAYER = 1
        RIGHTCLICKTILE = 2
        RIGHTCLICKLAYER = 0

        self.setMinimumWidth(self.scale*32+4)

        for i in range(self.MaxTools):
            if i == leftClickTool:
                self.ToolTile[i].updateTileImageInMap(
                    LEFTCLICKTILE, LEFTCLICKLAYER, self.toolTileset.tileset, self.scale)
            else:
                self.ToolTile[i].updateTileImageInMap(
                    0, LEFTCLICKLAYER, self.toolTileset.tileset, self.scale)
            if i == rightClickTool:
                self.ToolTile[i].updateTileImageInMap(
                    RIGHTCLICKTILE, RIGHTCLICKLAYER, self.toolTileset.tileset, self.scale)
            else:
                self.ToolTile[i].updateTileImageInMap(
                    0, RIGHTCLICKLAYER, self.toolTileset.tileset, self.scale)
