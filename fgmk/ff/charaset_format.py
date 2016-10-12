# -*- coding: utf-8 -*-
import os
from fgmk import fifl
from fgmk.ff import base_model

facing = ["up", "left", "down", "right"]
standardStateset = ["normalSet"]
standardMovement = ["standing", "walking"]

GAMEFOLDER = "gamefolder"

class CharasetFormat(base_model.BaseFormat):

    def __init__(self):
        #super().__init__()
        base_model.BaseFormat.__init__(self)

        self.size = [32, 64]
        self.boxsize = 32

        self.new()

    def loadGameFolder(self,gamefolder):
        if gamefolder != '':
            for f in os.listdir(os.path.join(gamefolder, fifl.CHARASETS)):
                if f.endswith(".json"):
                    break

            f = os.path.join(gamefolder, fifl.CHARASETS, f)
            if(os.path.isfile(f)):
                self.load(f)

    def new(self):
        self.jsonTree = {"Charaset": {}}

    def setTileImage(self, tileImage):
        self.jsonTree["Charaset"]["tileImage"] = tileImage

    def getTileImage(self):
        if "tileImage" in self.jsonTree["Charaset"]:
            return self.jsonTree["Charaset"]["tileImage"]
        else:
            return False

    def addCharaset(self, name, jsonTree={}):
        self.jsonTree["Charaset"][name] = jsonTree

    def getCharasets(self):
        charasetsa = self.jsonTree["Charaset"]
        excludes = ["tileImage"]
        resultset = [key for key, value in charasetsa.items()
                     if key not in excludes]
        return sorted(resultset)

    def getAnimations(self, charaset):
        csetTree = self.jsonTree["Charaset"][charaset]
        return csetTree.keys()

    def getAnimation(self, charaset):
        csetTree = self.jsonTree["Charaset"][charaset]
        csetTL1 = sorted(csetTree)
        tests = standardMovement[:]
        tests.append(sorted(csetTree)[0])
        for test in tests:
            if test in csetTL1:
                if (isinstance(csetTree[test], list)):
                    return csetTree[test]
                else:
                    csetTL2 = sorted(csetTree[test])
                    for face in sorted(facing):
                        if face in csetTL2:
                            return csetTree[test][face]
