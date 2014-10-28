import os
import server
import sys
import json
import TileXtra
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import fifl

facing = ["up","left","down","right"]
standardStateset = ["normalSet"]
standardMovement = ["standing","walking"]

GAMEFOLDER = "gamefolder"

class BaseFormat:
    def __init__( self ):
        self.jsonTree = {};

    def new(self):
        self.jsonTree = {};

    def save( self , charsn):
        f = open( charsn , "wb" )
        tMat.fwriteKeyVals(self.jsonTree, f)
        f.close()

    def exportJS( self , charsn):
        f = open( charsn , "wb" )
        f.write("var " + self.levelName + "= {\n")
        tMat.fwriteKeyValsJS(self.jsonTree, f)
        f.write("};")
        f.close()

    def load(self , charsn):
        f = open( charsn , "rb" )
        self.jsonTree = json.load(f)
        f.close()


class CharasetFormat(BaseFormat):
    def __init__( self ):
        BaseFormat.__init__(self)

        self.size = [32,64]
        self.boxsize = 32

        self.new()

    def new(self):
        self.jsonTree = { "Charasets": {} }

    def setTileImage(self, tileImage):
        self.jsonTree["Charasets"]["tileImage"] = tileImage

    def addCharaset(self, name, tileImage, stateSet = standardStateset[0]):
        self.jsonTree["Charasets"][name] = {   "currentSet": stateSet,
	                                          stateSet:{}
                                              } 

    def addToStateset(self, Charaset, name = standardMovement[0],  stateSet = standardStateset[0]):
        self.jsonTree["Charasets"][Charaset][stateSet][name] ={}

    def addAnim(self, Charaset, anim,  nfacing = 0, movement = standardMovement[0], stateSet = standardStateset[0]):
        self.jsonTree["Charasets"][Charaset][stateSet][movement][facing[nfacing]] = anim

    def getImage(self, Charaset, anim = 0,  nfacing = facing[3], movement = standardMovement[0], stateSet = standardStateset[0]):
        cropPosition =  self.jsonTree["Charasets"][Charaset][stateSet][movement][nfacing][anim]
        for i in xrange(len(cropPosition)):
            cropPosition[i] = cropPosition[i]*self.boxsize

        returnValue = { "tileImage" :  self.jsonTree["Charasets"][Charaset]["tileImage"],
                        "cropPosition" :  cropPosition,
                        "size" : self.size }

        return returnValue


class CharasFormat(BaseFormat):
    def __init__( self ):
        BaseFormat.__init__(self)

        self.new()

    def new(self):
        self.jsonTree = { "Charas": {} }

    def addChara(self, name, charaFile, charaSet, facing = "back"):

        self.jsonTree["Charas"][name]= {    "charaFile": charaFile, 
                                            "charaSet": charaSet, 
                                            "facing": facing,
                                            "stateActions": {}
                                            } 


class BaseCharaset:
    def __init__( self , image_file):

        self.init(image_file)
        self.imgFile = image_file

    def init( self , image_file):
        self.bcset = []
        self.boxw = 32
        self.boxh = 64
        self.boxsize = (self.boxw, self.boxh)        
        self.imageFile = Image.open( image_file )
        if self.imageFile.size[0] % self.boxsize[0] == 0 and self.imageFile.size[1] % self.boxsize[1] ==0 :
            currentx = 0
            currenty = 0
            tilei = 0
            yj = 0
            while currenty < self.imageFile.size[1]:
                self.bcset.append([]) 
                while currentx < self.imageFile.size[0]:
                    imageTemp = self.imageFile.crop((currentx,currenty,currentx + self.boxw, currenty + self.boxh))
                    self.bcset[yj].append([imageTemp,imageTemp.resize((self.boxw*2, self.boxh*2), Image.NEAREST) , imageTemp.resize((int(self.boxw*0.5), int(self.boxh*0.5)), Image.NEAREST)]  )
                    currentx += self.boxw

                yj += 1
                currenty += self.boxh
                currentx = 0

        else:
            print ("error:Your file width and height are not good to {0}x{1} pixel charaset!".format(self.boxw,self.boxh))

    def getTileSetImage(self, TileType):
        tileImage = ImageQt( self.tileset[ TileType[1]][TileType[0]] )
        pixmap = QtGui.QPixmap.fromImage(tileImage)
        image = QtGui.QPixmap(pixmap)
        return image



