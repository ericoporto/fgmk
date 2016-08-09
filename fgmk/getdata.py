# -*- coding: utf-8 -*-
import os.path
import sys

#am I running from pyinstaller ?
if getattr(sys, 'frozen', False):
    #yes, running from pyinstaller
    data_path = os.path.join(os.path.join(sys._MEIPASS),'data')
elif __file__:
    #no, this is the realworld
    data_path = os.path.join(os.path.dirname(__file__),'data')

def path(filename):
    """
    Returns path for filename in data folder, like images needed for the ui.
    """
    return os.path.join(data_path,filename)
