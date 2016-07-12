import os.path
from PyQt5 import QtWidgets, QtCore, QtGui
from fgmk import TileXtra, gameInit, current_project

class MapExplorerWidget(QtWidgets.QWidget):
    mapOpened = QtCore.pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.parent = parent
        self.LvlLWidget = QtWidgets.QListWidget(self)
        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.VBox.addWidget(self.LvlLWidget)
        self.levelList = []
        self.mapForOpen = ''
        self.LvlLWidget.itemClicked.connect(self.doubleClickedForOpen)
        #self.LvlLWidget.itemDoubleClicked.connect(self.doubleClickedForOpen)

        self.show()

    def reloadInitFile(self):
        gamefolder = current_project.settings["gamefolder"]
        self.initFile = gameInit.openInitFile(gamefolder)

        for level in self.levelList:
            self.LvlLWidget.takeItem(0)

        for level in self.initFile['LevelsList']:
            levelFile = self.initFile['LevelsList'][level]
            self.levelList.append(level)
            self.LvlLWidget.insertItem(0,level)

    def doubleClickedForOpen(self, item):
        mapForOpen = self.initFile['LevelsList'][item.text()]
        #only open map if it's not already opened
        if(os.path.basename(current_project.settings["workingFile"])!=mapForOpen):
            self.mapForOpen = mapForOpen
            self.mapOpened.emit()
