![Icon](iconTiny.png) fgmk
==========================

![Screenshot](screenshot.png)

This is an editor for making 2D SNES era RPG like games. These RPG should be HTML5 and run on most main browsers.

Everything here is really a working in progress and right now I am still working in getting battles done right.

Installation
------------

This can be run from the folder you cloned if you satisfy dependencies, if you don't, you can install it and all dependencies with pip3.

    git clone https://github.com/ericoporto/fgmk.git
    cd fgmk
    pip3 install .

Running
-------

You can run this from the directory you cloned by typing `./fgmk`or after install, just open a terminal and type

    fgmk


Dependencies
------------

This tool is written using Python 3. Needs `pillow`, `numpy` and `PyQt5` - you can `apt install python3-pyqt5` and
similar (in Ubuntu) or use pip3. 

In ubuntu 14.04 I had to install also `sudo apt install python3-pyqt5.qtwebkit`.
