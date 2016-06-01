![Icon](iconTiny.png) fangamk
=============================

Maker
-----

![Screenshot](screenshot.png)

This is the editor. It uses pyqt to render a rather nice view.

Currently the embedded tester only works in Linux, but you can test in your
default browser after saving by pressing f5.


Running in Linux:
-----------------

Right now I am porting from Python 2.7 to Python 3 and from Qt4 to Qt5.

Needs `pillow`, `numpy` and `PyQt5` - you can `apt install python3-pyqt5` and
similar (in Ubuntu) or use pip.

In ubuntu 14.04 I had to install also `sudo apt install python3-pyqt5.qtwebkit`.

Then cd to the correspondent folder and use

    python3 Editor.py
