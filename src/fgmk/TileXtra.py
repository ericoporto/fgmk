import os
import sys
import json
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
from fgmk import tMat

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

COREIMGFOLDER = "coreimg/"
LayersName = ["layer1", "layer2", "layer4", "colision", "events"]
NonViewable = ["colision", "events"]
LayersNameViewable = [
    _layer for _layer in LayersName if _layer not in NonViewable]

emptyTile = Image.open(COREIMGFOLDER + "emptyTile.png")


def divideRoundUp(a, b):
    return (a / b) + (a % b > 0)


def tileFill(clickedX, clickedY, fullLayer, changeTToType):
    # This function applies bucket fill at point clickedX, clickedY of a ndarray
    # fullLayer, and returns a list of the format
    #[[pointx, pointy, tileType befor fill, tileType after fill] :]

    changeWhatType = fullLayer[clickedY, clickedX]

    binaryLayer = (fullLayer == changeWhatType).astype(np.int)
    whatChanged = []

    tMat.fill(binaryLayer, len(binaryLayer), len(
        binaryLayer[0]), clickedY, clickedX)

    for i in range(len(binaryLayer)):
        for j in range(len(binaryLayer[0])):
            if binaryLayer[i, j] == 2:
                whatChanged.append(([j, i, changeWhatType, changeTToType]))

    return whatChanged


def tileLine(firstClickedX, firstClickedY, lastClickedX, lastClickedY, fullLayer, changeTToType):
    # This function applies bucket fill at point clickedX, clickedY of a ndarray
    # fullLayer, and returns a list of the format
    #[[pointx, pointy, tileType befor fill, tileType after fill] :]

    whatChanged = []

    thisLinePoints = tMat.line(
        firstClickedX, firstClickedY, lastClickedX, lastClickedY)

    for point in thisLinePoints:
        x = point[0]
        y = point[1]
        whatChanged.append(([x, y, fullLayer[y, x], changeTToType]))

    return whatChanged


def tileRect(firstClickedX, firstClickedY, lastClickedX, lastClickedY, fullLayer, changeTToType):
    # This function applies bucket fill at point clickedX, clickedY of a ndarray
    # fullLayer, and returns a list of the format
    #[[pointx, pointy, tileType befor fill, tileType after fill] :]

    whatChanged = []

    thisRectPoints = tMat.rect(
        firstClickedX, firstClickedY, lastClickedX, lastClickedY)

    for point in thisRectPoints:
        x = point[0]
        y = point[1]
        whatChanged.append(([x, y, fullLayer[y, x], changeTToType]))

    return whatChanged


class actionItem(QtWidgets.QListWidgetItem):

    def __init__(self, actionAndParameter):
        super().__init__(str(actionAndParameter))
        self.setText = str(actionAndParameter)
        self.setData(Qt.UserRole, actionAndParameter)

    def getAction(self):
        actionAndParameterReturn = self.data(Qt.UserRole)
        action = str(actionAndParameterReturn[0])
        parameter = str(actionAndParameterReturn[1])
        return [action, parameter]