class CharaPalette(QWidget):
    def __init__(self, base_image=None ,parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.Grid = QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)
        self.boxw = 32
        self.boxh = 64
        self.boxsize = (self.boxw, self.boxh)  

        self.scale = 2

        self.charasetList = []

        if(base_image != None):
            self.update(base_image)

    def update(self, base_image):
        self.baseImage = base_image
        self.draw()

    def draw(self):

        self.myBC = BaseCharaset( self.baseImage )

        self.setVisible(False)

        self.charHei = len(self.myBC.bcset)
        self.charWid = len(self.myBC.bcset[0])

        if len(self.charasetList) > 1:
            for collum in self.charasetList:
                for wdgt in collum:
                    wdgt.deleteLater()
                    wdgt = None
            self.charasetList = []
            
        # get the background numbers and use to get the tiles
        # for i in height    
        for iy in xrange(self.charHei):
            # for j in width
            self.charasetList.append([])
            for jx in range(self.charWid):
                self.charasetList[iy].append(CharaTile(self))
                self.Grid.addWidget(self.charasetList[iy][jx], iy, jx)
                self.charasetList[iy][jx].init( self.myBC.bcset, self.boxsize, [iy,jx], self.scale)
                self.connect(self.charasetList[iy][jx], SIGNAL('clicked()'), self.csetSinClick)              

        self.resize(self.charWid*self.boxw*self.scale,self.charHei*self.boxh*self.scale)

        self.setVisible(True)

    def csetSinClick(self):
        self.rValue = (self.sender().charType, self.myBC.bcset, self.scale)
        self.emit(SIGNAL('clicked()'))  
 

class CharaTile(QLabel):
    def __init(self, parent):
        QLabel.__init__(self, parent)

        self.charType = []
        self.boxw = 32
        self.boxh = 64
        self.boxsize = (self.boxw, self.boxh)  
        self.setMinimumSize (QSize(self.boxw, self.boxh))

    def init(self, bcset, boxsize, charType, scale = 1):
        self.charType = charType
        self.boxsize = boxsize
        self.boxw = self.boxsize[0]
        self.boxh = self.boxsize[1]

        if(scale==2):
            tempscale=1
        elif(scale==0.5):
            tempscale=2
        else:
            tempscale=0

        Composite = bcset[charType[0]][charType[1]][tempscale]
        pixmap = QtGui.QPixmap.fromImage(ImageQt( Composite ))
        self.setPixmap(pixmap)

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.emit(SIGNAL('rightClicked()'))
        else:
            self.emit(SIGNAL('clicked()'))

class csetsItem(QtGui.QListWidgetItem):
    def __init__(self, aname, jsonTree = {}):
        super(csetsItem, self).__init__(aname)

        self.aname = aname
        self.jsonTree = jsonTree

class AnimNamesItem(QtGui.QListWidgetItem):
    def __init__(self, aname, isgroup = False, isparent = False):
        super(AnimNamesItem, self).__init__(aname)

        self.isgroup = isgroup
        self.isparent = isparent
        self.ischildof = False
        self.aname = aname
        self.aarray = []

    def setIschildof(self,parent):
        self.ischildof = parent

    def getIschildof(self):
        return self.ischildof

    def setAarray(self, aarray):
        self.aarray = aarray

    def getAarray(self):
        return self.aarray

class CsetAItem(QtGui.QListWidgetItem):
    def __init__(self, charType, bcset, scale=1):
        super(CsetAItem, self).__init__()

        if(scale==2):
            tempscale=1
        elif(scale==0.5):
            tempscale=2
        else:
            tempscale=0

        Composite = bcset[charType[0]][charType[1]][tempscale]
        pixmap = QtGui.QPixmap.fromImage(ImageQt( Composite ))

        f=QFont ()
        f.setPointSize(1)
        self.setFont(f)

        self.setIcon(QIcon(pixmap))
        self.setData(Qt.UserRole, charType)

    def getCharType(self):
        return self.data(Qt.UserRole).toPyObject()


