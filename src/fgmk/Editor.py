#!/usr/bin/env python3
# display a tiled image from tileset with PyQt
import os
import tarfile
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import TileXtra, actionDialog, TXWdgt, gwserver, fifl, TileCharaset, Charas, actionsWdgt, gameInit, paletteWdgt, ToolsWdgt, EventsWdgt, LayerWdgt, proj
from fgmk.flowlayout import FlowLayout as FlowLayout


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

COLISIONLAYER = 3
EVENTSLAYER = 4

firstClickX = None
firstClickY = None


class MapWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.Grid = QtWidgets.QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.parent = parent

        self.TileWidth = 0
        self.TileHeight = 0
        self.myScale = 2
        self.currentTile = 5
        self.currentLayer = 0

        self.currentEvent = 1
        self.currentColision = 1

        self.TileList = []

        self.DrawMap(parent)

    def Rescale(self, scale=None):
        if(scale != None):
            self.myScale = scale

        for iy in range(self.TileHeight):
            for jx in range(self.TileWidth):
                self.TileList[iy][jx].Rescale(
                    self.parent.myTileSet.tileset, self.myScale)

        self.resize(self.TileWidth * self.parent.myTileSet.boxsize * self.myScale,
                    self.TileHeight * self.parent.myTileSet.boxsize * self.myScale)

        self.parent.myCharasPalWidget.reinit()

    def DrawMap(self, parent):
        # self.setUpdatesEnabled(False)
        self.setVisible(False)
        LayersMapTiles = parent.myMap.LayersMapTiles

        self.TileHeight = len(LayersMapTiles[0])
        self.TileWidth = len(LayersMapTiles[0][0])

        if len(self.TileList) > 1:
            for collum in self.TileList:
                for wdgt in collum:
                    wdgt.deleteLater()
                    wdgt = None
            self.TileList = []

        # get the background numbers and use to get the tiles
        for iy in range(self.TileHeight):
            self.TileList.append([])
            for jx in range(self.TileWidth):

                self.TileList[iy].append(TileXtra.ExtendedQLabel(self))
                self.Grid.addWidget(self.TileList[iy][jx], iy, jx)
                self.TileList[iy][jx].initTile(
                    parent.myTileSet.tileset, jx, iy, parent.myTileSet.boxsize, LayersMapTiles[:, iy, jx], self.myScale)
                self.TileList[iy][jx].clicked.connect(self.TileInMapClicked)
                self.TileList[iy][jx].rightClicked.connect(
                    self.TileInMapRightClicked)

        self.resize(self.TileWidth * parent.myTileSet.boxsize * self.myScale,
                    self.TileHeight * parent.myTileSet.boxsize * self.myScale)
        # self.setUpdatesEnabled(True)
        self.setVisible(True)
        # self.show()

    def TileInMapRightClicked(self):
        self.ClickedATileinMap(ToolsWdgt.rightClickTool)

    def TileInMapClicked(self):
        self.ClickedATileinMap(ToolsWdgt.leftClickTool)

    def ClickedATileinMap(self, theClickedTool):
        global firstClickX
        global firstClickY

        if theClickedTool == 0:
            # pen
            if(self.currentLayer == COLISIONLAYER):
                self.changeTileType(self.currentColision)
            elif(self.currentLayer == EVENTSLAYER):
                self.changeTileType(self.currentEvent)
                self.parent.myEventsWidget.updateEventsList()
            else:
                self.changeTileType(self.currentTile)

        elif theClickedTool == 1:
            # dropper
            if(self.currentLayer == COLISIONLAYER):
                self.parent.changeColisionCurrent(
                    self.sender().tileType[COLISIONLAYER])
            elif(self.currentLayer == EVENTSLAYER):
                self.parent.changeEventCurrent(
                    self.sender().tileType[EVENTSLAYER])
                self.parent.myEventsWidget.updateEventsList()
            else:
                self.parent.changeTileCurrent(
                    self.sender().tileType[self.currentLayer])

        elif theClickedTool == 2:
            # bucket
            if(self.currentLayer == COLISIONLAYER):
                self.toolBucketFill(self.currentColision)
            elif(self.currentLayer == EVENTSLAYER):
                self.toolBucketFill(self.currentEvent)
                self.parent.myEventsWidget.updateEventsList()
            else:
                self.toolBucketFill(self.currentTile)

        if theClickedTool == 3:
            # line
            if firstClickX is None:
                firstClickX = self.sender().tileX
                firstClickY = self.sender().tileY
            else:
                if(self.currentLayer == COLISIONLAYER):
                    self.toolLine(self.currentColision,
                                  firstClickX, firstClickY)
                elif(self.currentLayer == EVENTSLAYER):
                    self.toolLine(self.currentEvent, firstClickX, firstClickY)
                    self.parent.myEventsWidget.updateEventsList()
                else:
                    self.toolLine(self.currentTile, firstClickX, firstClickY)
                firstClickX = None
                firstClickY = None
        elif theClickedTool == 4:
            # rectangle
            if firstClickX is None:
                firstClickX = self.sender().tileX
                firstClickY = self.sender().tileY
            else:
                if(self.currentLayer == COLISIONLAYER):
                    self.toolRect(self.currentColision,
                                  firstClickX, firstClickY)
                elif(self.currentLayer == EVENTSLAYER):
                    self.toolRect(self.currentEvent, firstClickX, firstClickY)
                    self.parent.myEventsWidget.updateEventsList()
                else:
                    self.toolRect(self.currentTile, firstClickX, firstClickY)
                firstClickX = None
                firstClickY = None

        elif theClickedTool == 5:
            # charaplacer
            charaX = self.sender().tileX
            charaY = self.sender().tileY
            self.parent.myCharasPalWidget.addCharaAction((charaX, charaY))

        else:
            firstClickX = None
            firstClickY = None

    def changeTileType(self, changeTypeTo):
        command = TXWdgt.CommandCTTileType(self.parent, self.sender(
        ), self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, "change tile")
        self.parent.undoStack.push(command)

    def toolBucketFill(self, changeTypeTo):
        listToChange = TileXtra.tileFill(self.sender().tileX, self.sender(
        ).tileY, self.parent.myMap.LayersMapTiles[self.currentLayer], changeTypeTo)
        command = TXWdgt.CommandCGroupTType(self.parent, self.sender(
        ), self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, listToChange, "bucket fill")
        self.parent.undoStack.push(command)

    def toolLine(self, changeTypeTo, firstX, firstY):
        listToChange = TileXtra.tileLine(firstX, firstY, self.sender().tileX, self.sender(
        ).tileY, self.parent.myMap.LayersMapTiles[self.currentLayer], changeTypeTo)
        command = TXWdgt.CommandCGroupTType(self.parent, self.sender(
        ), self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, listToChange, "line")
        self.parent.undoStack.push(command)

    def toolRect(self, changeTypeTo, firstX, firstY):
        listToChange = TileXtra.tileRect(firstX, firstY, self.sender().tileX, self.sender(
        ).tileY, self.parent.myMap.LayersMapTiles[self.currentLayer], changeTypeTo)
        command = TXWdgt.CommandCGroupTType(self.parent, self.sender(
        ), self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, listToChange, "rectangle")
        self.parent.undoStack.push(command)


