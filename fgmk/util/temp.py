# -*- coding: utf-8 -*-
import tempfile
import shutil

__tempdirs = []

def mkdtemp():
    global __tempdirs
    __tempdirs.append(tempfile.mkdtemp())
    return __tempdirs[-1]

def clean():
    global __tempdirs
    for dir in __tempdirs:
        shutil.rmtree(dir)
