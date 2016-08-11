import os
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_model, current_project, fifl, tile_set, base_tile

IDLAYER=3
ANIMLAYER=4

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
        self.jsonTree = {'tileImage': '',
                         'tiles': {},
                         'tilesAnimated': {}}

    def imgloag(self,imgfile):
        self.jsonTree['tileImage'] = imgfile

    def getimg(self):
        return self.jsonTree['tileImage']

    def addAnimTile(self,tileT):
        self.jsonTree['tilesAnimated'][tileT.id].append([tileT.x,tileT.y])

    def addTile(self,tileT):
        self.jsonTree['tiles'][tileT.id] = [tileT.x,tileT.y]

    def delTile(self,tilen):
        return self.jsonTree['tiles'].pop(str(tilen), None)


class PaletteCfgWidget(QtWidgets.QWidget):
    def __init__(self, pal=None, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent

        self.Grid = QtWidgets.QGridLayout(self)
        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        if(pal==None):
            self.pal = PaletteFormat()
        else:
            self.pal = pal
        self.T = []
        self.img = None

        self.TileWidth = 0
        self.TileHeight = 0
        self.myScale = 2
        self.TileList = []

    def LoadPal(self, pal):
        self.pal = pal
        self.img = os.path.join(current_project.settings['gamefolder'], self.pal.getimg())

    def LoadImage(self,img):
        self.img = os.path.join(fifl.IMG,os.path.basename(img))
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
            self.T.append([])
            for jx in range(self.TileWidth):
                self.T[iy].append(T(-1,(jx,iy)))
                self.TileList[iy].append(base_tile.QTile(self))
                self.Grid.addWidget(self.TileList[iy][jx], iy, jx)
                self.TileList[iy][jx].initTile(self.t.tileset, jx, iy,
                                               self.t.boxsize,
                                               [i,0,0,0,0],
                                               self.myScale)
                self.TileList[iy][jx].clicked.connect(self.TileClicked)
                self.TileList[iy][jx].rightClicked.connect(
                    self.TileRightClicked)
                i+=1

        self.resize(self.TileWidth * self.t.boxsize * self.myScale,
                    self.TileHeight * self.t.boxsize * self.myScale)
        self.setVisible(True)

    def setTile(self, x,y,anim_or_id='id',number=-1):
        if(anim_or_id=='id'):
            self.T[y][x].id = number
        else:
            self.T[y][x].anim = number

    def TileClicked(self):
        command = CommandSetTileType(self, self.sender(), 'id', 1, "set id")
        self.parent.undoStack.push(command)

    def TileRightClicked(self):
        pass

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
        self.id_or_anim = id_or_anim
        if(self.id_or_anim=='id'):
            self.Layer = IDLAYER
            self.changeTypeTo = new_id_or_anim
            self.oldType = self.sender.tileType[IDLAYER]
        else:
            self.Layer = ANIMLAYER
            self.changeTypeTo = new_id_or_anim
            self.oldType = self.sender.tileType[ANIMLAYER]

        self.pPaletteCfgWidget = pPaletteCfgWidget
        self.ptileset = pPaletteCfgWidget.t.tileset

    def redo(self):
        self.pPaletteCfgWidget.setTile(self.tileX, self.tileY,
                          self.id_or_anim, self.changeTypeTo)
        self.sender.updateTileImageInMap(
            self.changeTypeTo, self.Layer, self.ptileset, self.pPaletteCfgWidget.myScale)

    def undo(self):
        self.pPaletteCfgWidget.setTile(self.tileX, self.tileY,
                          self.id_or_anim, self.oldType)
        self.sender.updateTileImageInMap(
            self.oldType, self.Layer, self.ptileset, self.pPaletteCfgWidget.myScale)



class PaletteEditorWidget(QtWidgets.QDialog):
    def __init__(self, parent=None, ssettings={}, **kwargs):
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.pal = PaletteFormat()

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

        #this will create a undo stack
        self.undoStack = QtWidgets.QUndoStack(self)

        VBox.addLayout(HBox)
        VBox.addWidget(self.PalscrollArea)

    def buttonClicked(self, button):
        if  (button.objectName()=='new_pal'):
            self.pal.new()
        elif(button.objectName()=='open_pal'):
            self.openPalette()
        elif(button.objectName()=='save_pal'):
            self.pal.addTile(T(1,(1,1)))
            self.pal.addTile(T(2,(1,2)))
            print(self.pal.jsonTree)
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
            self.pal.load(filename)

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
