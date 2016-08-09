# -*- coding: utf-8 -*-
import json
from fgmk import write_file

class BaseFormat:
    def __init__(self, filename=""):
        self.jsonTree = {}
        self.filename = filename

    def new(self):
        self.jsonTree = {}

    def save(self, filename=""):
        self.updateJsonTree()

        if(filename != ""):
            self.filename = filename

        write_file.writesafe(self.jsonTree, self.filename)

    def exportJS(self, filename="", jsvarname = ""):
        self.updateJsonTree()

        if(filename != ""):
            self.jsfilename = filename

        if(jsvarname != ""):
            self.jsvarname = jsvarname
        else:
            self.jsvarname = os.path.splitext(os.path.basename(self.jsfilename))[0]

        write_file.writesafe(self.jsonTree, self.jsfilename, self.jsvarname )

    def load(self, filename=""):
        if(filename != ""):
            self.filename = filename

        f = open(self.filename, "r")
        self.jsonTree = json.load(f)
        f.close()

    def isEqual(self, objToCompare):
        self.updateJsonTree()
        return write_file.isJsonEqual(self.jsonTree,objToCompare.jsonTree)

    def updateJsonTree(self):
        pass
