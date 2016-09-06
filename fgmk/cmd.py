# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER

class Box:
    pass

__m = Box()  # m will contain all module-level values
__m.undostack = None  # undostack  global in module
__m.setWindowTitle = None
__m.windowTitle = None

def initUndoStack(parent):
    global __m
    if __m.undostack is None:
        __m.undostack = QtWidgets.QUndoStack(parent)
        __m.undostack.cleanChanged.connect(checkAndUpdateTitle)

def createUndoAction(parent):
    global __m
    return __m.undostack.createUndoAction(parent, parent.tr("&Undo"))

def createRedoAction(parent):
    global __m
    return __m.undostack.createRedoAction(parent, parent.tr("&Redo"))

def clearCommandStack():
    global __m
    __m.undostack.clear()
    __m.undostack.setClean()

def updateStackAtSave():
    global __m
    __m.undostack.setClean()

def commandToStack(command):
    global __m
    __m.undostack.push(command)

def getWindowTitleHandler(window):
    global __m
    if __m.setWindowTitle is None:
        __m.setWindowTitle=window.setWindowTitle
        __m.windowTitle=window.windowTitle

def checkAndUpdateTitle():
    wintitle = __m.windowTitle()
    if(__m.undostack.isClean()):
        __m.setWindowTitle(delAsteriskFromStr(wintitle))
    else:
        __m.setWindowTitle(addAsteriskToStr(wintitle))

def addAsteriskToStr(title):
    if(title.endswith('*')):
        return title
    else:
        return title+'*'

def delAsteriskFromStr(title):
    if(title.endswith('*')):
        return title[:-1]
    else:
        return title

class CommandEventAction(QtWidgets.QUndoCommand):
    """
    Class for adding an action to an event.
    This class operates in the event
    widget and the map (that has the jsontree)
    """
    def __init__(self, description, pEventsWidget, event,  current_actions, previous_actions, what):
        #super().__init__(description)
        QtWidgets.QUndoCommand.__init__(self, description)

        self.pEventsWidget = pEventsWidget
        self.current_actions = current_actions
        self.previous_actions = previous_actions
        self.event = event
        self.what = what

    def redo(self):
        self.pEventsWidget.doAction(self.event,
                                    self.current_actions)

    def undo(self):
        self.pEventsWidget.doAction(self.event,
                                    self.previous_actions)

class CommandAddChara(QtWidgets.QUndoCommand):
    """
    Class for a single chara insert operation.
    This class operates in the visible map
    widget and the map (that has the jsontree), having redo (which is also the
    do action) and undo capabilities.
    """
    def __init__(self, description, pCharasPalWidget,  position=(0, 0), chara=None,):
        #super().__init__(description)
        QtWidgets.QUndoCommand.__init__(self, description)

        self.pCharasPalWidget = pCharasPalWidget
        self.position = position
        if (chara == None):
            chara = self.pCharasPalWidget.myCharaSelector.getSelected()
        self.chara = chara

    def redo(self):
        self.pCharasPalWidget.addCharaAction(self.position,self.chara, True)

    def undo(self):
        self.pCharasPalWidget.deletePosition(self.position, True)



class CommandDelChara(QtWidgets.QUndoCommand):
    """
    Class for a single chara delete operation.
    This class operates in the visible map
    widget and the map (that has the jsontree), having redo (which is also the
    do action) and undo capabilities.
    """
    def __init__(self, description, pCharasPalWidget,  position, chara):
        #super().__init__(description)
        QtWidgets.QUndoCommand.__init__(self, description)

        self.pCharasPalWidget = pCharasPalWidget
        self.position = position
        self.chara = chara

    def redo(self):
        self.pCharasPalWidget.deletePosition(self.position, True)

    def undo(self):
        self.pCharasPalWidget.addCharaAction(self.position,self.chara, True)



class CommandCTTileType(QtWidgets.QUndoCommand):
    """
    Class for a single tile operation.
    This class operates in the visible map
    widget and the map (that has the jsontree), having redo (which is also the
    do action) and undo capabilities.
    """
    def __init__(self, parent, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, description):
        #super().__init__(description)
        QtWidgets.QUndoCommand.__init__(self, description)

        self.sender = senderTileWdgt
        self.tileX = self.sender.tileX
        self.tileY = self.sender.tileY
        self.Layer = layer
        self.changeTypeTo = changeTypeTo
        self.oldType = self.sender.tileType[layer]

        self.pmyMapWidget = parent.myMapWidget
        self.pMap = pMap
        self.ptileset = ptileset
        self.myEventsWidget = parent.myEventsWidget

    def redo(self):
        self.pMap.setTile(self.tileX, self.tileY,
                          self.Layer, self.changeTypeTo)
        self.sender.updateTileImageInMap(
            self.changeTypeTo, self.Layer, self.ptileset, self.pmyMapWidget.myScale)

        if(self.Layer == EVENTSLAYER):
            self.myEventsWidget.updateEventsList()

        #print("Type= ", self.changeTypeTo, "  X= " ,self.tileX, "  Y= " , self.tileY)

    def undo(self):
        self.pMap.setTile(self.tileX, self.tileY, self.Layer, self.oldType)
        self.sender.updateTileImageInMap(
            self.oldType, self.Layer, self.ptileset, self.pmyMapWidget.myScale)

        if(self.Layer == EVENTSLAYER):
            self.myEventsWidget.updateEventsList()

        #print("Type= ", self.oldType, "  X= " ,self.tileX, "  Y= " , self.tileY)



class CommandCGroupTType(QtWidgets.QUndoCommand):
    """
    Class for a multiple tile operation.
    This class operates in the visible map
    widget and the map (that has the jsontree), having redo (which is also the
    do action) and undo capabilities.
    """

    def __init__(self, parent, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, listToChange, description):
        #super().__init__(description)
        QtWidgets.QUndoCommand.__init__(self, description)

        self.tileX = senderTileWdgt.tileX
        self.tileY = senderTileWdgt.tileY
        self.Layer = layer
        self.changeTypeTo = changeTypeTo

        self.pmyMapWidget = parent.myMapWidget
        self.pMap = pMap
        self.ptileset = ptileset
        self.myEventsWidget = parent.myEventsWidget

        self.listToChange = listToChange

    def redo(self):
        for change in self.listToChange:
            tile = self.pmyMapWidget.TileList[change[1]][change[0]]
            self.pMap.setTile(change[0], change[1], self.Layer, change[3])
            tile.updateTileImageInMap(
                change[3], self.Layer, self.ptileset, self.pmyMapWidget.myScale)

        if(self.Layer == EVENTSLAYER):
            self.myEventsWidget.updateEventsList()
            #print("Type= ", change[3], "  X= " , change[0], "  Y= " , change[1])

    def undo(self):
        for change in self.listToChange:
            tile = self.pmyMapWidget.TileList[change[1]][change[0]]
            self.pMap.setTile(change[0], change[1], self.Layer, change[2])
            tile.updateTileImageInMap(
                change[2], self.Layer, self.ptileset, self.pmyMapWidget.myScale)

        if(self.Layer == EVENTSLAYER):
            self.myEventsWidget.updateEventsList()
            #print("Type= ", change[2], "  X= " ,change[0], "  Y= " , change[1])
