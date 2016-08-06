from fgmk import __title__, __version__, __copyright__, __license__
from fgmk import temp, getdata, current_project, game_init
import os
import tarfile

credits = """
Higly based in Tsubasa's Redo.
Inspired in Enterbrain's RPG Maker 2000.
Thanks Nintendo for making the SNES.
"""

aboutstr = __title__ + " v" + __version__ + "\n\n" + \
    __copyright__ + "\n\n" + __license__ + "\n\nCredits:\n" + credits

def load_example():
    exampleProject = {"name": "example", "baseFolder": temp.mkdtemp()}
    current_projectectPath = os.path.join(
        str(exampleProject["baseFolder"]), str(exampleProject["name"]))
    current_project.settings["basefolder"] = str(exampleProject["baseFolder"])
    current_project.settings["gamefolder"] = current_projectectPath
    current_project.settings["gamename"] = str(exampleProject["name"])
    os.mkdir(current_projectectPath)
    tar = tarfile.open(getdata.path("example.tar.gz"))
    tar.extractall(current_projectectPath)
    tar.close()
    initfile = game_init.openInitFile(current_project.settings["gamefolder"])
    levellist = initfile["LevelsList"]
    startlevel = initfile['World']['initLevel']
    levelfile = levellist[startlevel]
    return levelfile
