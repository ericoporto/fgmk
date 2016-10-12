# -*- coding: utf-8 -*-
from fgmk.ff import base_model

class CharasFormat(base_model.BaseFormat):
    def __init__( self ):
        #super().__init__()
        base_model.BaseFormat.__init__(self)

        self.new()

    def new(self):
        self.jsonTree = { "Charas": {} }

    def addChara(self, name, charaset = "", actions = {"type":[1,0],"list":[]}, movements=[], properties={"nocolision":0, "pushable":False}):

        self.jsonTree["Charas"][name]= {    "charaset": charaset,
                                            "actions":actions,
                                            "movements":movements,
                                            "properties":properties
                                            }

    def addMovements(self, name, movements):
        self.jsonTree["Charas"][name]["movements"] = movements

    def addActions(self, name, actions):
        self.jsonTree["Charas"][name]["actions"] = actions

    def getCharaset(self,name):
        return self.jsonTree["Charas"][name]["charaset"]