class AnimatedCharaTile(QLabel):
    def __init__(self, parent = None):
        QLabel.__init__(self, parent)

        self.charType = []
        self.boxw = 32
        self.boxh = 64
        self.scale = 2
        self.boxsize = (self.boxw, self.boxh)  
        self.setMinimumSize (QSize(self.boxw*2, self.boxh*2))
        self._timer = QtCore.QTimer(interval=100,
                                    timeout=self._animation_step)

        self.clearAnim()

    def setACTImage(self, charType):
        self.charType = charType
        scale = self.scale        

        if(scale==2):
            tempscale=1
        elif(scale==0.5):
            tempscale=2
        else:
            tempscale=0

        Composite = self.bcset[charType[0]][charType[1]][tempscale]
        pixmap = QtGui.QPixmap.fromImage(ImageQt( Composite ))
        self.setPixmap(pixmap)

    def clearAnim(self):
        self._timer.stop()
        pixmap = QPixmap(self.boxw*self.scale, self.boxh*self.scale)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)


    def setAnimArray(self,bcset, aarray, scale = 2):
        self.aarray = aarray
        self.bcset = bcset
        self.scale = scale
        self._current_frame = 0
        self.play()

    def play(self):
        self._timer.start()

    def _animation_step(self):    
        if(len(self.aarray)>0):
            self.setACTImage(self.aarray[self._current_frame])
            self._current_frame += 1
            if self._current_frame >= len(self.aarray):
                self._current_frame = 0
        
def isFacing(test):
    for i in xrange(len(facing)):
        if(test == facing[i]):
            return True
    return False

def isParent(jsonTreeItem):
    for anim in jsonTreeItem:
        if(isFacing(anim)):
            return True

    return False

