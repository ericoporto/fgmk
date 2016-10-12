# -*- coding: utf-8 -*-
from fgmk.ff import base_model

effects_types=['none','hp_down','st_down','dx_down','iq_down','hp_up','st_up','dx_up','iq_up']
skill_targets_types=['an_enemy','all_enemies','a_friend','all_friends']

class Skill:
    def __init__(self,name, basep=0, plus=0, targets=skill_targets_types[0], effect=[], jsonTree=None):
        self.setname(name)
        self.normalname = normalname
        self.basep = basep
        self.plus = plus
        self.targets = targets
        self.effect = effect
        if(jsonTree!=None):
            self.jsonTree = jsonTree
        else:
            self.getjsontree()

     def setname(self, name):
         self.name = name
         normalname = str(name)
         normalname = normalname.title()
         normalname = normalname.replace(" ", "")
         self.normalname = normalname

     def setbasep(self,basep=0):
         self.basep = basep

     def setplus(self,plus=0):
         self.plus = plus

     def settargets(self,targets=skill_targets_types[0]):
         self.targets = targets

     def seteffect(self,effect=[]):
         self.effect = effect

     def new(self):
        self.setbasep()
        self.setplus()
        self.settargets()
        self.seteffect()
        self.getjsontree()

     def loadjsontree(self,jsonTree):
         self.new()
         self.setname(jsonTree['name'] if 'name' in jsonTree)
         self.setbasep(jsonTree['basep'] if 'basep' in jsonTree)
         self.setplus(jsonTree['plus'] if 'plus' in jsonTree)
         self.settargets(jsonTree['targets'] if 'targets' in jsonTree)
         self.seteffect(jsonTree['effect'] if 'effect' in jsonTree)

     def getjsontree(self):
        self.jsonTree = {
                         "name":self.name
                         "basep":self.basep,
                         "plus":self.plus,
                         "targets":self.targets,
                         "effect":self.effect}}
         return self.jsonTree
