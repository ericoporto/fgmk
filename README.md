![Icon](iconTiny.png) fgmk
==========================

![Screenshot](screenshot.png)

This is an editor for making 2D SNES era RPG like games. These RPG should be HTML5 and run on most main browsers.

Everything here is really a work in progress and right now I am still working in getting battles done right.

Installation
------------

You can go the releases and grab the latest .deb, or you can install from source.

### Deb Installation

If you use Ubuntu or Debian, [download from here](https://github.com/ericoporto/fgmk/releases) the latest .deb package.

After you can install using `sudo dpkg -i python3-fgmk_x.y.z.deb`, where x.y.z correspond to the latest version.

For removing, use `sudo apt remove python3-fgmk` .

### From Source Installation

Clone this repository, meet the dependencies and install this with pip3.

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

If you satisfy all dependencies you don't need to install, and [can run from source](#running).

Known Issues with PyQt5 in Ubuntu
---------------------------------
If you choose to install the dependencies using pip3, pyqt5 as is in Ubuntu
requires you to disable the system overlay scroolbars or change the style,
[see bug here](https://bugs.launchpad.net/ubuntu/+source/qt4-x11/+bug/805303).

Also menu shortcuts are not working unless you do a workaround,
[details in the bug here](https://bugs.launchpad.net/appmenu-qt5/+bug/1380702)

Author
------

Made by Érico Vieira Porto

License
-------

Distributed under GPLv2 license. See [`LICENSE`](LICENSE) for more information.
