import os
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_model, current_project, fifl, tile_set, base_tile

ANIMLAYER=3
IDLAYER=4

#T(id,(x,y))
class T:
    def __init__(self,id,pos,anim=None):
        self.id=str(id)
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.anim=anim

    def set(self,id,pos,anim=None):
        self.id=str(id)
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.anim=anim

    def setxy(self,x,y):
        self.pos=(x,y)
        self.x=x
        self.y=y

    def setid(self,id):
        self.id=str(id)

    def setanim(anim=None):
        self.anim=anim

class PaletteFormat(base_model.BaseFormat):
    def __init__(self):
        base_model.BaseFormat.__init__(self)
        self.new()

    def new(self):
        self.animtiles = {}
        self.jsonTree = {'tileImage': '',
                         'tiles': {'0':[0,0]},
                         'tilesAnimated': {}}

    def load(self,palfile):
        base_model.BaseFormat.load(self,palfile)
        for tile in self.jsonTree['tilesAnimated']:
            self.animtiles[str(tile)] = {}
            for i in range(len(self.jsonTree['tilesAnimated'][tile])):
                self.animtiles[tile][str(i)]=self.jsonTree['tilesAnimated'][tile][i]


    def imgloag(self,imgfile):
        self.jsonTree['tileImage'] = os.path.join(fifl.IMG,os.path.basename(imgfile))
        return self.jsonTree['tileImage']

    def getimg(self):
        return self.jsonTree['tileImage']

    def settile(self, t):
        #previous = self.gettile(t.x,t.y)
        if(int(t.id)>0):
            if(t.anim==None):
                self.deltilexy(t.x,t.y)
                self.addtile(t)
            else:
                self.deltilexy(t.x,t.y)
                self.addtile(t)
                self.addanimtile(t)

        else:
            self.deltilexy(t.x,t.y)

    def gettile(self, x, y):
        tiles = self.jsonTree['tiles']
        tanims = self.jsonTree['tilesAnimated']

        for ttype in tiles:
            tile = tiles[ttype]
            if(x==tile[0] and y==tile[1]):
                if ttype in tanims:
                    return T(ttype,(x,y), 1)
                else:
                    return T(ttype,(x,y))

        for ttype in tanims:
            animtile = tanims[ttype]
            if(len(animtile)>0):
                for i in range(len(animtile)):
                    tile = animtile[i]
                    if(x==tile[0] and y==tile[1]):
                        return T(ttype,(x,y),i+1)

        return T(-1,(x,y))



    def addanimtile(self,tileT):
        if tileT.id in self.animtiles:
            self.animtiles[tileT.id][tileT.anim] = [tileT.x,tileT.y]
        else:
            self.animtiles[tileT.id]={}
            self.animtiles[tileT.id][tileT.anim] = [tileT.x,tileT.y]

        animdict = self.animtiles[tileT.id]

        animlist = [animdict[k] for k in sorted(animdict)]

        self.jsonTree['tilesAnimated'][tileT.id] = animlist

    def addtile(self,tileT):
        self.jsonTree['tiles'][tileT.id] = [tileT.x,tileT.y]
        return self.jsonTree['tiles'][tileT.id]

    def deltilexy(self,x,y):
        dellist = []
        for tile in self.jsonTree['tiles']:
            if(self.jsonTree['tiles'][tile][0] ==x and self.jsonTree['tiles'][tile][0] ==y):
                dellist.append(tile)
        for tile in dellist:
            self.jsonTree['tiles'].pop(str(tile), None)

        dellist = []
        for tile in self.animtiles:
            for i in self.animtiles[tile]:
                if(self.animtiles[tile][i][0] ==x and self.animtiles[tile][i][0] ==y):
                    dellist.append((tile,i))
        for item in dellist:
            removed = self.animtiles[str(item[0])].pop(item[1], None)
            print(removed)

        tilesAnimated = {}
        for tile in self.animtiles:
            animdict = self.animtiles[tile]
            animlist = [animdict[k] for k in sorted(animdict)]
            tilesAnimated[tile]=animlist

        self.jsonTree['tilesAnimated'] = tilesAnimated



    def deltile(self,tilen):
        if str(tilen) in self.jsonTree['tiles']:
            self.jsonTree['tiles'].pop(str(tilen), None)
        if str(tilen) in self.jsonTree['tilesAnimated']:
            self.jsonTree['tilesAnimated'].pop(str(tilen), None)


