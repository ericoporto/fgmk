from fgmk import fifl
import os.path

def test_fifl1():
    expectedleveldir = os.path.join("descriptors", "levels")
    assert fifl.LEVELS == expectedleveldir

def test_fifl2():
    assert fifl.GAMESETTINGS == "init.json"
