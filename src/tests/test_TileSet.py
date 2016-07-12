import os
from fgmk import TileSet
from PIL import ImageChops

def gettestdata(filename):
    return os.path.join(os.path.dirname(__file__),filename)

def test_emptyTile():
    assert TileSet.emptyTile

def test_TileSet_length():
    mytileset = TileSet.TileSet(gettestdata('testTiles.png'))
    assert len(mytileset.tileset) == 3

def test_TileSet_boxsize():
    mytileset = TileSet.TileSet(gettestdata('testTiles.png'))
    assert mytileset.boxsize == 32

def test_TileSet_checkEmptyTile():
    """
    The first 32x32 box in the tileset is empty.
    So we will compare with the emptyTile in tileset.
    The difference should be empty because images are equal
    """

    mytileset = TileSet.TileSet(gettestdata('testTiles.png'))
    expected_empty_tile = mytileset.tileset[0][0]

    empty_tile = TileSet.emptyTile

    diff = ImageChops.difference(empty_tile, expected_empty_tile)

    assert diff.getbbox() == None

def test_TileSet_checkFilledTile():
    """
    The second 32x32 box in the tileset contains a tile ocuppying 32x32 space.
    So we will compare with the emptyTile in tileset.
    The difference should be a 32x32 box starting from zero.
    """

    mytileset = TileSet.TileSet(gettestdata('testTiles.png'))
    expected_filled_tile = mytileset.tileset[1][0]

    empty_tile = TileSet.emptyTile

    diff = ImageChops.difference(empty_tile, expected_filled_tile)

    assert diff.getbbox() == (0,0,32,32)