class PaletteCfgWidget(QtWidgets.QWidget):
    def __init__(self, pal=None, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent
        if(pal==None):
            self.pal = PaletteFormat()
        else:
            self.pal = pal

        self.Grid = QtWidgets.QGridLayout(self)
        self.new()

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
        self.myScale = 2
        self.TileList = []

    def LoadPal(self, pal):
        self.pal.load(pal)
        self.img = os.path.join(current_project.settings['gamefolder'], self.pal.getimg())
        self.LoadImage()

    def LoadImage(self,img=None):
        if(img!=None):
            self.img = os.path.join(current_project.settings['gamefolder'], self.pal.imgloag(img))
            self.pal.imgloag(self.img)

        self.t = tile_set.TileSet(os.path.join(current_project.settings['gamefolder'],self.img))
        self.TileWidth = int(self.t.imageFile.size[0]/self.t.boxsize)
        self.TileHeight = int(self.t.imageFile.size[1]/self.t.boxsize)
        self.DrawPal()

    def DrawPal(self):
        # self.setUpdatesEnabled(False)
        self.setVisible(False)

        if len(self.TileList) > 1:
            for collum in self.TileList:
                for wdgt in collum:
                    wdgt.deleteLater()
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
                self.TileList[iy][jx].initTile(self.t.tileset, jx, iy,
                                               self.t.boxsize,
                                               tiletype,
                                               self.myScale,
                                               True)
                self.TileList[iy][jx].clicked.connect(self.TileClicked)
                self.TileList[iy][jx].rightClicked.connect(
                    self.TileRightClicked)
                i+=1

        self.resize(self.TileWidth * self.t.boxsize * self.myScale,
                    self.TileHeight * self.t.boxsize * self.myScale)
        self.setVisible(True)

    def setTile(self, tiletype):
        i = tiletype[0]
        x = int(i % self.TileWidth)
        y = int(i / self.TileWidth)
        tileid = -1
        tileanim = None
        if(tiletype[IDLAYER]!=0):
            tileid = tiletype[IDLAYER]
            layer=IDLAYER

        if(tiletype[ANIMLAYER]!=0):
            tileanim = tiletype[ANIMLAYER]
            layer=ANIMLAYER

        self.pal.settile(T(tileid,(x,y),tileanim))

        if(tileid != -1):
            for iy in range(self.TileHeight):
                for jx in range(self.TileWidth):
                    if(self.TileList[iy][jx].tileType[IDLAYER] == int(tileid) and self.TileList[iy][jx].tileType[ANIMLAYER] == 0):
                        self.TileList[iy][jx].updateTileImageInMap(
                                                0,
                                                IDLAYER,
                                                self.t.tileset,
                                                self.myScale)

        if(tileanim != None):
            for iy in range(self.TileHeight):
                for jx in range(self.TileWidth):
                    if(self.TileList[iy][jx].tileType[3] == int(tileanim) and self.TileList[iy][jx].tileType[4]== tiletype[IDLAYER]):
                        self.TileList[iy][jx].updateTileImageInMap(
                                                0,
                                                ANIMLAYER,
                                                self.t.tileset,
                                                self.myScale)

        self.TileList[y][x].updateTileType(self.t.tileset, tiletype)

        print(self.pal.jsonTree)

    def getTileType(self,x,y):
        tile = self.pal.gettile(x,y)
        if int(tile.id) != -1:
            if tile.anim == None:
                return [0,0,0,0,int(tile.id)]
            else:
                return [0,0,0,tile.anim,int(tile.id)]
        else:
            return [0,0,0,0,0]

    def TileClicked(self):
        command = CommandSetTileType(self, self.sender(), 'id', self.currentType, "set id")
        self.parent.undostack.push(command)
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            self.currentType+=1
            if(self.currentType>299):
                self.currentType=0
            self.parent.animSpinbox.setValue(self.currentType)

    def TileRightClicked(self):
        command = CommandSetTileType(self, self.sender(), 'anim', self.currentAnim, "set anim")
        self.parent.undostack.push(command)
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            self.currentAnim+=1
            if(self.currentAnim>4):
                self.currentAnim=0
            self.parent.animSpinbox.setValue(self.currentAnim)

    def changeTileIdCurrent(self, num):
        self.currentType = num
    def changeAnimIdCurrent(self, num):
        self.currentAnim = num


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
    def __init__(self, parent=None, ssettings={}, **kwargs):
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

        #this block creates the main button to open and save a palette
        HBox=QtWidgets.QHBoxLayout()
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.buttonClicked[QtWidgets.QAbstractButton].connect(self.buttonClicked)
        buttons=[{'name':'new palette' , 'id':0, 'objname':'new_pal' },
                 {'name':'open palette', 'id':1, 'objname':'open_pal'},
                 {'name':'save palette', 'id':2, 'objname':'save_pal'},
                 {'name':'open image', 'id':3, 'objname':'open_palimg'},
                 {'name':'open game project', 'id':4, 'objname':'open_gamefolder'}]
        for b in buttons:
            button = QtWidgets.QPushButton(b['name'])
            button.setObjectName(b['objname'])
            self.buttonGroup.addButton(button, b['id'])
            HBox.addWidget(button)

        #this will create the basic palette editor widget
        self.myPalWidget = PaletteCfgWidget(parent=self)
        self.PalscrollArea = QtWidgets.QScrollArea(self)
        self.PalscrollArea.setWidget(self.myPalWidget)


        #adding a toolbar
        self.toolbar = QtWidgets.QToolBar(self)

        #this will add id and anim control
        undoaction = self.undostack.createUndoAction(self, self.tr("&Undo"))
        redoaction = self.undostack.createRedoAction(self, self.tr("&Redo"))
        self.toolbar.addAction(undoaction)
        self.toolbar.addAction(redoaction)

        labelIdCurrent = QtWidgets.QLabel("Tile Nº")
        self.tileSpinbox = QtWidgets.QSpinBox(self)
        self.tileSpinbox.setToolTip("Tile 0 means not selected.")
        self.tileSpinbox.setMinimum(0)
        self.tileSpinbox.setMaximum(299)
        self.tileSpinbox.setSingleStep(1)
        self.tileSpinbox.valueChanged.connect(self.myPalWidget.changeTileIdCurrent)
        labelAnimCurrent = QtWidgets.QLabel("Tile Animated")
        self.animSpinbox = QtWidgets.QSpinBox(self)
        self.animSpinbox.setToolTip("0 means not animated.")
        self.animSpinbox.setMinimum(0)
        self.animSpinbox.setMaximum(4)
        self.animSpinbox.setSingleStep(1)
        self.animSpinbox.valueChanged.connect(self.myPalWidget.changeAnimIdCurrent)
        SpinHBox=QtWidgets.QHBoxLayout()
        SpinHBox.setAlignment(QtCore.Qt.AlignLeft)
        SpinHBox.addWidget(labelIdCurrent)
        SpinHBox.addWidget(self.tileSpinbox)
        SpinHBox.addWidget(labelAnimCurrent)
        SpinHBox.addWidget(self.animSpinbox)


        VBox.addWidget(self.toolbar)
        VBox.addLayout(HBox)
        VBox.addLayout(SpinHBox)
        VBox.addWidget(self.PalscrollArea)

    def buttonClicked(self, button):
        if  (button.objectName()=='new_pal'):
            self.myPalWidget.new()
        elif(button.objectName()=='open_pal'):
            self.openPalette()
        elif(button.objectName()=='save_pal'):
            pass
        elif(button.objectName()=='open_palimg'):
            self.openImage()
        elif(button.objectName()=='open_gamefolder'):
            self.openProject()

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

if __name__ == "__main__":
    from sys import argv, exit

    a = QtWidgets.QApplication(argv)
    m = PaletteEditorWidget()
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
