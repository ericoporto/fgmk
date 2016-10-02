# -*- coding: utf-8 -*-
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import current_project, fifl, tile_set, base_tile, getdata
from fgmk.ff import palette_format

ANIMLAYER=3
IDLAYER=4

"""
The PaletteEditorWidget implements the whole palette editor, and the visual
palette you interact in the screen is implemented in the PaletteCfgWidget.
"""

class PaletteCfgWidget(QtWidgets.QWidget):
    def __init__(self, pal=None, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent
        if(pal==None):
            self.pal = palette_format.PaletteFormat()
        else:
            self.pal = pal

        self.Grid = QtWidgets.QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.currentType = 1
        self.currentAnim = 1

        self.img = None

        self.TileWidth = 0
        self.TileHeight = 0
        self.myScale = 1
        self.TileList = []

    def new(self):
        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.currentType = 1
        self.currentAnim = 1

        self.img = None

        self.TileWidth = 0
        self.TileHeight = 0
        self.myScale = 1

        self.pal.new()
        self.LoadPal()

    def getPalFilename(self):
        return self.pal.getfilename()

    def savePal(self, filename=''):
        self.updatePalFile()
        self.pal.save(filename)

    def LoadJsonDumpPal(self, jsonTree):
        self.pal.loadjsondump(jsonTree)
        self.img = os.path.join(current_project.settings['gamefolder'], self.pal.getimg())
        self.LoadImage()

    def LoadPal(self, pal=None):
        if(pal!=None):
            self.pal.load(pal)

        self.img = os.path.join(current_project.settings['gamefolder'], self.pal.getimg())
        if os.path.isfile(self.img):
            self.LoadImage()
            return

        self.img = os.path.join(os.path.dirname(self.pal.getfilename()), self.pal.getimg())
        if os.path.isfile(self.img):
            self.LoadImage()
            return

    def LoadImage(self,img=None):
        if(img!=None):
            self.img = os.path.join(current_project.settings['gamefolder'], self.pal.imgloag(img))
            self.pal.imgloag(self.img)

        self.t = tile_set.TileSet(os.path.join(current_project.settings['gamefolder'],self.img))
        self.TileWidth = int(self.t.imageFile.size[0]/self.t.boxsize)
        self.TileHeight = int(self.t.imageFile.size[1]/self.t.boxsize)
        self.DrawPal()

    def Rescale(self, scale=None):
        if(scale != None):
            self.myScale = scale

        for iy in range(self.TileHeight):
            for jx in range(self.TileWidth):
                self.TileList[iy][jx].Rescale(
                    self.t.tileset, self.myScale)

        self.resize(self.TileWidth * self.t.boxsize * self.myScale,
                    self.TileHeight * self.t.boxsize * self.myScale)


    def DrawPal(self):
        # self.setUpdatesEnabled(False)
        self.setVisible(False)

        if len(self.TileList) > 1:
            for collum in self.TileList:
                for wdgt in collum:
                    self.Grid.removeWidget(wdgt)
                    wdgt.deleteLater()
                    wdgt.hide()
                    del wdgt
                    wdgt = None
            self.TileList = []

        # get the background numbers and use to get the tiles
        i=0
        for iy in range(self.TileHeight):
            self.TileList.append([])
            for jx in range(self.TileWidth):
                tiletype = self.getTileType(jx,iy)
                tiletype[0]=i
                self.TileList[iy].append(base_tile.QTile(self))
                self.Grid.addWidget(self.TileList[iy][jx], iy, jx)
                if(i!=0):
                    self.TileList[iy][jx].initTile(self.t.tileset, jx, iy,
                                                   self.t.boxsize,
                                                   tiletype,
                                                   self.myScale,
                                                   True)
                    self.TileList[iy][jx].clicked.connect(self.TileClicked)
                    self.TileList[iy][jx].rightClicked.connect(
                        self.TileRightClicked)
                else:
                    self.TileList[iy][jx].initTile(self.t.tileset, jx, iy,
                                                   self.t.boxsize,
                                                   [0,0,0,0,0],
                                                   self.myScale,
                                                   True)
                i+=1

        self.resize(self.TileWidth * self.t.boxsize * self.myScale,
                    self.TileHeight * self.t.boxsize * self.myScale)
        self.setVisible(True)

    def setTile(self, tiletype):
        i = tiletype[0]
        x = int(i % self.TileWidth)
        y = int(i / self.TileWidth)
        tileid = -1
        tileanim = 0
        if(tiletype[IDLAYER]!=0):
            tileid = tiletype[IDLAYER]
            layer=IDLAYER

        if(tiletype[ANIMLAYER]!=0):
            tileanim = tiletype[ANIMLAYER]
            layer=ANIMLAYER

        if(tileid != -1):
            for iy in range(self.TileHeight):
                for jx in range(self.TileWidth):
                    if(self.TileList[iy][jx].tileType[IDLAYER] == int(tileid) and self.TileList[iy][jx].tileType[ANIMLAYER] == 0):
                        self.TileList[iy][jx].updateTileImageInMap(
                                                0,
                                                IDLAYER,
                                                self.t.tileset,
                                                self.myScale)

        if(tileanim != 0):
            for iy in range(self.TileHeight):
                for jx in range(self.TileWidth):
                    if(self.TileList[iy][jx].tileType[3] == int(tileanim) and self.TileList[iy][jx].tileType[4]== tiletype[IDLAYER]):
                        self.TileList[iy][jx].updateTileImageInMap(
                                                0,
                                                ANIMLAYER,
                                                self.t.tileset,
                                                self.myScale)

        self.TileList[y][x].updateTileType(self.t.tileset, tiletype)
        self.updatePalFile()

    def getTileType(self,x,y):
        tile = self.pal.gettile(x,y)
        if int(tile.id) != -1:
            return [0,0,0,tile.anim,int(tile.id)]
        else:
            return [0,0,0,0,0]

    def updatePalFile(self):
        self.pal.delalltiles()
        self.pal.addtile(palette_format.T(0,(0,0),0))
        for iy in range(self.TileHeight):
            for jx in range(self.TileWidth):
                tiletype = self.TileList[iy][jx].tileType
                if(tiletype[IDLAYER]!=0):
                    self.pal.addtile(palette_format.T(tiletype[IDLAYER],(jx,iy),tiletype[ANIMLAYER]))


    def TileClicked(self, ev):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            self.currentType+=1
            if(self.currentType>299):
                self.currentType=0
            self.parent.tileSpinbox.setValue(self.currentType)
        elif modifiers == QtCore.Qt.ControlModifier:
            self.currentType-=1
            if(self.currentType<0):
                self.currentType=0
            self.parent.tileSpinbox.setValue(self.currentType)


        command = CommandSetTileType(self, self.sender(), 'id', self.currentType, "set id")
        self.parent.undostack.push(command)

    def TileRightClicked(self, ev):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            self.currentAnim+=1
            if(self.currentAnim>4):
                self.currentAnim=0
            self.parent.animSpinbox.setValue(self.currentAnim)
        if modifiers == QtCore.Qt.ControlModifier:
            self.currentAnim-=1
            if(self.currentAnim<0):
                self.currentAnim=0
            self.parent.animSpinbox.setValue(self.currentAnim)

        command = CommandSetTileType(self, self.sender(), 'anim', self.currentAnim, "set anim")
        self.parent.undostack.push(command)

    def changeTileIdCurrent(self, num):
        self.currentType = num
    def changeAnimIdCurrent(self, num):
        self.currentAnim = num

    def getMaxTile(self):
        maxtile = 0
        for iy in range(self.TileHeight):
            for jx in range(self.TileWidth):
                tiletype = self.TileList[iy][jx].tileType
                if(tiletype[IDLAYER]>maxtile):
                    maxtile=tiletype[IDLAYER]
        return maxtile

    def getMaxAnim(self):
        maxanim = 1
        for iy in range(self.TileHeight):
            for jx in range(self.TileWidth):
                tiletype = self.TileList[iy][jx].tileType
                if(tiletype[IDLAYER]==self.currentType and tiletype[ANIMLAYER] > maxanim):
                    maxanim=tiletype[ANIMLAYER]
        return maxanim

class CommandSetTileType(QtWidgets.QUndoCommand):
    """
    Class for a single tile operation.
    This class operates in the visible map
    widget and the map (that has the jsontree), having redo (which is also the
    do action) and undo capabilities.
    """
    def __init__(self, pPaletteCfgWidget, senderTileWdgt, id_or_anim,  new_id_or_anim, description):
        #super().__init__(description)
        QtWidgets.QUndoCommand.__init__(self, description)

        self.sender = senderTileWdgt
        self.tileX = self.sender.tileX
        self.tileY = self.sender.tileY
        self.oldTileType = self.sender.tileType[:]
        self.id_or_anim = id_or_anim
        if(self.id_or_anim=='id'):
            newTileType = self.oldTileType[:]
            newTileType[IDLAYER]=new_id_or_anim
            self.newTileType = newTileType
        else:
            newTileType = self.oldTileType[:]
            newTileType[ANIMLAYER]=new_id_or_anim
            self.newTileType = newTileType

        self.pPaletteCfgWidget = pPaletteCfgWidget

    def redo(self):
        self.pPaletteCfgWidget.setTile(self.newTileType)
        #self.sender.updateTileImageInMap(
        #    self.changeTypeTo, self.Layer, self.ptileset, self.pPaletteCfgWidget.myScale)

    def undo(self):
        self.pPaletteCfgWidget.setTile(self.oldTileType)
        #self.sender.updateTileImageInMap(
        #    self.oldType, self.Layer, self.ptileset, self.pPaletteCfgWidget.myScale)



class PaletteEditorWidget(QtWidgets.QDialog):
    def __init__(self,mappalette=None, parent=None, ssettings={}, palettefiles=None, **kwargs):
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        #this will create a undo stack
        self.undostack = QtWidgets.QUndoStack(self)

        #this block creates the outer scroll area
        self.mainVBox = QtWidgets.QVBoxLayout(self)
        self.mainVBox.setAlignment(QtCore.Qt.AlignTop)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        self.mainVBox.addWidget(scrollArea)
        insideScrollArea = QtWidgets.QWidget(scrollArea)
        scrollArea.setWidget(insideScrollArea)
        VBox = QtWidgets.QVBoxLayout(insideScrollArea)
        VBox.setAlignment(QtCore.Qt.AlignTop)
        insideScrollArea.setLayout(VBox)

        #this will create the basic palette editor widget
        self.myPalWidget = PaletteCfgWidget(parent=self)
        self.PalscrollArea = QtWidgets.QScrollArea(self)
        self.PalscrollArea.setWidget(self.myPalWidget)

        #adding a toolbar
        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.addAction("new\npalette",self.myPalWidget.new)
        self.toolbar.addAction("open\npalette",self.openPalette)
        self.toolbar.addAction("save\npalette",self.savePalette)
        self.toolbar.addAction("save\npalette as..",self.savePaletteAs)
        self.toolbar.addAction("open\nimage",self.openImage)
        if(current_project.settings['gamefolder'] == ''):
            self.toolbar.addAction("open\ngame project",self.openProject)

        #this will add id and anim control
        undoaction = self.undostack.createUndoAction(self, self.tr("&Undo"))
        redoaction = self.undostack.createRedoAction(self, self.tr("&Redo"))
        self.toolbar.addAction(undoaction)
        self.toolbar.addAction(redoaction)

        maxpixmap = QtGui.QPixmap(getdata.path('icon_max.png'))
        maxp1pixmap = QtGui.QPixmap(getdata.path('icon_max_p1.png'))
        zeropixmap = QtGui.QPixmap(getdata.path('icon_zero.png'))
        maxicon = QtGui.QIcon(maxpixmap)
        maxp1icon = QtGui.QIcon(maxp1pixmap)
        zeroicon = QtGui.QIcon(zeropixmap)
        labelIdCurrent = QtWidgets.QLabel("Tile Nº")
        self.tileSpinbox = QtWidgets.QSpinBox(self)
        self.tileSpinbox.setToolTip("Tile 0 means not selected.")
        self.tileSpinbox.setMinimum(0)
        self.tileSpinbox.setMaximum(299)
        self.tileSpinbox.setSingleStep(1)
        self.tileSpinbox.valueChanged.connect(self.myPalWidget.changeTileIdCurrent)
        tileMaxP1 = QtWidgets.QPushButton()
        tileMaxP1.setIcon(maxp1icon)
        tileMaxP1.setIconSize(maxp1pixmap.rect().size())
        tileMaxP1.clicked.connect(self.maxTileSpinboxP1)
        tileMaxP1.show()
        tileMax = QtWidgets.QPushButton()
        tileMax.setIcon(maxicon)
        tileMax.setIconSize(maxpixmap.rect().size())
        tileMax.clicked.connect(self.maxTileSpinbox)
        tileMax.show()
        tileZero = QtWidgets.QPushButton()
        tileZero.setIcon(zeroicon)
        tileZero.setIconSize(zeropixmap.rect().size())
        tileZero.clicked.connect(self.zeroTileSpinbox)
        tileZero.show()
        labelAnimCurrent = QtWidgets.QLabel("Tile Animated")
        self.animSpinbox = QtWidgets.QSpinBox(self)
        self.animSpinbox.setToolTip("0 means not animated.")
        self.animSpinbox.setMinimum(0)
        self.animSpinbox.setMaximum(4)
        self.animSpinbox.setSingleStep(1)
        self.animSpinbox.valueChanged.connect(self.myPalWidget.changeAnimIdCurrent)
        animMax = QtWidgets.QPushButton()
        animMax.setIcon(maxicon)
        animMax.setIconSize(maxpixmap.rect().size())
        animMax.clicked.connect(self.maxAnimSpinbox)
        animMax.show()
        animZero = QtWidgets.QPushButton()
        animZero.setIcon(zeroicon)
        animZero.setIconSize(zeropixmap.rect().size())
        animZero.clicked.connect(self.zeroAnimSpinbox)
        animZero.show()
        SpinHBox=QtWidgets.QHBoxLayout()
        SpinHBox.setAlignment(QtCore.Qt.AlignLeft)
        SpinHBox.addWidget(labelIdCurrent)
        SpinHBox.addWidget(self.tileSpinbox)
        SpinHBox.addWidget(tileMaxP1)
        SpinHBox.addWidget(tileMax)
        SpinHBox.addWidget(tileZero)
        SpinHBox.addWidget(labelAnimCurrent)
        SpinHBox.addWidget(self.animSpinbox)
        SpinHBox.addWidget(animMax)
        SpinHBox.addWidget(animZero)

        VBox.addWidget(self.toolbar)
        VBox.addLayout(SpinHBox)
        VBox.addWidget(self.PalscrollArea)

        if(mappalette!=None):
            self.openMapPalette(mappalette)
        elif(palettefiles!=None):
            if os.path.isfile(os.path.join(palettefiles[0])):
                # if path is absolute
                self.myPalWidget.LoadPal(os.path.join(palettefiles[0]))
            elif os.path.isfile(os.path.join(os.getcwd(),palettefiles[0])):
                # if path is relative
                self.myPalWidget.LoadPal(os.path.join(os.getcwd(),palettefiles[0]))

    def openMapPalette(self, mappalette):
        self.myPalWidget.LoadJsonDumpPal(mappalette)

    def maxTileSpinbox(self):
        maxtile = self.myPalWidget.getMaxTile()
        self.myPalWidget.currentType=maxtile
        self.tileSpinbox.setValue(maxtile)

    def maxTileSpinboxP1(self):
        maxtile = self.myPalWidget.getMaxTile()+1
        self.myPalWidget.currentType=maxtile
        self.tileSpinbox.setValue(maxtile)

    def zeroTileSpinbox(self):
        self.myPalWidget.currentType=0
        self.tileSpinbox.setValue(0)

    def maxAnimSpinbox(self):
        maxanim = self.myPalWidget.getMaxAnim()
        self.myPalWidget.currentAnim=maxanim
        self.animSpinbox.setValue(maxanim)

    def zeroAnimSpinbox(self):
        self.myPalWidget.currentAnim=0
        self.animSpinbox.setValue(0)

    def savePalette(self,filename=''):
        if(filename==''):
            filename = self.myPalWidget.getPalFilename()

        if(filename==''):
            self.savePaletteAs()
        else:
            self.myPalWidget.savePal(filename)

    def savePaletteAs(self):
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.LEVELS)

        filename, extension = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', folder_to_open_to, 'JSON Pal Level (*.pal.json)')

        if filename != "":
            if filename[-9:] != '.pal.json':
                filename += '.pal.json'

            self.savePalette(filename)


    def openImage(self):
        folder_to_open_to=""
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.IMG)

        filename = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        folder_to_open_to,
                        "PNG (*.png);;All Files (*)")[0]
        if(filename!=''):
            self.myPalWidget.LoadImage(filename)

    def openPalette(self):
        folder_to_open_to=""
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.LEVELS)

        filename = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        folder_to_open_to,
                        "JSON Palette (*.pal.json);;All Files (*)")[0]
        if(filename!=''):
            self.myPalWidget.LoadPal(filename)

    def openProject(self):
        if(current_project.settings["gamefolder"] == ""):
            current_project.settings["gamefolder"] = os.path.expanduser("~")

        projectfolder = os.path.join(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Project Directory"))
        current_project.settings["gamefolder"] = projectfolder

def main(mappalette=None, parent=None, ssettings={},palettefiles=None):
    return PaletteEditorWidget(mappalette=mappalette,
                               parent=parent,
                               ssettings=ssettings,
                               palettefiles=palettefiles)

if __name__ == "__main__":
    from sys import argv, exit

    a = QtWidgets.QApplication(argv)
    m = main()
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
