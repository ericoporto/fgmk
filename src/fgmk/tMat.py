import numpy as np


def divideRoundUp(a, b):
    return int((a / b) + (a % b > 0))


def mnZeros(m, n):
    return [[0 for x in range(m)] for x in range(n)]


def fill(data, xsize, ysize, x_start, y_start):

    stack = [(x_start, y_start)]

    while stack:
        column, row = stack[0]
        stack = stack[1:]

        if data[column, row] == 1:
            data[column, row] = 2
            if column > 0:
                stack.append((column - 1, row))
            if column < (xsize - 1):
                stack.append((column + 1, row))
            if row > 0:
                stack.append((column, row - 1))
            if row < (ysize - 1):
                stack.append((column, row + 1))


def line(x0, y0, x1, y1):
    dx = abs(x1 - x0)    # distance to travel in X
    dy = abs(y1 - y0)    # distance to travel in Y

    lineComplete = []

    if x0 < x1:
        ix = 1           # x will increase at each step
    else:
        ix = -1          # x will decrease at each step

    if y0 < y1:
        iy = 1           # y will increase at each step
    else:
        iy = -1          # y will decrease at each step

    e = 0                # Current error

    for i in range(dx + dy):
        lineComplete.append(([x0, y0]))
        e1 = e + dy
        e2 = e - dx
        if abs(e1) < abs(e2):
            # Error will be smaller moving on X
            x0 += ix
            e = e1
        else:
            # Error will be smaller moving on Y
            y0 += iy
            e = e2

    lineComplete.append(([x1, y1]))

    return lineComplete


def rect(x0, y0, x1, y1):
    dx = abs(x1 - x0) + 1   # distance to travel in X
    dy = abs(y1 - y0) + 1   # distance to travel in Y

    rectComplete = []

    if x0 < x1:
        ix = 1           # x will increase at each step
    else:
        ix = -1          # x will decrease at each step

    if y0 < y1:
        iy = 1           # y will increase at each step
    else:
        iy = -1          # y will decrease at each step

    x = x0
    for i in range(dx):
        y = y0
        for j in range(dy):
            rectComplete.append(([x, y]))
            y += iy

        x += ix

    return rectComplete