class MapFormat:

    def __init__(self):
        self.jsonTree = []

        self.palette = []

        self.tileImage = ""

        self.levelName = ""
        self.LayersMapTiles = np.array(([[]],
                                        [[]]))

        self.listOfEvents = []

        self.listOfEventsTypes = dict()

        self.listOfActions = dict()

        self.listOfCharas = []

    def new(self, tlevelName, levelWidth, levelHeight, levelPalette=None):

        if levelPalette is None:
            f = open("paletteDefault.json", "r")
            levelPalette = json.load(f)
            f.close()

        self.jsonTree = {"Level":
                         {
                             "levelName": tlevelName,
                             LayersName[0]: tMat.mnZeros(levelWidth, levelHeight),
                             LayersName[1]: tMat.mnZeros(levelWidth, levelHeight),
                             LayersName[2]: tMat.mnZeros(levelWidth, levelHeight),
                             LayersName[3]: tMat.mnZeros(levelWidth, levelHeight),
                             LayersName[4]: tMat.mnZeros(levelWidth, levelHeight),
                             "tiles": levelPalette['tiles'],
                             "tileImage": levelPalette['tileImage'],
                             "tilesAnimated": levelPalette['tilesAnimated'],
                             "eventsType": self.listOfEventsTypes,
                             "eventsActions": self.listOfActions,
                             "charas": self.listOfCharas
                         }
                         }
        self.LayersMapTiles = np.array((self.jsonTree['Level'][LayersName[0]],
                                        self.jsonTree['Level'][LayersName[1]],
                                        self.jsonTree['Level'][LayersName[2]],
                                        self.jsonTree['Level'][LayersName[3]],
                                        self.jsonTree['Level'][LayersName[4]]))

        self.palette = self.jsonTree['Level']['tiles']
        self.tileImage = self.jsonTree['Level']['tileImage']
        self.tilesAnimated = self.jsonTree['Level']['tilesAnimated']
        self.levelName = self.jsonTree['Level']['levelName']
        # print(self.LayersMapTiles)

    def save(self, mapn):
        f = open(mapn, "w")

        # print(self.listOfActions)

        self.jsonTree = {"Level":
                         {
                             "levelName": self.levelName,
                             LayersName[0]: self.LayersMapTiles[0, :, :].tolist(),
                             LayersName[1]: self.LayersMapTiles[1, :, :].tolist(),
                             LayersName[2]: self.LayersMapTiles[2, :, :].tolist(),
                             LayersName[3]: self.LayersMapTiles[3, :, :].tolist(),
                             LayersName[4]: self.LayersMapTiles[4, :, :].tolist(),
                             "tiles": self.palette,
                             "tileImage": self.tileImage,
                             "tilesAnimated": self.tilesAnimated,
                             "eventsType": self.listOfEventsTypes,
                             "eventsActions": self.listOfActions,
                             "charas": self.listOfCharas
                         }
                         }

        tMat.fwriteKeyVals(self.jsonTree, f)

        f.close()

    def exportJS(self, mapn):
        f = open(mapn, "w")

        self.jsonTree = {"Level":
                         {
                             "levelName": self.levelName,
                             LayersName[0]: self.LayersMapTiles[0, :, :].tolist(),
                             LayersName[1]: self.LayersMapTiles[1, :, :].tolist(),
                             LayersName[2]: self.LayersMapTiles[2, :, :].tolist(),
                             LayersName[3]: self.LayersMapTiles[3, :, :].tolist(),
                             LayersName[4]: self.LayersMapTiles[4, :, :].tolist(),
                             "tiles": self.palette,
                             "tileImage": self.tileImage,
                             "eventsType": self.listOfEventsTypes,
                             "eventsActions": self.listOfActions,
                             "tilesAnimated": self.tilesAnimated,
                             "charas": self.listOfCharas
                         }
                         }
        #f.write("var " + self.levelName + "= {};\n")
        #f.write(self.levelName + ".levels = [];\n")
        #f.write(self.levelName + ".levels[0] = {\n")

        f.write("var " + self.levelName + "= {\n")

        tMat.fwriteKeyValsJS(self.jsonTree, f)

        f.write("};")
        f.close()

    def load(self, mapn):
        f = open(mapn, "r")
        self.jsonTree = json.load(f)
        self.LayersMapTiles = []
        self.LayersMapTiles = np.array((self.jsonTree['Level'][LayersName[0]],
                                        self.jsonTree['Level'][LayersName[1]],
                                        self.jsonTree['Level'][LayersName[2]],
                                        self.jsonTree['Level'][LayersName[3]],
                                        self.jsonTree['Level'][LayersName[4]]))
        self.palette = self.jsonTree['Level']['tiles']
        self.tileImage = self.jsonTree['Level']['tileImage']
        if ('tilesAnimated' in self.jsonTree['Level']):
            self.tilesAnimated = self.jsonTree['Level']['tilesAnimated']
        else:
            self.tilesAnimated = {"": [[]]}

        if ('eventsType' in self.jsonTree['Level']):
            self.listOfEventsTypes = self.jsonTree['Level']['eventsType']

        if ('eventsActions' in self.jsonTree['Level']):
            self.listOfActions = self.jsonTree['Level']['eventsActions']

        if ('charas' in self.jsonTree['Level']):
            self.listOfCharas = self.jsonTree['Level']['charas']

        self.levelName = self.jsonTree['Level']['levelName']

        f.close()

    def getCharaList(self):
        return self.listOfCharas

    def insertChara(self, x, y, chara):
        self.listOfCharas.append([chara, x, y])

    def removeChara(self, x, y):
        for char in self.listOfCharas:
            if (char[1] == x and char[2] == y):
                self.listOfCharas.remove(char)
                break

    def setTile(self, x, y, layer, tiletype):
        self.LayersMapTiles[layer][y][x] = tiletype

    def getTileListFromLayer(self, layer):
        TileListFromLayer = np.unique(self.LayersMapTiles[layer]).tolist()
        TileListFromLayer.remove(0)
        self.listOfEvents = TileListFromLayer
        return TileListFromLayer

    def addActionToEvent(self, action, event):
        if self.listOfActions.get(str(event), None) is None:
            self.listOfActions[str(event)] = []
        self.listOfActions[str(event)].append(action)

    def insertActionToEvent(self, index, action, event):
        if self.listOfActions.get(str(event), None) is None:
            self.listOfActions[str(event)] = []
        self.listOfActions[str(event)].insert(index, action)

    def getActionOnEvent(self, index, event):
        if self.listOfActions.get(str(event), None) is None:
            self.listOfActions[str(event)] = []
        return self.listOfActions[str(event)][index]

    def changeActionOnEvent(self, index, action, event):
        if self.listOfActions.get(str(event), None) is None:
            self.listOfActions[str(event)] = []
        self.listOfActions[str(event)][index] = action

    def removeAllActionsOnEvent(self, event):
        self.listOfActions[str(event)] = []

    def removeLastActionOnEvent(self, event):
        if self.listOfActions.get(str(event), None) is None:
            self.listOfActions[str(event)] = []
        del self.listOfActions[str(event)][-1]

    def removeActionByIndexOnEvent(self, index, event):
        if self.listOfActions.get(str(event), None) is None:
            self.listOfActions[str(event)] = []
        print("listOfActions index {0}".format(index))
        print(self.listOfActions[str(event)][index])
        del self.listOfActions[str(event)][index]

    def getActionListOnEvent(self, event):
        if self.listOfActions.get(str(event), None) is None:
            self.listOfActions[str(event)] = []
        return self.listOfActions[str(event)]

    def setEventType(self, event, eventType):
        if self.listOfEventsTypes.get(str(event), None) is None:
            self.listOfEventsTypes[str(event)] = []
        self.listOfEventsTypes[str(event)] = eventType[:]

    def getEventType(self, event):
        if self.listOfEventsTypes.get(str(event), None) is None:
            self.listOfEventsTypes[str(event)] = [1, 0]
        return self.listOfEventsTypes[str(event)]


