#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import environ as environ
from sys import exit, argv
from time import time, sleep
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt
from fgmk import Editor


def main(args=None):
    """The main routine."""

    environ["LIBOVERLAY_SCROLLBAR"] = "0"
    if args is None:
        args = argv[1:]

    a = QApplication(args)
    start = time()
    splash_pix = Editor.Icon()
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    while time() - start < 1:
        sleep(0.001)
        a.processEvents()
    mw = Editor.MainWindow(args)
    a.processEvents()
    mw.show()
    splash.finish(mw)
    mw.raise_()
    mw.afterInit()
    exit(a.exec_())

if __name__ == "__main__":
    environ["LIBOVERLAY_SCROLLBAR"] = "0"
    main()
