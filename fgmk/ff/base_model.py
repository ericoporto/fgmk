# -*- coding: utf-8 -*-
import json
from fgmk.ff import write_file

class BaseFormat:
    """
    If you want to create a basic json, instantiate this class. If you want to
    define a json descriptor, inherit from this class.

    . this class has a property called jsonTree, which contains a dict, and a
    property filename, which has the filename to save it.
    . Calling save prints the jsonTree to a file named filename.
    . Calling load opens a json file named filename and loads it's contents to
    jsonTree
    . Both functions accept a filename as parameter to change it's filename
    value.
    . it's method isEqual allows comparing it with an object that inherits from
    itself.

    If you need to update the content of the jsonTree automatically before
    saving, you can replace the method updateJsonTree.
    """

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