class TileSet:

    def __init__(self, image_file, tilePalette=None):
        if tilePalette is None:
            self.initWithoutPalette(image_file)
        else:
            self.initWithPalette(image_file, tilePalette)

    def initWithoutPalette(self, image_file):
        self.tileset = []
        self.boxsize = 32
        self.imageFile = Image.open(image_file)
        if self.imageFile.size[0] % self.boxsize == 0 and self.imageFile.size[1] % self.boxsize == 0:
            currentx = 0
            currenty = 0
            tilei = 0
            while currenty < self.imageFile.size[1]:
                while currentx < self.imageFile.size[0]:
                    imageTemp = self.imageFile.crop(
                        (currentx, currenty, currentx + self.boxsize, currenty + self.boxsize))
                    self.tileset.append([imageTemp, imageTemp.resize((self.boxsize * 2, self.boxsize * 2), Image.NEAREST),
                                         imageTemp.resize((int(self.boxsize * 0.5), int(self.boxsize * 0.5)), Image.NEAREST)])
                    tilei += 1
                    currentx += self.boxsize
                currenty += self.boxsize
                currentx = 0

    def initWithPalette(self, image_file, tilePalette):
        self.tileset = []
        self.boxsize = 32
        bxsz = self.boxsize
        self.tilePalette = tilePalette
        v = self.tilePalette
        self.imageFile = Image.open(image_file)
        if self.imageFile.size[0] % self.boxsize == 0 and self.imageFile.size[1] % self.boxsize == 0:
            if isinstance(self.tilePalette, dict):
                # remember: crop uses (( and )) because it is converting the
                # elements inside in coordinates
                self.tileset.append(emptyTile)
                sorted_keys = sorted(self.tilePalette, key=int)
                for k in sorted_keys:
                    #print("P Type= ", k, "  X= " ,v[k][0], "  Y= " , v[k][1])
                    #self.tileset.append( self.imageFile.crop((bxsz*v[k][0],bxsz*v[k][1],bxsz*v[k][0] + bxsz, bxsz*v[k][1] + bxsz)) )
                    imageTemp = self.imageFile.crop(
                        (bxsz * v[k][0], bxsz * v[k][1], bxsz * v[k][0] + bxsz, bxsz * v[k][1] + bxsz))
                    self.tileset.append([imageTemp, imageTemp.resize(
                        (bxsz * 2, bxsz * 2), Image.NEAREST), imageTemp.resize((int(bxsz * 0.5), int(bxsz * 0.5)), Image.NEAREST)])

    def getTileSetImage(self, TileType):
        tileImage = ImageQt(self.tileset[TileType])
        pixmap = QtGui.QPixmap.fromImage(tileImage)
        image = QtGui.QPixmap(pixmap)
        return image