class CharasetEditorWidget(QWidget):
    def __init__(self, parent=None, ssettings={}, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.cset = CharasetFormat() 

        self.ssettings = ssettings

        self.updating = False

        self.HBox = QHBoxLayout(self)
        self.HBox.setAlignment(Qt.AlignTop)

        self.csetsOpenEdit = QLineEdit()
        self.csetsNewButton = QPushButton("New")
        self.csetsOpenButton = QPushButton("Open")
        self.csetsSaveButton = QPushButton("Save")

        self.csetsNewButton.clicked.connect(self.charasetNew)
        self.csetsOpenButton.clicked.connect(self.charasetOpen)
        self.csetsSaveButton.clicked.connect(self.charasetSave)

        HBoxOpen = QHBoxLayout()
        HBoxOpen.addWidget(self.csetsNewButton)
        HBoxOpen.addWidget(self.csetsOpenButton)
        HBoxOpen.addWidget(self.csetsSaveButton)

        self.csetsEntry = QLineEdit()
        self.csetsAddButton = QPushButton("Add")
        self.csetsDelButton = QPushButton("Delete")
        HBoxEntry = QHBoxLayout()
        HBoxEntry.addWidget(self.csetsEntry)
        HBoxEntry.addWidget(self.csetsAddButton)
        HBoxEntry.addWidget(self.csetsDelButton)

        self.csetsList = QListWidget()
        self.csetsList.itemSelectionChanged.connect(self.csetsListSelectionChanged)

        VBoxCSets = QVBoxLayout()
        VBoxCSets.addWidget(QLabel("Charaset File:"))
        VBoxCSets.addWidget(self.csetsOpenEdit)
        VBoxCSets.addLayout(HBoxOpen)
        VBoxCSets.addWidget(QLabel("Entry name to add:"))
        VBoxCSets.addLayout(HBoxEntry)
        VBoxCSets.addWidget(self.csetsList)

        self.palette = CharaPalette()
        self.connect(self.palette, SIGNAL('clicked()'), self.animselected)
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.palette)
        self.scrollArea.setMinimumWidth(self.palette.boxw*self.palette.scale*3+16)
        self.scrollArea.setMinimumHeight(self.palette.boxh*self.palette.scale*4+16)

        self.palImageFile = QLineEdit()
        self.palImageFileButton = QPushButton("Open")
        self.palImageFileButton.clicked.connect(self.imgOpen)

        self.animList = QListWidget()
        self.animList.setIconSize(QSize(64,128))
        self.animList.setFlow(QListWidget.LeftToRight)
        self.animList.setMinimumWidth(self.palette.boxw*self.palette.scale*4+48)
        self.animList.setMinimumHeight(self.palette.boxh*self.palette.scale*2+16)
        self.animList.setMaximumHeight(self.palette.boxh*self.palette.scale*2+16)
        self.animList.setDragDropMode(QAbstractItemView.InternalMove)
        self.animListDel = QPushButton("Delete Frames")
        self.animListDel.clicked.connect(self.animListDelAction)

        animListModel = self.animList.model()
        animListModel.layoutChanged.connect(self.animListUpdated)
        animListModel.rowsInserted.connect(self.animListUpdated)


        self.animNamesEntry = QLineEdit()
        self.animNamesAdd = QPushButton("Add animation")
        self.animNamesAdd.clicked.connect(self.animNamesAddAction)
        self.animNamesCheckBNF = QCheckBox("No facing")
        self.animNamesDel = QPushButton("Delete")
        self.animNamesDel.clicked.connect(self.animNamesDelAction)
        self.animNames = QListWidget()
        self.animNames.itemSelectionChanged.connect(self.animNamesSelectionChanged)

        self.animPreview = AnimatedCharaTile()

        HBoxCharaPalName = QHBoxLayout()
        HBoxCharaPalName.addWidget(self.palImageFile)
        HBoxCharaPalName.addWidget(self.palImageFileButton)

        VBoxCharaPalette = QVBoxLayout()
        VBoxCharaPalette.addWidget(QLabel("Image file to load:"))
        VBoxCharaPalette.addLayout(HBoxCharaPalName)
        VBoxCharaPalette.addWidget(QLabel("Available frames:"))
        VBoxCharaPalette.addWidget(self.scrollArea)

        HBoxANE = QHBoxLayout()
        HBoxANE.addWidget(self.animNamesEntry)
        HBoxANE.addWidget(self.animNamesAdd)
        HBoxANE.addWidget(self.animNamesCheckBNF)
        HBoxANE.addWidget(self.animNamesDel)

        HBoxAnim = QHBoxLayout()
        HBoxAnim.addWidget(self.animPreview)
        HBoxAnim.addWidget(self.animListDel)

        VBoxCharaAnim = QVBoxLayout()

        VBoxCharaAnim.addWidget(QLabel("Animation Sequence:"))
        VBoxCharaAnim.addLayout(HBoxANE)
        VBoxCharaAnim.addWidget(self.animNames)
        VBoxCharaAnim.addLayout(HBoxAnim)
        VBoxCharaAnim.addWidget(QLabel("Animation Frames:"))
        VBoxCharaAnim.addWidget(self.animList)
        
        self.HBox.addLayout(VBoxCSets)
        self.HBox.addLayout(VBoxCharaPalette)
        self.HBox.addLayout(VBoxCharaAnim)

        self.animNamesEntry.textChanged.connect(self.animNamesEnable)
        self.animNamesAdd.setEnabled(False)
        self.animNames.setEnabled(False)

    def csetsListSelectionChanged(self):
        if (len(self.csetsList.selectedItems())>0):
            self.animNames.clear()

            jsonTree = self.csetsList.selectedItems()[0].jsonTree

            print(jsonTree)
            for item in jsonTree:
                if(isParent(jsonTree[item])):
                    parentItem = AnimNamesItem(item, True, True)
                    self.animNames.addItem(parentItem ) 
                    for i in xrange(len(facing)):
                        itemToAdd = AnimNamesItem("    "+facing[i])
                        itemToAdd.setIschildof(parentItem)
                        itemToAdd.aarray = jsonTree[item][facing[i]]
                        self.animNames.addItem(itemToAdd)

            self.animNames.setEnabled(True)
             


    def charasetNew(self):

        self.csetsList.clear()
        self.animNames.clear()
        self.animList.clear()

    def charasetOpen(self):

        self.csetsList.clear()
        self.animNames.clear()
        self.animList.clear()

        if(self.ssettings == {} ):
            filepath =  os.path.expanduser("~")
       
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', filepath ) )
        if os.path.isfile(filename):
            self.cset.load(filename)
            self.ssettings["gamefolder"] = os.path.abspath(os.path.join(os.path.dirname(str(filename)),"../../"))
            self.__imgOpen(os.path.join(self.ssettings["gamefolder"], fifl.IMG, self.cset.jsonTree["Charaset"]["tileImage"]))
            for charset in self.cset.jsonTree["Charaset"]:
                if(charset!="tileImage"):
                    self.csetsList.addItem(csetsItem(charset, self.cset.jsonTree["Charaset"][charset]))

    def charasetSave(self):
        self.cset.new()

        animation = {}
        for itemIndex in xrange(self.animNames.count()):
            if(self.animNames.item(itemIndex).isparent):
                animation[self.animNames.item(itemIndex).aname]={}

    def imgOpen(self):

        if(self.ssettings == {}):
            filepath =  os.path.expanduser("~")
       
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', filepath ) )
        if os.path.isfile(filename):
            __imgOpen(filename)

    def __imgOpen(self,filename):
        self.palette.update(filename)
        self.palImageFile.setText(filename)

        self.animList.clear()
        self.animNames.clear()
            

    def animNamesEnable(self, dummy):
        if(len(self.animNamesEntry.text())>0):
            self.animNamesAdd.setEnabled(True)
            self.animNames.setEnabled(True)
        else:
            self.animNamesAdd.setEnabled(False)
            self.animNames.setEnabled(False)
        

    def animNamesDelAction(self):
        if (len(self.animNames.selectedItems())>0):
            for item in self.animNames.selectedItems():
                if(item.isparent):
                    for itemIndex in xrange(self.animNames.count()):
                        if(self.animNames.item(itemIndex).ischildof == item):
                            self.animNames.takeItem(itemIndex)

                    itemIndex = self.animNames.row(item)
                    self.animNames.takeItem(itemIndex)
                elif(item.ischildof):
                    itemsToTake=[]
                    for itemIndex in xrange(self.animNames.count()):
                        if(self.animNames.item(itemIndex).ischildof == item.ischildof and self.animNames.item(itemIndex) != item):
                            itemsToTake.append(self.animNames.item(itemIndex))

                    for itemtotake in itemsToTake:
                        self.animNames.takeItem(self.animNames.row(itemtotake))

                    itemIndex = self.animNames.row(item.ischildof)
                    self.animNames.takeItem(itemIndex)

                    itemIndex = self.animNames.row(item)
                    self.animNames.takeItem(itemIndex)

        else:
            self.animNames.clear()  

        self.updating = True
        self.animList.clear()
        self.animPreview.clearAnim()
        self.updating = False

        self.animNamesSelectionChanged()

    def animListDelAction(self):
        if (len(self.animList.selectedItems())>0):
                for item in self.animList.selectedItems():
                    itemIndex = self.animList.row(item)
                    self.animList.takeItem(itemIndex)
        else:
            self.animList.clear()  

        self.animListUpdated()    

    def animNamesSelectionChanged(self):
        self.animPreview.clearAnim()

        if (len(self.animNames.selectedItems())>0):
            if(self.animNames.selectedItems()[0].isgroup):
                curRow = self.animNames.currentRow()
                curRow += 1
                self.animNames.setCurrentRow(curRow)
            
            if(self.animNames.selectedItems()[0].isgroup==False):
                animArray = self.animNames.selectedItems()[0].getAarray()
                scale = 2
                bcset = self.palette.myBC.bcset

                self.updating = True

                self.animList.clear()  
                if( len(animArray)> 0):
                    for item in animArray:
                        print(item)
                        #right now there is a bug, x and y seem to be somehow inverted..
                        self.animList.addItem(CsetAItem(item, bcset, 2) )

                self.updating = False
                self.animPreview.setAnimArray(bcset, animArray)

    def animNamesAddAction(self):
        if(len(self.animNamesEntry.text())>0):
            if self.animNamesCheckBNF.isChecked():
                self.animNames.addItem(AnimNamesItem(self.animNamesEntry.text(), False, True) ) 
            else: 
                parentItem = AnimNamesItem(self.animNamesEntry.text(), True, True)
                self.animNames.addItem(parentItem ) 
                for i in xrange(len(facing)):
                    itemToAdd = AnimNamesItem("    "+facing[i])
                    itemToAdd.setIschildof(parentItem)
                    self.animNames.addItem(itemToAdd) 

    
    def animselected(self):
        if (len(self.animNames.selectedItems())>0):
            self.animList.addItem(CsetAItem(self.palette.rValue[0], self.palette.rValue[1], self.palette.rValue[2] ) )
            print(self.palette.rValue[0])

    def animListUpdated(self):
        if(self.updating == False):
            if (self.animList.count() > 0):
                animArray = []
                i = 0
                while i < self.animList.count():
                    item = self.animList.item(i)
                    animArray.append(item.getCharType())
                    i += 1

                self.animPreview.setAnimArray(self.palette.myBC.bcset, animArray)
                self.animNames.selectedItems()[0].setAarray(animArray)
            else:
                self.animPreview.clearAnim()
                self.animNames.selectedItems()[0].setAarray([])
        


class CharasPaletteWidget(QWidget):
    def __init__(self,pMap, pSettings, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

class CharasEditorWidget(QWidget):
    def __init__(self,pMap, pSettings, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)


if __name__=="__main__":
    from sys import argv, exit

    a=QApplication(argv)
    m=CharasetEditorWidget()
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