class CharasPalWidget(QtWidgets.QWidget):
    def __init__(self, mapWdgt, pMap, parent=None, charaInstance=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.mapWdgt = mapWdgt
        self.pMap = pMap
        self.parent = parent

        self.vbox = QtWidgets.QVBoxLayout(self)

        self.charaslist = []
        self.myCharaSelector = Charas.CharaSelector(self, proj.settings)
        self.vbox.addWidget(self.myCharaSelector)
        self.show()

    def reinit(self):
        for charaplaced in self.charaslist:
            charaplaced[2].stop()
            self.mapWdgt.Grid.removeWidget(charaplaced[2])
            charaplaced[2].deleteLater()

        self.myCharaSelector.update()
        self.charaslist = []

        charalist = self.pMap.getCharaList()
        if(charalist == [''] or not charalist):
            return

        for char in charalist:
            self.addCharaAction((char[1], char[2]), char[0], False)

    def addCharaAction(self, position=(0, 0), chara=None, onmap=True):
        if (chara == None):
            chara = self.myCharaSelector.getSelected()

        if (chara != None):
            scale = self.mapWdgt.myScale / 2.0
            if(self.positionEmpty(position)):
                item = Charas.MiniCharaTile(
                    None, proj.settings, chara, (0, 0), scale)
                item.rightClicked.connect(self.autodelete)
                self.mapWdgt.Grid.addWidget(item, position[1], position[0])
                if(onmap):
                    self.pMap.insertChara(position[0], position[1], chara)
                self.charaslist.append((chara, position, item))

    def autodelete(self):
        item = self.sender()
        for charaplaced in self.charaslist:
            if(charaplaced[2] == item):
                charaplaced[2].stop()
                self.pMap.removeChara(charaplaced[1][0], charaplaced[1][1])
                self.mapWdgt.Grid.removeWidget(charaplaced[2])
                charaplaced[2].deleteLater()
                break

        self.charaslist.remove(charaplaced)

    def getCharasList(self):
        charaslist = []
        for charaplaced in self.charaslist:
            charaslist.append(charaplaced[0], charaplaced[
                              1][0], charaplaced[1][1])

        return charaslist

    def deletePosition(self, position=(0, 0)):
        for charaplaced in self.charaslist:
            if(charaplaced[1] == position):
                charaplaced[2].stop()
                self.mapWdgt.Grid.removeWidget(charaplaced[2])
                charaplaced[2].deleteLater()
                break

        self.charaslist.remove(charaplaced)

    def positionEmpty(self, position):
        for charaplaced in self.charaslist:
            if(charaplaced[1] == position):
                return False

        else:
            return True

    def getSelected(self):
        return self.myCharaSelector.getSelected()


class ExitFSWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.parent = parent
        self.VBox = QtWidgets.QVBoxLayout(self)
        self.ButtonExitFS = QtWidgets.QPushButton("exit\nfullscreen")
        self.ButtonExitFS.clicked.connect(self.ExitFS)
        self.VBox.addWidget(self.ButtonExitFS)
        self.setMaximumHeight(60)
        # self.setMinimumHeight(60)
        self.setMaximumWidth(90)
        # self.setMinimumWidth(84)

    def ExitFS(self):
        self.parent.fullscreenViewAction.toggle()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, filelist, **kwargs):
        super().__init__(None, **kwargs)

        self.resize(1024, 768)

        self.undoStack = QtWidgets.QUndoStack(self)

        self.levelName = "newFile"
        proj.settings["workingFile"] = self.levelName + ".json"

        self.myMap = TileXtra.MapFormat()

        self.myMap.new(self.levelName, 10, 10)

        self.scrollArea = QtWidgets.QScrollArea(self)

        # get tileset file and split it in images that can be pointed through
        # array
        self.myTileSet = TileXtra.TileSet(
            self.myMap.tileImage, self.myMap.palette)
        self.myMapWidget = MapWidget(self)

        self.scrollArea.setWidget(self.myMapWidget)

        self.setCentralWidget(self.scrollArea)

        self.FancyWindow(self)

        self.opemFileIfDropped(filelist)

        self.setAcceptDrops(True)


    def changeLayerCurrent(self, changeTo):
        self.myMapWidget.currentLayer = changeTo
        self.myLayerWidget.changeLayerView(changeTo)

    def changeEventCurrent(self, changeTo):
        self.myMapWidget.currentEvent = changeTo
        self.myEventsWidget.eventSelectSpinbox.setValue(changeTo)
        self.changeLayerCurrent(EVENTSLAYER)

    def changeColisionCurrent(self, changeTo):
        self.myMapWidget.currentColision = changeTo
        self.myEventsWidget.setColisionValueView(changeTo)

    def changeTileCurrent(self, changeTo):
        self.myMapWidget.currentTile = changeTo
        self.myPaletteWidget.setImageCurrent(changeTo)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            self.opemFileIfDropped(event.mimeData().urls()[0].toLocalFile())

        else:
            event.ignore()

    def opemFileIfDropped(self, filelist):
        if (isinstance(filelist, str)):
            if (".map.json" in filelist):
                self.openFileByName(filelist)

        else:
            matching = [s for s in filelist if ".map.json" in s]
            if len(matching) > 0:
                self.openFileByName(matching[0])

    def selectStartPosition(self):
        result = gameInit.selectStartingPosition(self, proj.settings)

        doSave = False
        if(result[1] != "this"):
            doSave = True
        else:
            if result[0]["World"]["initLevel"] not in result[0]["LevelsList"]:
                msg_msgbox = "The current level is not listed in LevelsList.\nMaybe you didn't save it or added to the list yet.\nProceed anyway?"
                reply = QtWidgets.QMessageBox.question(self, 'Message',
                                                       msg_msgbox, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    doSave = True
            else:
                doSave = True

        if(doSave):
            TXWdgt.saveInitFile(proj.settings["gamefolder"], result[0])

    def FancyWindow(self, parent=None):
        self.menubar = QtWidgets.QMenuBar(self)
        fileMenu = self.menubar.addMenu('&File')
        editMenu = self.menubar.addMenu('&Edit')
        projectMenu = self.menubar.addMenu('&Project')
        fileMenu.addAction('&New', self.newFile, "Ctrl+N")
        fileMenu.addAction('&Open...', self.openFile, "Ctrl+O")
        fileMenu.addAction('&Save', self.saveFile, "Ctrl+S")
        fileMenu.addAction('&Save As...', self.saveFileAs, "Shift+Ctrl+S")
        fileMenu.addAction('&Export to JS...',
                           self.exportToJsAs, "Shift+Ctrl+E")
        fileMenu.addAction('&Exit', self.close, "Ctrl+Q")

        undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        undoAction.setShortcuts(QtGui.QKeySequence.Undo)
        editMenu.addAction(undoAction)
        redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        redoAction.setShortcuts(QtGui.QKeySequence.Redo)
        editMenu.addAction(redoAction)

        projectMenu.addAction('New &Project', self.newProject, '')
        projectMenu.addAction('Set starting &position...',
                              self.selectStartPosition, '')
        projectMenu.addAction('Edit &charasets...', self.editCharasets, '')
        projectMenu.addAction('Edit &charas...', self.editCharas, '')
        projectMenu.addAction('Run Project', self.runServer, 'f5')

        self.viewMenu = self.menubar.addMenu('&View')

        self.myPaletteWidget = paletteWdgt.PaletteWidget(self, self.myTileSet)
        self.paletteDockWdgt = QtWidgets.QDockWidget("Palette", self)
        self.paletteDockWdgt.setWidget(self.myPaletteWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.paletteDockWdgt)

        self.viewMenu.addAction(self.paletteDockWdgt.toggleViewAction())

        self.myCharasPalWidget = CharasPalWidget(
            self.myMapWidget, self.myMap, self)
        self.charasDockWdgt = QtWidgets.QDockWidget("Charas", self)
        self.charasDockWdgt.setWidget(self.myCharasPalWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.charasDockWdgt)
        self.tabifyDockWidget(self.charasDockWdgt, self.paletteDockWdgt)

        self.viewMenu.addAction(self.charasDockWdgt.toggleViewAction())

        self.myLayerWidget = LayerWdgt.LayerWidget(self)
        self.layerDockWdgt = QtWidgets.QDockWidget("Layers", self)
        self.layerDockWdgt.setWidget(self.myLayerWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.layerDockWdgt)

        self.viewMenu.addAction(self.layerDockWdgt.toggleViewAction())

        self.myToolsWidget = ToolsWdgt.ToolsWidget(self)
        self.toolsDockWdgt = QtWidgets.QDockWidget("Tool", self)
        self.toolsDockWdgt.setWidget(self.myToolsWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.toolsDockWdgt)

        self.viewMenu.addAction(self.toolsDockWdgt.toggleViewAction())

        self.myEventsWidget = EventsWdgt.EventsWidget(self.myMap, self)
        self.eventsDockWdgt = QtWidgets.QDockWidget("Events", self)
        self.eventsDockWdgt.setWidget(self.myEventsWidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.eventsDockWdgt)

        self.viewMenu.addAction(self.eventsDockWdgt.toggleViewAction())

        self.viewMenu.addSeparator()

        self.zoom05xViewAction = QtWidgets.QAction(
            'Zoom 0.5x', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.zoom05xViewAction)
        self.zoom05xViewAction.triggered.connect(self.changeZoom05x)

        self.zoom1xViewAction = QtWidgets.QAction(
            'Zoom 1x', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.zoom1xViewAction)
        self.zoom1xViewAction.triggered.connect(self.changeZoom1x)

        self.zoom2xViewAction = QtWidgets.QAction(
            'Zoom 2x', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.zoom2xViewAction)
        self.zoom2xViewAction.setShortcut(
            QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_0))
        self.zoom2xViewAction.triggered.connect(self.changeZoom2x)

        self.zoom4xViewAction = QtWidgets.QAction(
            'Zoom 4x', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.zoom4xViewAction)
        self.zoom4xViewAction.triggered.connect(self.changeZoom4x)

        self.zoomInAction = QtWidgets.QAction(
            'Zoom In', self.viewMenu, checkable=False)
        self.zoomInAction.setShortcut(QtGui.QKeySequence.ZoomIn)
        self.viewMenu.addAction(self.zoomInAction)
        self.zoomInAction.triggered.connect(self.zoomIn)

        self.zoomOutAction = QtWidgets.QAction(
            'Zoom Out', self.viewMenu, checkable=False)
        self.zoomOutAction.setShortcut(QtGui.QKeySequence.ZoomOut)
        self.viewMenu.addAction(self.zoomOutAction)
        self.zoomOutAction.triggered.connect(self.zoomOut)

        self.viewMenu.addSeparator()

        self.gridViewAction = QtWidgets.QAction(
            'grid', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.gridViewAction)
        self.gridViewAction.changed.connect(self.changeGridMargin)

        self.myExitFSWidget = ExitFSWidget(self)
        self.exitFSDockWdgt = QtWidgets.QDockWidget("", self)
        self.exitFSDockWdgt.setWidget(self.myExitFSWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.exitFSDockWdgt)
        self.exitFSDockWdgt.hide()

        self.fullscreenViewAction = QtWidgets.QAction(
            'Fullscreen', self.viewMenu, checkable=True)
        self.fullscreenViewAction.setShortcut('f11')
        self.viewMenu.addAction(self.fullscreenViewAction)
        self.fullscreenViewAction.changed.connect(self.changeToFullscreen)

        helpMenu = self.menubar.addMenu('&Help')
        helpMenu.addAction('About...', self.helpAbout)

        self.setMenuBar(self.menubar)

        self.changeZoomValue(2)

    def changeZoomValue(self, zoomvalue):
        if(zoomvalue == 0.5):
            self.zoom05xViewAction.setChecked(True)
            self.zoom1xViewAction.setChecked(False)
            self.zoom2xViewAction.setChecked(False)
            self.zoom4xViewAction.setChecked(False)
        if(zoomvalue == 1):
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(True)
            self.zoom2xViewAction.setChecked(False)
            self.zoom4xViewAction.setChecked(False)
        if(zoomvalue == 2):
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(False)
            self.zoom2xViewAction.setChecked(True)
            self.zoom4xViewAction.setChecked(False)
        if(zoomvalue == 4):
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(False)
            self.zoom2xViewAction.setChecked(False)
            self.zoom4xViewAction.setChecked(True)
        self.myMapWidget.Rescale(zoomvalue)

    def zoomIn(self):
        if(self.myMapWidget.myScale == 2):
            self.myMapWidget.Rescale(4)
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(False)
            self.zoom2xViewAction.setChecked(False)
            self.zoom4xViewAction.setChecked(True)
        elif(self.myMapWidget.myScale == 1):
            self.myMapWidget.Rescale(2)
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(False)
            self.zoom2xViewAction.setChecked(True)
            self.zoom4xViewAction.setChecked(False)
        elif(self.myMapWidget.myScale == 0.5):
            self.myMapWidget.Rescale(1)
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(True)
            self.zoom2xViewAction.setChecked(False)
            self.zoom4xViewAction.setChecked(False)

    def zoomOut(self):
        if(self.myMapWidget.myScale == 1):
            self.myMapWidget.Rescale(0.5)
            self.zoom05xViewAction.setChecked(True)
            self.zoom1xViewAction.setChecked(False)
            self.zoom2xViewAction.setChecked(False)
            self.zoom4xViewAction.setChecked(False)
        elif(self.myMapWidget.myScale == 2):
            self.myMapWidget.Rescale(1)
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(True)
            self.zoom2xViewAction.setChecked(False)
            self.zoom4xViewAction.setChecked(False)
        elif(self.myMapWidget.myScale == 4):
            self.myMapWidget.Rescale(2)
            self.zoom05xViewAction.setChecked(False)
            self.zoom1xViewAction.setChecked(False)
            self.zoom2xViewAction.setChecked(True)
            self.zoom4xViewAction.setChecked(False)

    def changeZoom05x(self, checked):
        self.changeZoomValue(0.5)

    def changeZoom1x(self, checked):
        self.changeZoomValue(1)

    def changeZoom2x(self, checked):
        self.changeZoomValue(2)

    def changeZoom4x(self, checked):
        self.changeZoomValue(4)

    def editCharasets(self):

        myCharasetEditor = TileCharaset.CharasetEditorWidget(
            self, proj.settings)
        if myCharasetEditor.exec_() == QtWidgets.QDialog.Accepted:
            print(myCharasetEditor)

    def editCharas(self):

        myCharasEditor = Charas.CharaEditor(self, proj.settings)
        if myCharasEditor.exec_() == QtWidgets.QDialog.Accepted:
            print(myCharasEditor)

    def changeToFullscreen(self):
        if self.fullscreenViewAction.isChecked():
            self.showFullScreen()
            self.exitFSDockWdgt.show()
        else:
            self.showNormal()
            self.exitFSDockWdgt.hide()

    def changeGridMargin(self):
        bxsz = self.myTileSet.boxsize
        if self.gridViewAction.isChecked() is True:
            self.myMapWidget.Grid.setHorizontalSpacing(1)
            self.myMapWidget.Grid.setVerticalSpacing(1)
            self.myMapWidget.resize(self.myMapWidget.TileWidth * (bxsz * self.myMapWidget.myScale + 1) - 1,
                                    self.myMapWidget.TileHeight * (bxsz * self.myMapWidget.myScale + 1) - 1)
        else:
            self.myMapWidget.Grid.setHorizontalSpacing(0)
            self.myMapWidget.Grid.setVerticalSpacing(0)
            self.myMapWidget.resize(self.myMapWidget.TileWidth * bxsz * self.myMapWidget.myScale,
                                    self.myMapWidget.TileHeight * bxsz * self.myMapWidget.myScale)
        self.myMapWidget.show()

    def runServer(self):

        gwserver.servePage(os.path.abspath(proj.settings["gamefolder"]))

    def newProject(self):
        myNewProjectDialog = TXWdgt.newProject(self)
        if myNewProjectDialog.exec_() == QtWidgets.QDialog.Accepted:
            returnedNFD = myNewProjectDialog.getValue()
            self.__newProject(returnedNFD)

    def __newProject(self, returnedNFD):
        import shutil

        projectPath = os.path.join(
            str(returnedNFD["baseFolder"]), str(returnedNFD["name"]))
        proj.settings["basefolder"] = str(returnedNFD["baseFolder"])
        proj.settings["gamefolder"] = projectPath
        proj.settings["gamename"] = str(returnedNFD["name"])
        os.mkdir(projectPath)
        tar = tarfile.open("basegame.tar.gz")
        tar.extractall(projectPath)
        tar.close()

        self.undoStack.clear()

    def newFile(self):
        myNewFileDialog = TXWdgt.newFile(self)
        if myNewFileDialog.exec_() == QtWidgets.QDialog.Accepted:
            returnedNFD = myNewFileDialog.getValue()
            self.__newFile(returnedNFD)

    def __newFile(self, returnedNFD):
        proj.settings["gamefolder"] = str(returnedNFD["gameFolder"])
        self.levelName = str(returnedNFD["name"])
        proj.settings["workingFile"] = os.path.join(
            proj.settings["gamefolder"], self.levelName + ".json")
        self.setWindowTitle(proj.settings["workingFile"])
        self.myMap.new(self.levelName, returnedNFD[
                       "width"], returnedNFD["height"])
        self.myTileSet = TileXtra.TileSet(os.path.join(
            proj.settings["gamefolder"], self.myMap.tileImage), self.myMap.palette)
        self.myMapWidget.DrawMap(self)
        self.gridViewAction.setChecked(False)  # gambiarra
        self.myPaletteWidget.drawPalette(self.myTileSet)
        self.myEventsWidget.updateEventsList()
        self.myCharasPalWidget.reinit()
        self.undoStack.clear()

    def saveFile(self):
        filename = proj.settings["workingFile"]
        if filename != "":
            self.myMap.save(filename)

    def saveFileAs(self):
        filename, extension = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', os.path.expanduser("~"), 'JSON Game Level (*.map.json)')

        if filename[0] != "":
            if filename[-9:] != '.map.json':
                filename += '.map.json'

            proj.settings["workingFile"] = filename
            self.myMap.save(proj.settings["workingFile"])

    def exportToJsAs(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', os.path.expanduser("~"), 'JS Game Level (*.js)')

        if filename[0] != "":
            if filename[-3:] != '.js':
                filename += '.js'

            proj.settings["workingFile"] = filename
            self.myMap.exportJS(proj.settings["workingFile"])

    def openFileByName(self, filename):
        if os.path.isfile(filename):
            proj.settings["gamefolder"] = os.path.abspath(
                os.path.join(os.path.dirname(str(filename)), "../../"))
            proj.settings["workingFile"] = filename
            self.setWindowTitle(proj.settings["workingFile"])
            self.myMap.load(proj.settings["workingFile"])
            self.myTileSet = TileXtra.TileSet(os.path.join(
                proj.settings["gamefolder"], self.myMap.tileImage), self.myMap.palette)
            self.myMapWidget.DrawMap(self)
            self.gridViewAction.setChecked(False)  # gambiarra
            self.undoStack.clear()
            self.myPaletteWidget.drawPalette(self.myTileSet)
            self.myEventsWidget.updateEventsList()
            self.myCharasPalWidget.reinit()

    def openFile(self):
        if(proj.settings["gamefolder"] == ""):
            proj.settings["gamefolder"] = os.path.expanduser("~")
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open File', proj.settings["gamefolder"], "JSON Level (*.map.json);;All Files (*)")[0]
        self.openFileByName(filename)

    def helpAbout(self):
        credits = "Made by Erico\nWith help from the internet.\nHigly based in Tsubasa's Redo, and inspired in Enterbrain's RPG Maker 2000.\nThanks Nintendo for making the SNES."
        QtWidgets.QMessageBox.about(self, "About...", credits)

    def closeEvent(self, event):
        quit_msg = "Do you want to save changes?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               quit_msg, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.saveFile()
        elif reply == QtWidgets.QMessageBox.No:
            event.accept()
        else:
            event.ignore()


def Icon():
    return QtGui.QPixmap('icon.png')
