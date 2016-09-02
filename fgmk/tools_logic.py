from fgmk import tMat
import numpy as np

def tileFill(clickedX, clickedY, fullLayer, changeTToType):
    """
    This function applies bucket fill at point clickedX, clickedY of a ndarray
    fullLayer, and returns a list of the format
    [[pointx, pointy, tileType befor fill, tileType after fill] :]
    """

    changeWhatType = fullLayer[clickedY, clickedX]

    binaryLayer = (fullLayer == changeWhatType).astype(np.int)
    whatChanged = []

    tMat.fill(binaryLayer, len(binaryLayer), len(
        binaryLayer[0]), clickedY, clickedX)

    for i in range(len(binaryLayer)):
        for j in range(len(binaryLayer[0])):
            if binaryLayer[i, j] == 2:
                whatChanged.append(([j, i, changeWhatType, changeTToType]))

    return whatChanged


def tileLine(firstClickedX, firstClickedY, lastClickedX, lastClickedY, fullLayer, changeTToType):
    """
    This function applies bucket fill at point clickedX, clickedY of a ndarray
    fullLayer, and returns a list of the format
    [[pointx, pointy, tileType befor fill, tileType after fill] :]
    """

    whatChanged = []

    thisLinePoints = tMat.line(
        firstClickedX, firstClickedY, lastClickedX, lastClickedY)

    for point in thisLinePoints:
        x = point[0]
        y = point[1]
        whatChanged.append(([x, y, fullLayer[y, x], changeTToType]))

    return whatChanged


def tileRect(firstClickedX, firstClickedY, lastClickedX, lastClickedY, fullLayer, changeTToType):
    """
    This function applies bucket fill at point clickedX, clickedY of a ndarray
    fullLayer, and returns a list of the format
    [[pointx, pointy, tileType befor fill, tileType after fill] :]
    """

    whatChanged = []

    thisRectPoints = tMat.rect(
        firstClickedX, firstClickedY, lastClickedX, lastClickedY)

    for point in thisRectPoints:
        x = point[0]
        y = point[1]
        whatChanged.append(([x, y, fullLayer[y, x], changeTToType]))

    return whatChanged