colisionSet = TileSet(COREIMGFOLDER + "collisionTiles.png")
eventSet = TileSet(COREIMGFOLDER + "eventTiles.png")
clearTile = TileSet(COREIMGFOLDER + "clearTile.png")


class ExtendedQLabel(QLabel):

    def __init(self, parent):
        super().__init__(parent)

        self.tileType = []
        self.tileX = 0
        self.tileY = 0
        self.boxSize = 32
        self.ndPixmap = []
        #self.setMinimumSize(QSize(self.boxSize, self.boxSize))

    clicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def Rescale(self, tileset,  scale=1):
        self.scale = scale

        self.updateTileImageInMap(self.tileType[0], 0, tileset, self.scale)

    def initTile(self, tileset, x, y, boxSize, tileType, scale=1):
        self.tileType = tileType
        self.tileX = x
        self.tileY = y
        self.boxSize = boxSize
        self.scale = scale

        self.updateTileImageInMap(self.tileType[0], 0, tileset, self.scale)

    def updateTileImageInMap(self, ChangeTileType, layer, tileset,  scale=1):
        self.tileType[layer] = ChangeTileType
        self.scale = scale

        if(scale == 2):
            tempscale = 1
        elif(scale == 0.5):
            tempscale = 2
        else:
            tempscale = 0

        Composite = clearTile.tileset[0][tempscale]
        try:
            for i in range(len(self.tileType) - 2):
                if(self.tileType[i]):
                    Composite = Image.alpha_composite(
                        Composite, tileset[self.tileType[i]][tempscale])
            if(self.tileType[i + 1]):
                Composite = Image.alpha_composite(Composite, colisionSet.tileset[
                                                  self.tileType[i + 1]][tempscale])
            if(self.tileType[i + 2]):
                Composite = Image.alpha_composite(Composite, eventSet.tileset[
                                                  self.tileType[i + 2]][tempscale])
        except:
            for i in range(len(self.tileType) - 2):
                if(self.tileType[i]):
                    Composite = tMat.alpha_composite(
                        Composite, tileset[self.tileType[i]][tempscale])
            if(self.tileType[i + 1]):
                Composite = tMat.alpha_composite(Composite, colisionSet.tileset[
                                                 self.tileType[i + 1]][tempscale])
            if(self.tileType[i + 2]):
                Composite = tMat.alpha_composite(Composite, eventSet.tileset[
                                                 self.tileType[i + 2]][tempscale])

        if(scale != 1 and scale != 0.5 and scale != 2):
            Composite = Composite.resize(
                (int(self.boxSize * scale), int(self.boxSize * scale)), Image.NEAREST)

        pixmap = QtGui.QPixmap.fromImage(ImageQt(Composite))
        self.ndPixmap = pixmap
        self.setPixmap(pixmap)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()

    ##def wheelEvent(self, ev):
    #    self.emit(SIGNAL('scroll(int)'), ev.delta())
