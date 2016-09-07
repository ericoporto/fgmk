import json
import os
from fgmk import tMat, getdata
from fgmk.ff import  base_model
import numpy as np

LayersName = ["layer1", "layer2", "layer4", "colision", "events"]
NonViewable = ["colision", "events"]
LayersNameViewable = [
    _layer for _layer in LayersName if _layer not in NonViewable]


class MapFormat(base_model.BaseFormat):
    """
    Creates a map. This object has functions to allow modifying the map
    jsonTree, saving to file, loading a file over, new map creation, and more.
    The map only exists in memory, it's not an image, canvas or similar.
    """
    def __init__(self, parent=None):
        #super().__init__()
        base_model.BaseFormat.__init__(self)

        self.parent = parent
        self.palette = []

        self.tileImage = ""

        self.levelName = ""
        self.LayersMapTiles = np.array(([[]],
                                        [[]]))

        self.listOfEvents = []

        self.listOfEventsTypes = dict()

        self.listOfActions = dict()

        self.listOfCharas = []

    def new(self, tlevelName, levelWidth, levelHeight, palettepath=None):

        if palettepath is None:
            f = open(getdata.path('default.pal.json'), 'r')
            levelPalette = json.load(f)
            f.close()
        else:
            f = open(os.path.join(palettepath), 'r')
            levelPalette = json.load(f)
            f.close()

        self.listOfEvents = []
        self.listOfCharas = []
        self.listOfEventsTypes = dict()
        self.listOfActions = dict()

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

    def updateJsonTree(self):

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

    def exportJS(self, mapn):
        #super().exportJS(mapn, self.levelName)
        base_model.BaseFormat.exportJS(self, mapn, self.levelName)


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
        if(0 in TileListFromLayer):
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
        #print("listOfActions index {0}".format(index))
        #print(self.listOfActions[str(event)][index])
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

    def setEventList(self,actionsAndType,event):
        eventType = actionsAndType['type']
        actionsList = actionsAndType['list']
        self.listOfActions[str(event)] = actionsList
        self.listOfEventsTypes[str(event)] = eventType
        self.updateJsonTree()
