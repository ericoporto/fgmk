#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# display a tiled image from tileset with PyQt
import os
import tarfile
import math
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_tile, editor_mainwindow_menus, cmd, game_server, fifl, tile_charaset, persona, game_init, current_project
from fgmk import  getdata, tile_set, configure_project
from fgmk import tools_logic
from fgmk import help
from fgmk import palette_editor, item_editor
from fgmk.dock import events_wdgt, layer_wdgt, map_explorer_wdgt, charas_palette_wdgt, tools_wdgt, tile_palette_wdgt, exit_fullscreen_wdgt
from fgmk.flowlayout import FlowLayout as FlowLayout
from fgmk.util.layer_logic import COLISIONLAYER as COLISIONLAYER
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER
from fgmk.ff import mapfile
from fgmk.util import temp

firstClickX = None
firstClickY = None

"""
This is the MainWindow, the most important module.

it's 'a little' massive right now.
The MapWidget is the main widget you interact in the map editor.
The map editor implements the MainWindow, from the scroollarea, to all dockable,
(from fgmk.dock) and the menus (in editor_mainwindow_menus, item_editor,
palette_editor, persona and tile_charaset)
"""

class MapWidget(QtWidgets.QWidget):
    ctrlWheelPlu = QtCore.pyqtSignal()
    ctrlWheelNeg = QtCore.pyqtSignal()
    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.Grid = QtWidgets.QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)
        self.gridpx=0

        self.parent = parent

        self.TileWidth = 0
        self.TileHeight = 0
        self.myScale = 2
        self.currentTile = 5
        self.currentLayer = 0

        self.currentEvent = 1
        self.currentColision = 1

        self.TileList = []

        self.mousePos = QtCore.QPoint(0,0)

        self.DrawMap(parent)

    # allows resizing the map, used with Zoom feature!
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

    # this is the function to draw and redraw all tiles!
    def DrawMap(self, parent):
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

                self.TileList[iy].append(base_tile.QTile(self))
                self.Grid.addWidget(self.TileList[iy][jx], iy, jx)
                self.TileList[iy][jx].initTile(
                    parent.myTileSet.tileset, jx, iy, parent.myTileSet.boxsize, LayersMapTiles[:, iy, jx], self.myScale)
                self.TileList[iy][jx].clicked.connect(self.TileInMapClicked)
                self.TileList[iy][jx].mouseMoved.connect(self.mouseMoved)
                self.TileList[iy][jx].rightClicked.connect(
                    self.TileInMapRightClicked)

        self.resize(self.TileWidth * parent.myTileSet.boxsize * self.myScale,
                    self.TileHeight * parent.myTileSet.boxsize * self.myScale)
        self.setVisible(True)

    def mouseMoved(self, ev):
        # this is for the pan/move tool to work!
        if((tools_wdgt.rightClickTool == 6 and ev.buttons() == QtCore.Qt.RightButton) or (tools_wdgt.leftClickTool == 6 and ev.buttons() == QtCore.Qt.LeftButton)):
            diff = (ev.pos() - self.mousePos)/1.5
            self.mousePos = ev.pos()
            vscroll = self.parent.scrollArea.verticalScrollBar()
            hscroll = self.parent.scrollArea.horizontalScrollBar()

            vscroll.setValue(vscroll.value()+diff.y())
            hscroll.setValue(hscroll.value()+diff.x())

        # this enables click and hold in the map with the pen tool!
        if((tools_wdgt.rightClickTool == 0 and ev.buttons() == QtCore.Qt.RightButton) or (tools_wdgt.leftClickTool == 0 and ev.buttons() == QtCore.Qt.LeftButton)):
            pos_qpoint = ev.pos()
            pos = (int(math.floor(pos_qpoint.x()/(32.0*self.myScale+self.gridpx))),
                   int(math.floor(pos_qpoint.y()/(32.0*self.myScale+self.gridpx))))
            if(pos != self.prevPenPos):
                self.prevPenPos = pos
                movedTilesXY = int(pos[0]+self.penTileXY[0]),int(pos[1]+self.penTileXY[1])
                if(movedTilesXY[0]<0 or movedTilesXY[0]>self.TileWidth-1 or movedTilesXY[1]<0 or movedTilesXY[1]>self.TileHeight-1):
                    return

                tileToChange = self.TileList[movedTilesXY[1]][movedTilesXY[0]]

                if(self.currentLayer == COLISIONLAYER):
                    self.changeTileType(self.currentColision,tileToChange)
                elif(self.currentLayer == EVENTSLAYER):
                    self.changeTileType(self.currentEvent,tileToChange)
                else:
                    self.changeTileType(self.currentTile,tileToChange)


    def TileInMapRightClicked(self, ev):
        self.ClickedATileinMap(tools_wdgt.rightClickTool, ev)

    def TileInMapClicked(self, ev):
        self.ClickedATileinMap(tools_wdgt.leftClickTool, ev)

    def ClickedATileinMap(self, theClickedTool, ev):
        global firstClickX
        global firstClickY

        if theClickedTool == 0:
            # pen

            # this points are here to allow click and hold with the map editor
            pos_qpoint = ev.pos()
            self.prevPenPos = (int(math.floor(pos_qpoint.x()/(32.0*self.myScale+self.gridpx))),
                               int(math.floor(pos_qpoint.y()/(32.0*self.myScale+self.gridpx))))
            self.penTileXY = self.sender().tileX, self.sender().tileY

            if(self.currentLayer == COLISIONLAYER):
                self.changeTileType(self.currentColision)
            elif(self.currentLayer == EVENTSLAYER):
                self.changeTileType(self.currentEvent)
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
            else:
                self.parent.changeTileCurrent(
                    self.sender().tileType[self.currentLayer])

        elif theClickedTool == 2:
            # bucket
            if(self.currentLayer == COLISIONLAYER):
                self.toolBucketFill(self.currentColision)
            elif(self.currentLayer == EVENTSLAYER):
                self.toolBucketFill(self.currentEvent)
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
                else:
                    self.toolRect(self.currentTile, firstClickX, firstClickY)
                firstClickX = None
                firstClickY = None

        elif theClickedTool == 5:
            # charaplacer
            charaX = self.sender().tileX
            charaY = self.sender().tileY
            command = cmd.CommandAddChara("place chara", self.parent.myCharasPalWidget, (charaX, charaY))
            cmd.commandToStack(command)

        elif theClickedTool == 6:
            # pan
            self.mousePos = ev.pos()

        else:
            firstClickX = None
            firstClickY = None

    def changeTileType(self, changeTypeTo, sender = None):
        if(sender == None):
            sender = self.sender()

        command = cmd.CommandCTTileType(self.parent, sender, self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, "change tile")
        cmd.commandToStack(command)

    def toolBucketFill(self, changeTypeTo):
        listToChange = tools_logic.tileFill(self.sender().tileX, self.sender(
        ).tileY, self.parent.myMap.LayersMapTiles[self.currentLayer], changeTypeTo)
        command = cmd.CommandCGroupTType(self.parent, self.sender(
        ), self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, listToChange, "bucket fill")
        cmd.commandToStack(command)

    def toolLine(self, changeTypeTo, firstX, firstY):
        listToChange = tools_logic.tileLine(firstX, firstY, self.sender().tileX, self.sender(
        ).tileY, self.parent.myMap.LayersMapTiles[self.currentLayer], changeTypeTo)
        command = cmd.CommandCGroupTType(self.parent, self.sender(
        ), self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, listToChange, "line")
        cmd.commandToStack(command)

    def toolRect(self, changeTypeTo, firstX, firstY):
        listToChange = tools_logic.tileRect(firstX, firstY, self.sender().tileX, self.sender(
        ).tileY, self.parent.myMap.LayersMapTiles[self.currentLayer], changeTypeTo)
        command = cmd.CommandCGroupTType(self.parent, self.sender(
        ), self.parent.myMap, self.parent.myTileSet.tileset, self.currentLayer, changeTypeTo, listToChange, "rectangle")
        cmd.commandToStack(command)

    def changeGrid(self,state):
        bxsz = self.parent.myTileSet.boxsize
        if state is True:
            self.gridpx=1
            self.Grid.setHorizontalSpacing(1)
            self.Grid.setVerticalSpacing(1)
            self.resize(self.TileWidth * (bxsz * self.myScale + 1) - 1,
                                    self.TileHeight * (bxsz * self.myScale + 1) - 1)
        else:
            self.gridpx=0
            self.Grid.setHorizontalSpacing(0)
            self.Grid.setVerticalSpacing(0)
            self.resize(self.TileWidth * bxsz * self.myScale,
                                    self.TileHeight * bxsz * self.myScale)
        self.show()

    def wheelEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if (modifiers == QtCore.Qt.ControlModifier):
            delta = event.angleDelta()
            dsum = delta.x()+delta.y()
            if(dsum>0):
                self.ctrlWheelPlu.emit()
            elif(dsum<0):
                self.ctrlWheelNeg.emit()
        else:
            QtWidgets.QWidget.wheelEvent(self,event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, filelist, **kwargs):
        #super().__init__(None, **kwargs)
        QtWidgets.QMainWindow.__init__(self, None, **kwargs)
        #self.resize(1024, 768)

        cmd.initUndoStack(self)
        cmd.getWindowTitleHandler(self)

        self.setWindowIcon(QtGui.QIcon(Icon()))
        self.levelName = "newFile"
        current_project.settings["workingFile"] = self.levelName + ".map.json"

        self.myMap = mapfile.MapFormat(self)

        self.myMap.new(self.levelName, 10, 10)

        self.scrollArea = QtWidgets.QScrollArea(self)

        # get tileset file and split it in images that can be pointed
        self.myTileSet = tile_set.TileSet(
            self.myMap.tileImage, self.myMap.palette)
        self.myMapWidget = MapWidget(self)

        self.scrollArea.setWidget(self.myMapWidget)
        self.setCentralWidget(self.scrollArea)

        self.FancyWindow(self)

        self.setAcceptDrops(True)
        self.myMapWidget.ctrlWheelPlu.connect(self.zoomIn)
        self.myMapWidget.ctrlWheelNeg.connect(self.zoomOut)

        self.settings = QtCore.QSettings("FGMK", "fgmkEditor")
        self.firsttime = self.loadSettings()
        self.opemFileIfDropped(filelist)

    def afterInit(self):
        if self.firsttime:
            help.welcome(self)


    def changeLayerCurrent(self, changeTo):
        self.myMapWidget.currentLayer = changeTo
        self.myLayerWidget.changeLayerView(changeTo)

    def changeEventCurrent(self, changeTo):
        self.myMapWidget.currentEvent = changeTo
        self.myEventsWidget.eventsAndColision.eventSelectSpinbox.setValue(changeTo)
        self.changeLayerCurrent(EVENTSLAYER)

    def changeColisionCurrent(self, changeTo):
        self.myMapWidget.currentColision = changeTo
        self.myEventsWidget.eventsAndColision.setColisionValueView(changeTo)

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
        result = configure_project.selectStartingPosition(self)

        if result is None:
            return

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
            game_init.saveInitFile(current_project.settings["gamefolder"], result[0])

    def FancyWindow(self, parent=None):
        self.menubar = QtWidgets.QMenuBar(self)
        fileMenu = self.menubar.addMenu('&File')
        editMenu = self.menubar.addMenu('&Edit')
        current_projectectMenu = self.menubar.addMenu('&Project')
        fileMenu.addAction('&New Map...', self.newFile, "Ctrl+N")
        fileMenu.addAction('&Open...', self.openFile, "Ctrl+O")
        fileMenu.addAction('&Save', self.saveFile, "Ctrl+S")
        fileMenu.addAction('&Save As...', self.saveFileAs, "Shift+Ctrl+S")
        fileMenu.addAction('&Export to JS...',
                           self.exportToJsAs, "Shift+Ctrl+E")
        fileMenu.addAction('&Exit', self.close, "Ctrl+Q")

        undoAction = cmd.createUndoAction(self)
        undoAction.setShortcuts(QtGui.QKeySequence.Undo)
        editMenu.addAction(undoAction)
        redoAction = cmd.createRedoAction(self)
        redoAction.setShortcuts(QtGui.QKeySequence.Redo)
        editMenu.addAction(redoAction)

        current_projectectMenu.addAction('&New Project...', self.newProject, 'Ctrl+Shift+N')
        current_projectectMenu.addAction('&Open Project...', self.openProject, 'Ctrl+Shift+O')
        current_projectectMenu.addSeparator()
        current_projectectMenu.addAction('Set starting &position...',
                              self.selectStartPosition, '')
        current_projectectMenu.addSeparator()
        current_projectectMenu.addAction('Edit &charasets...', self.editCharasets, '')
        current_projectectMenu.addAction('Edit c&haras...', self.editCharas, '')
        current_projectectMenu.addAction('Edit &palette...', self.editPalette, '')
        current_projectectMenu.addAction('Edit &Items...', self.editItems, '')
        current_projectectMenu.addSeparator()
        current_projectectMenu.addAction('Save and Run Project', self.saveAndRun, 'f5')
        current_projectectMenu.addAction('Run Project', self.runServer, 'Ctrl+f5')
        current_projectectMenu.addAction('Open Project Folder', self.openProjectFolder, '')

        self.viewMenu = self.menubar.addMenu('&View')

        self.myPaletteWidget = tile_palette_wdgt.PaletteWidget(self, self.myTileSet)
        self.paletteDockWdgt = QtWidgets.QDockWidget("Palette", self)
        self.paletteDockWdgt.setObjectName("Palette")
        self.paletteDockWdgt.setWidget(self.myPaletteWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.paletteDockWdgt)

        self.viewMenu.addAction(self.paletteDockWdgt.toggleViewAction())

        self.myCharasPalWidget = charas_palette_wdgt.CharasPalWidget(
            self.myMapWidget, self.myMap, self)
        self.charasDockWdgt = QtWidgets.QDockWidget("Charas", self)
        self.charasDockWdgt.setObjectName("Charas")
        self.charasDockWdgt.setWidget(self.myCharasPalWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.charasDockWdgt)
        self.tabifyDockWidget(self.charasDockWdgt, self.paletteDockWdgt)

        self.viewMenu.addAction(self.charasDockWdgt.toggleViewAction())

        self.myLayerWidget = layer_wdgt.LayerWidget(self)
        self.layerDockWdgt = QtWidgets.QDockWidget("Layers", self)
        self.layerDockWdgt.setObjectName("Layers")
        self.layerDockWdgt.setWidget(self.myLayerWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.layerDockWdgt)

        self.viewMenu.addAction(self.layerDockWdgt.toggleViewAction())

        self.myToolsWidget = tools_wdgt.ToolsWidget(self)
        self.toolsDockWdgt = QtWidgets.QDockWidget("Tool", self)
        self.toolsDockWdgt.setObjectName("Tool")
        self.toolsDockWdgt.setWidget(self.myToolsWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.toolsDockWdgt)

        self.viewMenu.addAction(self.toolsDockWdgt.toggleViewAction())

        self.myEventsWidget = events_wdgt.EventsWidget(self.myMap, self)
        self.eventsDockWdgt = QtWidgets.QDockWidget("Events", self)
        self.eventsDockWdgt.setObjectName("Events")
        self.eventsDockWdgt.setWidget(self.myEventsWidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.eventsDockWdgt)

        self.viewMenu.addAction(self.eventsDockWdgt.toggleViewAction())

        self.myMapExplorerWidget = map_explorer_wdgt.MapExplorerWidget(self)
        self.myMapExplorerWidget.mapOpened.connect(self.openFromExplorer)
        self.mapExplorerDockWdgt = QtWidgets.QDockWidget("Map Explorer", self)
        self.mapExplorerDockWdgt.setObjectName("MapExplorer")
        self.mapExplorerDockWdgt.setWidget(self.myMapExplorerWidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.mapExplorerDockWdgt)

        self.viewMenu.addAction(self.mapExplorerDockWdgt.toggleViewAction())

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
        self.zoomInAction.setShortcuts([QtGui.QKeySequence.ZoomIn,
                                        QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Equal)])
        self.viewMenu.addAction(self.zoomInAction)
        self.zoomInAction.triggered.connect(self.zoomIn)

        self.zoomOutAction = QtWidgets.QAction(
            'Zoom Out', self.viewMenu, checkable=False)
        self.zoomOutAction.setShortcut(QtGui.QKeySequence.ZoomOut)
        self.viewMenu.addAction(self.zoomOutAction)
        self.zoomOutAction.triggered.connect(self.zoomOut)

        self.viewMenu.addSeparator()

        self.toggleVisibilityAll = QtWidgets.QAction(
            'toolbar visibility', self.viewMenu, checkable=True)
        self.toggleVisibilityAll.triggered.connect(self.toggleVisibleDocks)
        self.toggleVisibilityAll.setShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Tab))
        self.visibleDocks = []
        self.toggleVisibilityAll.setChecked(True)

        self.viewMenu.addAction(self.toggleVisibilityAll)

        self.viewMenu.addSeparator()

        self.gridViewAction = QtWidgets.QAction(
            'grid', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.gridViewAction)
        self.gridViewAction.changed.connect(self.changeGridMargin)


        self.myExitFSWidget = exit_fullscreen_wdgt.ExitFSWidget(self)
        self.exitFSDockWdgt = QtWidgets.QDockWidget("", self)
        self.exitFSDockWdgt.setObjectName("ExitFullScreen")
        self.exitFSDockWdgt.setWidget(self.myExitFSWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.exitFSDockWdgt)
        self.exitFSDockWdgt.hide()

        self.fullscreenViewAction = QtWidgets.QAction(
            'Fullscreen', self.viewMenu, checkable=True)
        self.fullscreenViewAction.setShortcut('f11')
        self.viewMenu.addAction(self.fullscreenViewAction)
        self.fullscreenViewAction.changed.connect(self.changeToFullscreen)

        self.viewMenu.addSeparator()

        self.toolScale2x = QtWidgets.QAction(
            'Tools Size 2x', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.toolScale2x)
        self.toolScale2x.triggered.connect(self.changeToolsScale2x)

        self.toolScale1x = QtWidgets.QAction(
            'Tools Size 1x', self.viewMenu, checkable=True)
        self.viewMenu.addAction(self.toolScale1x)
        self.toolScale1x.triggered.connect(self.changeToolsScale1x)

        helpMenu = self.menubar.addMenu('&Help')
        helpMenu.addAction('Help...', self.help)
        helpMenu.addSeparator()
        helpMenu.addAction('Load example...', self.load_example)
        helpMenu.addSeparator()
        helpMenu.addAction('About...', self.about)

        self.setMenuBar(self.menubar)

    def toggleVisibleDocks(self):
        if(self.toggleVisibilityAll.isChecked()):
            #make all visible (as before)
            if(self.visibleDocks[0]): self.paletteDockWdgt.show()
            if(self.visibleDocks[1]): self.charasDockWdgt.show()
            if(self.visibleDocks[2]): self.layerDockWdgt.show()
            if(self.visibleDocks[3]): self.toolsDockWdgt.show()
            if(self.visibleDocks[4]): self.eventsDockWdgt.show()
            if(self.visibleDocks[5]): self.mapExplorerDockWdgt.show()
        else:
            #make all invisible
            self.visibleDocks = [self.paletteDockWdgt.isVisible(),
                self.charasDockWdgt.isVisible(),
                self.layerDockWdgt.isVisible(),
                self.toolsDockWdgt.isVisible(),
                self.eventsDockWdgt.isVisible(),
                self.mapExplorerDockWdgt.isVisible()]
            self.paletteDockWdgt.hide()
            self.charasDockWdgt.hide()
            self.layerDockWdgt.hide()
            self.toolsDockWdgt.hide()
            self.eventsDockWdgt.hide()
            self.mapExplorerDockWdgt.hide()

    def changeToolsScale2x(self):
        self.toolScale2x.setChecked(True)
        self.toolScale1x.setChecked(False)
        self.myToolsWidget.rescale(2)

    def changeToolsScale1x(self):
        self.toolScale2x.setChecked(False)
        self.toolScale1x.setChecked(True)
        self.myToolsWidget.rescale(1)

    def changeZoomValue(self, zoomvalue):
        self.changeZoomViewActionChecked(zoomvalue)
        self.myMapWidget.Rescale(zoomvalue)

    def zoomIn(self):
        if(self.myMapWidget.myScale == 2):
            self.myMapWidget.Rescale(4)
            self.changeZoomViewActionChecked(4)
        elif(self.myMapWidget.myScale == 1):
            self.myMapWidget.Rescale(2)
            self.changeZoomViewActionChecked(2)
        elif(self.myMapWidget.myScale == 0.5):
            self.myMapWidget.Rescale(1)
            self.changeZoomViewActionChecked(1)

    def zoomOut(self):
        if(self.myMapWidget.myScale == 1):
            self.myMapWidget.Rescale(0.5)
            self.changeZoomViewActionChecked(0.5)
        elif(self.myMapWidget.myScale == 2):
            self.myMapWidget.Rescale(1)
            self.changeZoomViewActionChecked(1)
        elif(self.myMapWidget.myScale == 4):
            self.myMapWidget.Rescale(2)
            self.changeZoomViewActionChecked(2)

    def changeZoomViewActionChecked(self, zoomname):
            if(zoomname==0.5):
                self.zoom05xViewAction.setChecked(True)
            else:
                self.zoom05xViewAction.setChecked(False)
            if(zoomname==1):
                self.zoom1xViewAction.setChecked(True)
            else:
                self.zoom1xViewAction.setChecked(False)
            if(zoomname==2):
                self.zoom2xViewAction.setChecked(True)
            else:
                self.zoom2xViewAction.setChecked(False)
            if(zoomname==4):
                self.zoom4xViewAction.setChecked(True)
            else:
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
        myCharasetEditor = tile_charaset.CharasetEditorWidget(
            self, current_project.settings)
        if myCharasetEditor.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def editCharas(self):
        myCharasEditor = persona.CharaEditor(self, current_project.settings)
        if myCharasEditor.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def editPalette(self):
        mappalette = { 'tiles': self.myMap.palette,
                       'tileImage': self.myMap.tileImage,
                       'tilesAnimated': self.myMap.tilesAnimated}
        myPaletteEditor = palette_editor.main(mappalette=mappalette,
                                              parent=self,
                                              ssettings=current_project.settings )
        if myPaletteEditor.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def editItems(self):
        myItemEditor = item_editor.itemsEditorWidget(parent=self)
        if myItemEditor.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def changeToFullscreen(self):
        if self.fullscreenViewAction.isChecked():
            self.showFullScreen()
            self.exitFSDockWdgt.show()
        else:
            self.showNormal()
            self.exitFSDockWdgt.hide()

    def changeGridMargin(self):
        self.myMapWidget.changeGrid(self.gridViewAction.isChecked() is True)

    def openFromExplorer(self):
        testMap = mapfile.MapFormat()
        try:
            testMap.load(current_project.settings["workingFile"])
            testResult = not self.myMap.isEqual(testMap)
        except FileNotFoundError:
            testResult = True
        acceptOpen = False

        if testResult:

            quit_msg = "Do you want to save changes?"
            reply = QtWidgets.QMessageBox.question(self, 'Message',
                                                   quit_msg, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

            if reply == QtWidgets.QMessageBox.Yes:
                acceptOpen=True
                self.saveFile()
            elif reply == QtWidgets.QMessageBox.No:
                acceptOpen=True
            else:
                return
        else:
            acceptOpen = True

        if acceptOpen:
            mapfilename = self.myMapExplorerWidget.mapForOpen
            gamefolder = os.path.abspath(current_project.settings["gamefolder"])
            filetopen = os.path.join(str(gamefolder), fifl.LEVELS, mapfilename)
            self.openFileByName(filetopen)

    def saveAndRun(self):
        self.saveFile()
        self.runServer()

    def openProjectFolder(self):
        foldertoopen = os.path.join(current_project.settings["gamefolder"])
        if(foldertoopen==''):
            foldertoopen = os.path.expanduser("~")

        editor_mainwindow_menus.openFolder(foldertoopen)

    def runServer(self):
        game_server.servePage(os.path.abspath(current_project.settings["gamefolder"]))

    def newProject(self):
        myNewProjectDialog = editor_mainwindow_menus.newProject(self)
        if myNewProjectDialog.exec_() == QtWidgets.QDialog.Accepted:
            returnedNFD = myNewProjectDialog.getValue()
            self.__newProject(returnedNFD)

    def __newProject(self, returnedNFD):
        current_projectectPath = os.path.join(
            str(returnedNFD["baseFolder"]), str(returnedNFD["name"]))
        current_project.settings["basefolder"] = str(returnedNFD["baseFolder"])
        current_project.settings["gamefolder"] = current_projectectPath
        current_project.settings["gamename"] = str(returnedNFD["name"])
        os.mkdir(current_projectectPath)
        tar = tarfile.open(getdata.path("basegame.tar.gz"))
        tar.extractall(current_projectectPath)
        tar.close()
        initfile = game_init.openInitFile(current_project.settings["gamefolder"])
        levellist = initfile["LevelsList"]
        startlevel = initfile['World']['initLevel']
        levelfile = levellist[startlevel]
        self.openFileByName(os.path.join(current_project.settings["gamefolder"],fifl.LEVELS,levelfile))

    def openProject(self):
        if(current_project.settings["gamefolder"] == ""):
            current_project.settings["gamefolder"] = os.path.expanduser("~")

        projectfolder = os.path.join(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Project Directory"))

        if(os.path.isfile(os.path.join(projectfolder,fifl.INITFILE))):
            initfile = game_init.openInitFile(projectfolder)
            levellist = initfile["LevelsList"]
            startlevel = initfile['World']['initLevel']
            levelfile = levellist[startlevel]
            self.openFileByName(os.path.join(projectfolder,fifl.LEVELS,levelfile))


    def newFile(self):
        myNewFileDialog = editor_mainwindow_menus.newFile(self)
        if myNewFileDialog.exec_() == QtWidgets.QDialog.Accepted:
            returnedNFD = myNewFileDialog.getValue()
            self.__newFile(returnedNFD)
            return True

        return False

    def __newFile(self, returnedNFD):
        current_project.settings["gamefolder"] = str(returnedNFD["gameFolder"])
        self.levelName = str(returnedNFD["name"])
        current_project.settings["workingFile"] = os.path.join(
            current_project.settings["gamefolder"], fifl.LEVELS, self.levelName + ".map.json")
        self.setWindowTitle(current_project.settings["workingFile"])
        palette = os.path.join(
            current_project.settings["gamefolder"], fifl.LEVELS,returnedNFD["palette"])
        self.myMap.new(self.levelName, returnedNFD[
                       "width"], returnedNFD["height"], palette)
        self.myTileSet = tile_set.TileSet(os.path.join(
            current_project.settings["gamefolder"], self.myMap.tileImage), self.myMap.palette)
        self.myMapWidget.DrawMap(self)
        self.gridViewAction.setChecked(False)  # gambiarra
        self.myPaletteWidget.drawPalette(self.myTileSet)
        self.myEventsWidget.updateEventsList()
        self.myCharasPalWidget.reinit()
        game_init.regenerateLevelList()
        hasinit = self.myMapExplorerWidget.reloadInitFile()
        self.setEnabledAll(hasinit == True)
        self.changeTileCurrent(0)
        cmd.clearCommandStack()

    def saveFile(self):
        filename = current_project.settings["workingFile"]

        if filename != "":
            self.myMap.save(filename)
            cmd.updateStackAtSave()

            if game_init.regenerateLevelList():
                self.myMapExplorerWidget.reloadInitFile()


    def saveFileAs(self):
        filename, extension = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', os.path.expanduser("~"), 'JSON Game Level (*.map.json)')

        if filename[0] != "":
            if filename[-9:] != '.map.json':
                filename += '.map.json'

            current_project.settings["workingFile"] = filename
            self.myMap.save(current_project.settings["workingFile"])
            cmd.updateStackAtSave()

            if game_init.regenerateLevelList():
                self.myMapExplorerWidget.reloadInitFile()

    def exportToJsAs(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', os.path.expanduser("~"), 'JS Game Level (*.js)')

        if filename[0] != "":
            if filename[-3:] != '.js':
                filename += '.js'

            #current_project.settings["workingFile"] = filename
            self.myMap.exportJS(filename)

    def openFileByName(self, filename):
        if(filename=="newFile.map.json"):
            return

        if os.path.isfile(filename):
            current_project.settings["gamefolder"] = os.path.abspath(
                os.path.join(os.path.dirname(str(filename)), "../../"))
            current_project.settings["workingFile"] = filename
            self.setWindowTitle(current_project.settings["workingFile"])
            self.myMap.load(current_project.settings["workingFile"])
            self.myTileSet = tile_set.TileSet(os.path.join(
                current_project.settings["gamefolder"], self.myMap.tileImage), self.myMap.palette)
            self.myMapWidget.DrawMap(self)
            self.gridViewAction.setChecked(False)  # gambiarra
            self.myPaletteWidget.drawPalette(self.myTileSet)
            self.myEventsWidget.updateEventsList()
            self.myEventsWidget.enableButtonsBecauseEventsList()
            self.myCharasPalWidget.reinit()
            game_init.regenerateLevelList()
            hasinit = self.myMapExplorerWidget.reloadInitFile()
            self.setEnabledAll(hasinit == True)
            cmd.clearCommandStack()
            self.firsttime = False
            self.changeTileCurrent(0)

    def openFile(self):
        if(current_project.settings["gamefolder"] == ""):
            current_project.settings["gamefolder"] = os.path.expanduser("~")
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open File', os.path.join(current_project.settings["gamefolder"], fifl.LEVELS), "JSON Level (*.map.json);;All Files (*)")[0]
        self.openFileByName(filename)


    def closeEvent(self, event):
        if(os.path.isfile(current_project.settings["workingFile"])):
            testMap = mapfile.MapFormat()
            testMap.load(current_project.settings["workingFile"])
            if not self.myMap.isEqual(testMap):

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
                    return

        else:
            event.accept()


        temp.clean()
        self.saveSettings()

    def saveSettings(self):
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size());
        self.settings.setValue("pos", self.pos());
        self.settings.setValue("zoom", self.myMapWidget.myScale)
        self.settings.setValue("toolzoom", self.myToolsWidget.scale)
        self.settings.setValue("state", self.saveState())
        self.settings.setValue("visibledocks", self.visibleDocks)
        self.settings.setValue("tabDockVisibility", self.toggleVisibilityAll.isChecked())
        self.settings.endGroup();

        self.settings.beginGroup("Project")
        if(os.path.isfile(current_project.settings["workingFile"])):
            self.settings.setValue("workingFile", current_project.settings["workingFile"]);
        self.settings.endGroup();

        self.settings.setValue("firsttime", False)


    def loadSettings(self):
        self.settings.beginGroup("MainWindow");
        self.resize(self.settings.value("size", QtCore.QSize(1024, 768)));
        self.move(self.settings.value("pos", QtCore.QPoint(32,32)));
        self.changeZoomValue(float(self.settings.value("zoom", 2)))
        if(float(self.settings.value("toolzoom", 2))==1):
            self.changeToolsScale1x()
        else:
            self.changeToolsScale2x()

        self.visibleDocks = self.settings.value("visibledocks", [True, True, True, True, True, True], type=bool)
        self.toggleVisibilityAll.setChecked(self.settings.value("tabDockVisibility", True, type=bool))
        state = self.settings.value("state", QtCore.QByteArray(), type=QtCore.QByteArray)
        if state:
            self.restoreState(state)
        self.settings.endGroup();

        self.settings.beginGroup("Project")

        workingFile = self.settings.value("workingFile", self.levelName + ".map.json")
        if(os.path.isfile(workingFile)):
            self.openFileByName(workingFile)
        else:
            self.setEnabledAll(False)
        self.settings.endGroup();

        return self.settings.value("firsttime",True, type=bool)

    def help(self):
        myHelp = help.HelpWindow(parent=self)
        if myHelp.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def about(self):
        QtWidgets.QMessageBox.about(self, "About...", help.aboutstr)

    def load_example(self):
        levelfile = help.load_example()
        self.openFileByName(os.path.join(current_project.settings["gamefolder"],fifl.LEVELS,levelfile))

    def setEnabledAll(self, torf):
        self.myPaletteWidget.setEnabled(torf)
        self.myCharasPalWidget.setEnabled(torf)
        self.myLayerWidget.setEnabled(torf)
        self.myToolsWidget.setEnabled(torf)
        self.myEventsWidget.setEnabled(torf)
        self.myMapExplorerWidget.setEnabled(torf)
        self.myMapWidget.setEnabled(torf)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.myToolsWidget.switchLCToolToPan()

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.myToolsWidget.swithcLCToolBack()


def Icon():
    return QtGui.QPixmap(getdata.path('icon.png'))
