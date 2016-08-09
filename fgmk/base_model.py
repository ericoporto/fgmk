import json
from fgmk import writefile

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

        writefile.writesafe(self.jsonTree, self.filename)

    def exportJS(self, filename="", jsvarname = ""):
        self.updateJsonTree()
        
        if(filename != ""):
            self.jsfilename = filename

        if(jsvarname != ""):
            self.jsvarname = jsvarname
        else:
            self.jsvarname = os.path.splitext(os.path.basename(self.jsfilename))[0]

        writefile.writesafe(self.jsonTree, self.jsfilename, self.jsvarname )

    def load(self, filename=""):
        if(filename != ""):
            self.filename = filename

        f = open(self.filename, "r")
        self.jsonTree = json.load(f)
        f.close()

    def isEqual(self, objToCompare):
        self.updateJsonTree()
        return writefile.isJsonEqual(self.jsonTree,objToCompare.jsonTree)

    def updateJsonTree(self):
        pass
