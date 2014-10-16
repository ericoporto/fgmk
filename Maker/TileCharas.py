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
import actionDialog
import TXWdgt

facing = ["up","left","down","right"]
standardStateset = ["normalSet"]
standardMovement = ["standing","walking"]

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
        self.jsonTree = { "Charaset": {} }

    def addCharaset(self, name, tileImage, stateSet = standardStateset[0]):
        self.jsonTree["Charaset"][name] = {   "currentSet": stateSet,
                                              "tileImage": tileImage,
	                                          stateSet:{}
                                              } 

    def addToStateset(self, Charaset, name = standardMovement[0],  stateSet = standardStateset[0]):
        self.jsonTree["Charaset"][Charaset][stateSet][name] ={}

    def addAnim(self, Charaset, anim,  nfacing = 0, movement = standardMovement[0], stateSet = standardStateset[0]):
        self.jsonTree["Charaset"][Charaset][stateSet][movement][facing[nfacing]] = anim

    def getImage(self, Charaset, anim = 0,  nfacing = facing[3], movement = standardMovement[0], stateSet = standardStateset[0]):
        cropPosition =  self.jsonTree["Charaset"][Charaset][stateSet][movement][nfacing][anim]
        for i in xrange(len(cropPosition)):
            cropPosition[i] = cropPosition[i]*self.boxsize

        returnValue = { "tileImage" :  self.jsonTree["Charaset"][Charaset]["tileImage"],
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




class CharasPaletteWidget(QWidget):
    def __init__(self,pMap, pSettings, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

class CharasEditorWidget(QWidget):
    def __init__(self,pMap, pSettings, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
