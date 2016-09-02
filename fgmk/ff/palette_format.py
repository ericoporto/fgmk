# -*- coding: utf-8 -*-
import os
from fgmk.ff import base_model
from fgmk import fifl

"""
This module deals with the palette format, which is how are palette files saved
and loaded.

The class T describes a single tile in a palette, and is used in the palette
editor to describe a tile to the PaletteFormat class, so it can receive a tile
through the addtile and addanimtile functions. It inherits BaseFormat.load and
BaseFormat.save to deal with opening and saving the files.
"""

#T(id,(x,y))
class T:
    def __init__(self,id,pos,anim=0):
        self.set(id,pos,anim)

    def set(self,id,pos,anim=0):
        self.id=str(id)
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        if(anim==0):
            anim=0
        self.anim=anim

    def setxy(self,x,y):
        self.pos=(x,y)
        self.x=x
        self.y=y

    def setid(self,id):
        self.id=str(id)

    def setanim(anim=0):
        self.anim=anim

class PaletteFormat(base_model.BaseFormat):
    def __init__(self):
        base_model.BaseFormat.__init__(self)
        self.new()

    def getfilename(self):
        return self.filename

    def new(self):
        self.animtiles = {}
        self.jsonTree = {'tileImage': 'img/tile.png',
                         'tiles': {'0':[0,0]},
                         'tilesAnimated': {}}

    def loadjsondump(self,jsonTree):
        self.jsonTree = jsonTree
        for tile in self.jsonTree['tilesAnimated']:
            self.animtiles[str(tile)] = {}
            for i in range(len(self.jsonTree['tilesAnimated'][tile])):
                self.animtiles[tile][str(i)]=self.jsonTree['tilesAnimated'][tile][i]

    def load(self,palfile):
        base_model.BaseFormat.load(self,palfile)
        for tile in self.jsonTree['tilesAnimated']:
            self.animtiles[str(tile)] = {}
            for i in range(len(self.jsonTree['tilesAnimated'][tile])):
                self.animtiles[tile][str(i)]=self.jsonTree['tilesAnimated'][tile][i]


    def imgloag(self,imgfile):
        self.jsonTree['tileImage'] = os.path.join(fifl.IMG,os.path.basename(imgfile))
        return self.jsonTree['tileImage']

    def getimg(self):
        return self.jsonTree['tileImage']

    def gettiles(self):
        return self.jsonTree['tiles']

    def gettile(self, x, y):
        tiles = self.jsonTree['tiles']
        tanims = self.jsonTree['tilesAnimated']

        for ttype in tiles:
            tile = tiles[ttype]
            if(x==tile[0] and y==tile[1]):
                if ttype in tanims:
                    return T(ttype,(x,y), 1)
                else:
                    return T(ttype,(x,y))

        for ttype in tanims:
            animtile = tanims[ttype]
            if(len(animtile)>0):
                for i in range(len(animtile)):
                    tile = animtile[i]
                    if(x==tile[0] and y==tile[1]):
                        return T(ttype,(x,y),i+1)

        return T(-1,(x,y))

    def delalltiles(self):
        self.animtiles = {}
        self.jsonTree['tiles'] = {}
        self.jsonTree['tilesAnimated'] = {}

    def addanimtile(self,tileT):
        if tileT.id in self.animtiles:
            self.animtiles[tileT.id][tileT.anim] = [tileT.x,tileT.y]
        else:
            self.animtiles[tileT.id]={}
            self.animtiles[tileT.id][tileT.anim] = [tileT.x,tileT.y]
        animdict = self.animtiles[tileT.id]
        animlist = [animdict[k] for k in sorted(animdict)]
        self.jsonTree['tilesAnimated'][tileT.id] = animlist

    def addtile(self,tileT):
        if(tileT.anim > 0):
            self.addanimtile(tileT)
        self.jsonTree['tiles'][tileT.id] = [tileT.x,tileT.y]
        return self.jsonTree['tiles'][tileT.id]
