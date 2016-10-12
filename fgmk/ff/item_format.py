# -*- coding: utf-8 -*-
import os
from fgmk.ff import base_model

item_categories=['none','consumable','collectible','weapon','armor']
effects_types=['none','hpup','hpdown']
atr_types=['none','st','dx','iq']
default_equipable = False
default_unique = False
default_reusable = False
default_usable = False
default_effect = None
default_statMod = None
default_description = ''
default_icon = None
default_category = None
default_action = None

class base_item:
    def __init__(self,name, equipable=default_equipable,
                            unique=default_unique,
                            reusable=default_reusable,
                            usable=default_usable,
                            effect=default_effect,
                            statMod=default_statMod,
                            description=default_description,
                            icon=default_icon,
                            category=default_category,
                            action=default_action,
                            jsonTree=None):
        normalized_name = str(name)
        normalized_name = normalized_name.title()
        normalized_name = normalized_name.replace(" ", "")

        self.name = name
        self.equipable = equipable
        self.unique = unique
        self.reusable = reusable
        self.usable = usable
        self.effect = effect
        self.statMod = statMod
        self.description = description
        self.icon = icon
        self.category = category
        self.action = action
        if(jsonTree!=None):
            self.loadjsontree(jsonTree)

    def setname(self,name):
        self.name = name

    def setequipable(self, equipable=True):
        self.equipable = equipable

    def setunique(self, unique=True):
        self.unique = unique

    def setreusable(self, reusable=True):
        self.reusable = reusable

    def setusable(self,usable=True):
        self.usable = usable

    def seteffect(self,effect=default_effect):
        self.effect = effect

    def setstatmod(self,statMod=default_statMod):
        self.statMod = statMod

    def setdescription(self, description=default_description):
        self.description = description

    def seticon(self, icon=default_icon):
        self.icon = icon

    def setcategory(self, category=default_category):
        self.category = category

    def setaction(self,action=default_action):
        self.action = action

    def getnormalname(self):
        normalized_name = str(self.name)
        normalized_name = normalized_name.replace(" ", "")
        return normalized_name

    def new(self):
        self.equipable=default_equipable
        self.unique=default_unique
        self.reusable=default_reusable
        self.usable=default_usable
        self.effect=default_effect
        self.statMod=default_statMod
        self.description=default_description
        self.icon=default_icon
        self.category=default_category
        self.action=default_action

    def loadjsontree(self,jsonTree):
        self.new()
        if('name' in jsonTree):
            self.name = jsonTree['name']
        if('equipable' in jsonTree):
            self.equipable = jsonTree['equipable']
        if('usable' in jsonTree):
            self.usable = jsonTree['usable']
        if('unique' in jsonTree):
            self.unique = jsonTree['unique']
        if('reusable' in jsonTree):
            self.reusable = jsonTree['reusable']
        if('effect' in jsonTree):
            self.effect = jsonTree['effect']
        if('statMod' in jsonTree):
            self.statMod = jsonTree['statMod']
        if('description' in jsonTree):
            self.description = jsonTree['description']
        if('icon' in jsonTree):
            self.icon = jsonTree['icon']
        if('category' in jsonTree):
            self.category = jsonTree['category']
        if('action' in jsonTree):
            self.action = jsonTree['action']

    def getjsontree(self):
        jsonTree = {}
        jsonTree['name'] = self.name
        if(self.equipable):
            jsonTree['equipable'] = True
        if(self.usable):
            jsonTree['usable'] = True
        if(self.unique):
            jsonTree['unique'] = True
        if(self.reusable):
            jsonTree['reusable'] = True
        if(self.effect != None):
            jsonTree['effect'] = self.effect
        if(self.statMod != None):
            jsonTree['statMod'] = self.statMod
        if(self.description != False or self.description != ''):
            jsonTree['description'] = self.description
        if(self.icon != None):
            jsonTree['icon'] = self.icon
        if(self.category != None):
            jsonTree['category'] = self.category
        if(self.action != None):
            jsonTree['action'] = self.action

        return jsonTree


class ItemsFormat(base_model.BaseFormat):
    def __init__(self,filename=''):
        base_model.BaseFormat.__init__(self)
        self.filename = filename
        self.new()

    def new(self):
        self.jsonTree = {"Items":{}}
        if os.path.isfile(self.filename):
            self.load()

    def additem(self, item):
        newitem=False
        if(not item.getnormalname() in self.jsonTree['Items']):
            newitem=True

        self.jsonTree['Items'][item.getnormalname()] = item.getjsontree()
        return newitem

    def removebyname(self, name):
        it = base_item(name)
        del self.jsonTree['Items'][it.getnormalname()]
        return self.jsonTree

    def getitems(self):
        return self.jsonTree['Items']

    def getitem(self,item):
        tempjson = self.jsonTree['Items'][item]
        if not 'name' in tempjson:
            tempjson['name']=item

        return tempjson

    def getitemsname(self):
        return sorted(self.jsonTree['Items'])
