![Icon](iconTiny.png) fgmk
==========================

This is an editor for making 2D SNES era RPG like games. The games are composed
of plain text files, images and a index.html file containing [the engine](https://github.com/ericoporto/fgmkJsEngine).

![Screenshot](screenshot.png)

The goal is that these plain text files should be easy to be read by humans and
software.

Installation
------------

### From pip Installation

This software is available under [PyPI](https://pypi.python.org/pypi/fgmk)
as **fgmk**.

    pip3 install fgmk

### Deb Installation

If you use Ubuntu or Debian, [download from here](https://github.com/ericoporto/fgmk/releases)
the latest `.deb` package.

After you can install using `sudo dpkg -i python3-fgmk_x.y.z.deb`, where
x.y.z correspond to the latest version.

For removing, use `sudo apt remove python3-fgmk` .

### From Source Installation

Clone this repository, meet the dependencies and install this with pip3.

    git clone https://github.com/ericoporto/fgmk.git
    cd fgmk
    pip3 install .

Running
-------

You can run this from the directory you cloned by typing `./run.py` (without
installing)or after install, just open a terminal and type:

    fgmk


Dependencies
------------

This tool is written using Python 3. Needs `pillow`, `numpy` and `PyQt5` -
you can `apt install python3-pyqt5` and similar (in Ubuntu) or use pip3.

If you satisfy all dependencies you don't need to install, and [can run from source](#running).

Known Issues with PyQt5 in Ubuntu
---------------------------------

### Application crashes Ubuntu

If you choose to install the dependencies using pip3, pyqt5 as is in Ubuntu
requires you to disable the system overlay scroolbars or change the style,
[see bug here](https://bugs.launchpad.net/ubuntu/+source/qt4-x11/+bug/805303).

Doing so will have the menu not integrated with the top bar, but keyboard
shortcuts will work.

### Application has no keyboard shortcuts

If instead of using pip3 you are installing dependencies using `apt install`,
the menu will be nicely integrated. Unfortunately, keyboard shortcuts won't
work.

[Details in the bug here](https://bugs.launchpad.net/appmenu-qt5/+bug/1380702)

Author
------

Made by Érico Vieira Porto

License
-------

Distributed under GPLv2 license. See [`LICENSE`](LICENSE) for more information.
