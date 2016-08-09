import json
from fgmk import writefile

class BaseFormat:
    def __init__(self, filename=""):
        self.jsonTree = {}
        self.filename = filename

    def new(self):
        self.jsonTree = {}

    def save(self, filename=""):
        if(filename != ""):
            self.filename = filename

        writefile.writesafe(self.jsonTree, self.filename)

    def exportJS(self, filename="", jsvarname = ""):
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
