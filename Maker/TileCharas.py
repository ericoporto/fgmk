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

    def addCharaset(self, name, tileImage, stateSet = standardStateset[0]):
        self.jsonTree["Charasets"][name] = {   "currentSet": stateSet,
                                              "tileImage": tileImage,
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

    def init( self , image_file):
        self.bcset = []
        self.boxw = 32
        self.boxh = 64
        self.boxsize = (self.boxw, self.boxh)        
        self.imageFile = Image.open( image_file )
        if self.imageFile.size[0] % self.boxsize(0) == 0 and self.imageFile.size[1] % self.boxsize(1) ==0 :
            currentx = 0
            currenty = 0
            tilei = 0
            yj = 0
            while currenty < self.imageFile.size[1]:
                bcset.append([]) 
                while currentx < self.imageFile.size[0]:
                    imageTemp = self.imageFile.crop((currentx,currenty,currentx + self.boxsize, currenty + self.boxsize))
                    self.bcset[yj].append([imageTemp,imageTemp.resize((self.boxw*2, self.boxh*2), Image.NEAREST) , imageTemp.resize((int(self.boxw*0.5), int(self.boxh*0.5)), Image.NEAREST)]  )
                    currentx += self.boxw

                yj += 1
                currenty += self.boxh
                currentx = 0

    def getTileSetImage(self, TileType):
        tileImage = ImageQt( self.tileset[ TileType ] )
        pixmap = QtGui.QPixmap.fromImage(tileImage)
        image = QtGui.QPixmap(pixmap)
        return image

class CharaTile(QLabel):
    def __init(self, parent):
        QLabel.__init__(self, parent)

        self.tileType = []
        self.boxWidth = 32
        self.boxHeight = 64
        self.boxSize = (self.boxWidth, self.boxHeight)
        self.setMinimumSize (QSize(self.boxWidth, self.boxHeight))

    def initTile(self, tileset, x, y, boxSize, tileType, scale = 1):
        self.tileType = tileType
        self.boxSize = boxSize

        if(scale==2):
            tempscale=1
        elif(scale==0.5):
            tempscale=2
        else:
            tempscale=0

        Composite = clearTile.tileset[0][tempscale]

        Composite = Image.alpha_composite(Composite, tileset[ tileType[i] ][tempscale]) 
   

        pixmap = QtGui.QPixmap.fromImage(ImageQt( Composite ))
        self.setPixmap(pixmap)




class CharasetEditorWidget(QWidget):
    def __init__(self, pSettings, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        

class CharasPaletteWidget(QWidget):
    def __init__(self,pMap, pSettings, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

class CharasEditorWidget(QWidget):
    def __init__(self,pMap, pSettings, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
