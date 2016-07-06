from fgmk import tMat
import numpy as np

def test_divideRoundUp1():
    assert tMat.divideRoundUp(5,2) == 3

def test_divideRoundUp2():
    assert tMat.divideRoundUp(8,2) == 4

def test_mnZeros():
    assert tMat.mnZeros(3,2) == [[0, 0, 0],[0, 0, 0]]

def test_fill():
    """
    data will be a matrix with some points 1 and some 0.
    if I target a group of connected points 1, I expect
    them to become 2 after applying fill. Non connected
    points must remain 1. The matrix rdata contains the
    expected result.

    """
    data = np.array([[0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 1, 0],
                     [0, 1, 1, 1, 1, 0],
                     [0, 1, 0, 0, 0, 0],
                     [0, 1, 1, 1, 0, 1],
                     [0, 0, 1, 1, 0, 1],
                     [0, 0, 0, 0, 0, 0]]).astype(np.int)

    rdat = np.array([[0, 0, 0, 0, 0, 0],
                     [0, 0, 2, 2, 2, 0],
                     [0, 0, 0, 0, 2, 0],
                     [0, 2, 2, 2, 2, 0],
                     [0, 2, 0, 0, 0, 0],
                     [0, 2, 2, 2, 0, 1],
                     [0, 0, 2, 2, 0, 1],
                     [0, 0, 0, 0, 0, 0]]).astype(np.int)

    tMat.fill(data, 8, 6, 1, 2)

    np.testing.assert_array_equal(data, rdat)

def test_line1():
    """
    I want a line like below
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 1 1 1 1 0 0
    0 0 0 0 0 0 0
    """

    line = tMat.line(1, 2, 4, 2)
    expectedline = [[1, 2],[2, 2],[3,2],[4,2]]
    assert line == expectedline

def test_line2():
    """
    I want a line like below
    0 1 0 0 0 0 0
    0 1 1 0 0 0 0
    0 0 1 1 0 0 0
    0 0 0 1 1 0 0
    0 0 0 0 1 1 0
    """

    line = tMat.line(1, 0, 5, 4)
    expectedline = [[1, 0],[1,1],[2, 1],[2,2],[3,2],[3,3],[4,3],[4,4],[5,4]]
    assert line == expectedline

def test_rect():
    """
    I want a rectangle like below
    0 0 0 0 0 0 0
    0 0 1 1 1 1 0
    0 0 1 1 1 1 0
    0 0 1 1 1 1 0
    0 0 0 0 0 0 0
    """

    rect = tMat.rect(2,1, 5,3)
    expectedrect = [[2,1],[3,1],[4,1],[5,1],
                    [2,2],[3,2],[4,2],[5,2],
                    [2,3],[3,3],[4,3],[5,3]]
