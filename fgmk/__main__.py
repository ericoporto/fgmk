#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import environ as environ
from sys import exit, argv
from time import time, sleep
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QSettings
from fgmk import Editor
from fgmk import __title__, __version__, __copyright__, __license__
import argparse

def main():
    """The main routine."""
    environ["LIBOVERLAY_SCROLLBAR"] = "0"
    parser = argparse.ArgumentParser(
                prog=__title__,
                description=__title__ + ' is a 2d RPG game maker.',
                epilog=__copyright__ + ", " + __license__ +".")
    parser.add_argument('-v', '--version', action='store_true', default=False, help='get software version.')
    parser.add_argument('-c', '--clean', action='store_true', default=False, help='cleans software settings.')
    parser.add_argument('mapfile', nargs='?', default='check_no_map', help='a single .map.json file')
    args = parser.parse_args()

    if args.clean == True:
        settings = QSettings("FGMK", "fgmkEditor")
        for key in settings.allKeys():
            settings.remove(key) #guarantee to eliminate all
        settings.sync() #writes to disk
        exit()

    if args.version == True:
        print(__title__ + "  v " + __version__ )
        exit()

    a = QApplication([])
    start = time()
    splash_pix = Editor.Icon()
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    while time() - start < 1:
        sleep(0.001)
        a.processEvents()

    mw_arg=[]
    if 'mapfile' in args:
        mw_arg = [args.mapfile]

    mw = Editor.MainWindow(mw_arg)
    a.processEvents()
    mw.show()
    splash.finish(mw)
    mw.raise_()
    mw.afterInit()
    exit(a.exec_())

if __name__ == "__main__":
    main()
