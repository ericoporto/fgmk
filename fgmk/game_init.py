# -*- coding: utf-8 -*-
import json
import os.path
from os import listdir
from fgmk import fifl, current_project
from fgmk.ff import write_file

def getLevelPathFromInitFile(gamefolder, levelname):
    initFile = openInitFile(gamefolder)
    return os.path.join(str(gamefolder), fifl.LEVELS, initFile['LevelsList'][str(levelname)])


def openInitFile(gamefolder):
    fname = os.path.join(str(gamefolder), fifl.DESCRIPTORS, fifl.GAMESETTINGS)

    if os.path.isfile(fname):
        f = open(fname, "r")
        initFileJsonTree = json.load(f)
        f.close()
        return initFileJsonTree
    else:
        return None

def playerInitCharaset():
    initJsonTree = getInitFile()
    return initJsonTree['Player']['charaSet']


def saveInitFile(gamefolder, initFileJsonTree):
    f = open(os.path.join(str(gamefolder),
                          fifl.DESCRIPTORS, fifl.GAMESETTINGS), "w")
    initFileJsonTree = json.dump(initFileJsonTree, f, indent=4, sort_keys=True)
    f.close()
    return initFileJsonTree


def getInitFile():
    gamefolder = os.path.join(current_project.settings["gamefolder"])
    if os.path.isdir(gamefolder):
        return openInitFile(gamefolder)
    else:
        return {}

def getMusicList():
    initJsonTree = getInitFile()
    if("MusicList" in initJsonTree):
        return initJsonTree["MusicList"]
    else:
        return dict()

def getSoundList():
    initJsonTree = getInitFile()
    if("SoundList" in initJsonTree):
        return initJsonTree["SoundList"]
    else:
        return dict()

def regenerateInit():
    initFileJsonTree = getInitFile()
    needupdate = False

    levelJsonTree = regenerateLevelList(initFileJsonTree)
    if(levelJsonTree == None):
        #regress to before json tree
        levelJsonTree = initFileJsonTree
    else:
        needupdate = True

    musicJsonTree = regenerateMusicList(levelJsonTree)
    if(musicJsonTree == None):
        #regress to before json tree
        musicJsonTree = levelJsonTree
    else:
        needupdate = True

    soundJsonTree = regenerateSoundList(musicJsonTree)
    if(soundJsonTree == None):
        #regress to before json tree
        soundJsonTree = musicJsonTree
    else:
        needupdate = True

    if(needupdate):
        gamefolder = os.path.join(current_project.settings["gamefolder"])
        saveInitFile(gamefolder, soundJsonTree)
        return True

    return False

def regenerateSoundList(initFileJsonTree):
    if 'SoundList' not in initFileJsonTree:
        return None

    gamefolder = os.path.join(current_project.settings["gamefolder"])

    if(initFileJsonTree != None):
        sound = os.path.join(gamefolder, fifl.AUDIO)
        mp3list = [f for f in listdir(sound) if os.path.isfile(os.path.join(sound, f)) and f.endswith(".mp3")]
        ogglist = [f for f in listdir(sound) if os.path.isfile(os.path.join(sound, f)) and f.endswith(".ogg")]
        wavlist = [f for f in listdir(sound) if os.path.isfile(os.path.join(sound, f)) and f.endswith(".wav")]
        originalSoundList = initFileJsonTree["SoundList"]

        filelist = mp3list + ogglist + wavlist
        SoundList = {}
        for file in filelist:
            [filewoext, ext ] = os.path.splitext(file)
            if hasattr(SoundList, filewoext):
                SoundList[filewoext][ext[1:]] = file
            else:
                SoundList[filewoext] = {}
                SoundList[filewoext][ext[1:]] = file

        if(write_file.isJsonEqual(SoundList,originalSoundList) == False):
            initFileJsonTree["SoundList"] = []
            initFileJsonTree["SoundList"] = SoundList
            return initFileJsonTree

    return None

def regenerateMusicList(initFileJsonTree):
    if 'MusicList' not in initFileJsonTree:
        return None

    gamefolder = os.path.join(current_project.settings["gamefolder"])

    if(initFileJsonTree != None):
        songs = os.path.join(gamefolder, fifl.MUSIC)
        mp3list = [f for f in listdir(songs) if os.path.isfile(os.path.join(songs, f)) and f.endswith(".mp3")]
        ogglist = [f for f in listdir(songs) if os.path.isfile(os.path.join(songs, f)) and f.endswith(".ogg")]
        wavlist = [f for f in listdir(songs) if os.path.isfile(os.path.join(songs, f)) and f.endswith(".wav")]
        originalMusicList = initFileJsonTree["MusicList"]

        filelist = mp3list + ogglist + wavlist
        MusicList = {}
        for file in filelist:
            [filewoext, ext ] = os.path.splitext(file)
            if hasattr(MusicList, filewoext):
                MusicList[filewoext][ext[1:]] = file
            else:
                MusicList[filewoext] = {}
                MusicList[filewoext][ext[1:]] = file

        if(write_file.isJsonEqual(MusicList,originalMusicList) == False):
            initFileJsonTree["MusicList"] = []
            initFileJsonTree["MusicList"] = MusicList
            return initFileJsonTree

    return None

def regenerateLevelList(initFileJsonTree):
    if 'LevelsList' not in initFileJsonTree:
        return None

    gamefolder = os.path.join(current_project.settings["gamefolder"])

    if(initFileJsonTree != None):
        levels = os.path.join(gamefolder, fifl.LEVELS)
        filelist = [f for f in listdir(levels) if os.path.isfile(os.path.join(levels, f)) and f.endswith(".map.json")]
        originalLevelList = initFileJsonTree["LevelsList"]

        LevelsList = {}
        for file in filelist:
            filewoext = file.split(os.extsep, 1)[0]
            LevelsList[filewoext] = file

        unmatched_maps = set(LevelsList.items()) ^ set(originalLevelList.items())

        if(len(unmatched_maps)!=0):
            initFileJsonTree["LevelsList"] = []
            initFileJsonTree["LevelsList"] = LevelsList
            return initFileJsonTree

    return None

def getAllVariables():
    # charas.json -> ['Charas'][charanames]['actions']['list']
    # *.map.json -> ['Level']['eventsActions'][events]
    return 'allvariables'
