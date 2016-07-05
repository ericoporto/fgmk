import os.path
import sys

#am I running from pyinstaller ?
if getattr(sys, 'frozen', False):
    data_path = os.path.join(os.path.join(sys._MEIPASS),'data')
elif __file__:
    data_path = os.path.join(os.path.dirname(__file__),'data')

def path(filename):
    return os.path.join(data_path,filename)
