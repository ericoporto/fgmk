# -*- coding: utf-8 -*-
import os.path
from os import remove as osremove
from PyQt5 import QtWidgets, QtCore, QtGui
from fgmk import game_init, current_project, tile_set, getdata, base_tile, fifl

class MapExplorerWidget(QtWidgets.QWidget):
    """
    A widget that can list the available levels from the init file, and allow
    navigating them by open and closing them in the Editor.
    """

    mapOpened = QtCore.pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.menuTileset = tile_set.TileSet(getdata.path('map_explorer_icons.png'))
        self.scale = 0.5

        iconGrid = QtWidgets.QGridLayout()

        iconHBoxL = QtWidgets.QHBoxLayout()
        iconHBoxL.setAlignment(QtCore.Qt.AlignLeft)
        iconGrid.addLayout(iconHBoxL, 0,0, QtCore.Qt.AlignLeft)

        iconHBoxR = QtWidgets.QHBoxLayout()
        iconHBoxR.setAlignment(QtCore.Qt.AlignRight)
        iconGrid.addLayout(iconHBoxR, 0,1, QtCore.Qt.AlignRight)

        #the last element will be left at the right corner
        #I want the trash to be always the last element
        iconName = ["new","open","trash"]
        iconHelp = ["creates a new map file",
                    "opens a map file. Same as double clicking.",
                    "deletes a map file."]
        self.menuIcons = []

        for i in range(len(iconName)):
            self.menuIcons.append(base_tile.QTile(self))
            self.menuIcons[-1].initTile(self.menuTileset.tileset, 0, 0,
                                        self.menuTileset.boxsize,
                                        [0, 0, i+1, 0, 0], self.scale)
            self.menuIcons[-1].setObjectName(iconName[i])
            self.menuIcons[-1].setToolTip(iconName[i] + "\nWhen clicked, " + iconHelp[i])
            self.menuIcons[-1].clicked.connect(self.clickedOnIcon)
            if(i<len(iconName)-1):
                iconHBoxL.addWidget(self.menuIcons[-1])
            else:
                iconHBoxR.addWidget(self.menuIcons[-1])


        self.parent = parent
        self.LvlLWidget = QtWidgets.QListWidget(self)
        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.VBox.addLayout(iconGrid)
        self.VBox.addWidget(self.LvlLWidget)
        self.levelList = []
        self.mapForOpen = ''
        self.LvlLWidget.itemDoubleClicked.connect(self.openMapItem)
        #self.LvlLWidget.itemClicked.connect(self.doubleClickedForOpen)

        self.show()

    def clickedOnIcon(self, ev):
        action = str(self.sender().objectName())
        are_items_selected = len(self.LvlLWidget.selectedItems())>0
        if are_items_selected:
            selected_item = self.LvlLWidget.selectedItems()[0]

            if(action == "open"):
                self.openMapItem(selected_item)

            elif(action == "trash"):
                self.deleteMap(selected_item)

        if(action == "new"):
            if self.parent.newFile():
                self.parent.saveFile()


    def deleteMap(self, item):
        mapForDeletion = self.initFile['LevelsList'][item.text()]

        gamefolder = current_project.settings["gamefolder"]

        target_to_delete = os.path.join(gamefolder,fifl.LEVELS,mapForDeletion)

        if(os.path.basename(current_project.settings["workingFile"])!=mapForDeletion):

            reply = QtWidgets.QMessageBox.question(self, 'Delete?',
                                                   'Do you really wish to delete:\n'+mapForDeletion, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                osremove(target_to_delete)
                game_init.regenerateLevelList()
                self.reloadInitFile()

        else:
            QtWidgets.QMessageBox.information(self, 'Delete Problem',
                                                   "Can't delete a map while it's open in the map editor.", QtWidgets.QMessageBox.Ok )

    def reloadInitFile(self):
        gamefolder = current_project.settings["gamefolder"]
        self.initFile = game_init.openInitFile(gamefolder)

        for level in self.levelList:
            self.LvlLWidget.takeItem(0)

        for level in self.initFile['LevelsList']:
            levelFile = self.initFile['LevelsList'][level]
            self.levelList.append(level)
            self.LvlLWidget.insertItem(0,level)

        if(self.initFile != None):
            return True
        else:
            return False

    def openMapItem(self, item):
        mapForOpen = self.initFile['LevelsList'][item.text()]
        #only open map if it's not already opened
        if(os.path.basename(current_project.settings["workingFile"])!=mapForOpen):
            self.mapForOpen = mapForOpen
            self.mapOpened.emit()
