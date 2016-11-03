![Icon](iconTiny.png) fgmk
==========================

[![Join the chat at https://gitter.im/fgmk/Lobby](https://badges.gitter.im/fgmk/Lobby.svg)](https://gitter.im/fgmk/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![PyPI](https://img.shields.io/pypi/v/fgmk.svg?maxAge=3600)](https://pypi.python.org/pypi/fgmk)
[![Github All Releases](https://img.shields.io/github/downloads/ericoporto/fgmk/total.svg?maxAge=3600)](https://github.com/ericoporto/fgmk/releases)
[![PyPI](https://img.shields.io/pypi/pyversions/fgmk.svg?maxAge=86400)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/l/fgmk.svg?maxAge=2592000)](LICENSE)

![Screenshot](screenshot.png)

This is an editor for making 2D RPG games.
Games are composed of plain text files, images and a index.html file containing
[the engine](https://github.com/ericoporto/fgmkJsEngine).

These plain text files are easy to read by software and humans.

[Click here to try a demo game (4MB size). ](https://ericoporto.github.io/fgmkJsEngine/index.html)

Recommended Install and Run
--------------------------

This software is available under [PyPI](https://pypi.python.org/pypi/fgmk)
as **fgmk**. For installing `pip3` in Ubuntu, use `sudo apt install python3-pip`.

    pip3 install fgmk

After install, just open a terminal and type:

    fgmk

### Windows install and run

![Installation on Windows with pip](win_fgmk_install.gif)

In Windows, install Python 3 from [www.python.org](https://www.python.org/downloads/), and then open `cmd.exe` and type (press enter after):

    python -m pip install fgmk

To run, you can type the following in `cmd.exe` or the `run...` prompt

    python -m fgmk


Alternative Installation and Running methods
--------------------------------------------

### From Source Installation

Clone this repository, meet the dependencies and install this with pip3.

    git clone https://github.com/ericoporto/fgmk.git
    cd fgmk
    pip3 install .

### Running from source

Clone this repository, meet the dependencies and type `python3 -m fgmk`

    git clone https://github.com/ericoporto/fgmk.git
    cd fgmk
    python3 -m fgmk

Dependencies
------------

This tool is written using Python 3. Needs `pillow`, `numpy` and `PyQt5` -
you can `apt install python3-pyqt5` and similar (in Ubuntu) or use pip.

If you satisfy all dependencies you don't need to install, and [can run from source](#running-from-source).

Experimental compatibility to python2 (2.7 and on) is added to versions above
0.3.0 .


Documentation
-------------

The docs are available in the website: [ericoporto.github.io/fgmk/](http://ericoporto.github.io/fgmk/).

You can also browse the docs after opening the interface, by clicking in **Help**.

[This is the Quickstart](docs/Markdown/Quickstart/Quickstart.md).

If you wish to edit the docs, they are [here as markdown files](docs/Markdown/index.md).


Contributing
------------

Please take a look to the [`CONTRIBUTING.md`](CONTRIBUTING.md) file.


Author
------

Made by Érico Vieira Porto


License
-------

Distributed under GPLv2 license. See [`LICENSE`](LICENSE) for more information


Known Issues with PyQt5 in Ubuntu
---------------------------------

### Application has no keyboard shortcuts

If instead of using pip3 you are installing dependencies using `apt install`,
the menu will be nicely integrated. Unfortunately, keyboard shortcuts won't
work.

[Details in the bug here](https://bugs.launchpad.net/appmenu-qt5/+bug/1380702)
