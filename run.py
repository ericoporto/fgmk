#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import path as ospath
from sys import path as syspath

if ospath.isdir(ospath.join(".","src")) and ospath.isfile(
        ospath.join(".","setup.py")):
    syspath.append(ospath.realpath("src"))
    syspath.append(ospath.realpath("src/fgmk"))

import fgmk.__main__ as application

application.main()
