import numpy as np
from numbers import Number

def mnZeros(m, n):
    return [[0 for x in range(m)] for x in range(n)]

def fill( data, xsize, ysize, x_start, y_start):

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
    dx = abs(x1 - x0) +1   # distance to travel in X
    dy = abs(y1 - y0) +1   # distance to travel in Y

    rectComplete = []

    if x0 < x1:
        ix = 1           # x will increase at each step
    else:
        ix = -1          # x will decrease at each step

    if y0 < y1:
        iy = 1           # y will increase at each step
    else:
        iy = -1          # y will decrease at each step

    x=x0
    for i in range(dx):
        y = y0
        for j in range(dy):
            rectComplete.append(([x, y]))
            y += iy

        x += ix

    return rectComplete

def fwriteKeyVals(data, f, indent=0):
    if isinstance(data, list):
        try:
            gotdata = isinstance(data[0], list)
        except IndexError:
            gotdata = False

        if gotdata:

            f.write( "\n" + "    " * indent + "[" )
            for i in range(len(data) ):
                if ( i == 0):
                    f.write( "[" )
                else:
                    f.write( "    " * indent + " [" )
                for j in range(len(data[0])):
                    if isinstance( data[i][j], Number):
                        f.write( "%3d" %  data[i][j] )
                    elif isinstance( data[i][j], bool):
                        f.write( "%3d" %  data[i][j] )
                    elif isinstance( data[i][j], basestring):
                        dataListLf = data[i][j].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n'+line

                        f.write( "\"" + dataToWrite + "\"")
                    else:
                        f.write(  dataToWrite )
                    f.write( "," ) if j != len(data[0])-1 else (f.write( "]," ) if i != len(data)-1 else f.write( "]" ))
                f.write( "\n" ) if i != len(data)-1 else f.write( "]" )
        else:
            try:
                gotdata = data[0]
            except IndexError:
                gotdata = 'False'

            if gotdata is not 'False':
                f.write( " [" )
                for i in range(len(data) ):
                    if isinstance(data[i], Number):
                        f.write( "%3d" % data[i] )
                    elif isinstance( data[i], bool):
                        f.write( "%3d" %  data[i][j] )
                    elif isinstance( data[i], basestring):
                        dataListLf = data[i].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n'+line

                        f.write( "\"" + dataToWrite + "\"")
                    else:
                        f.write( dataToWrite)
                    f.write( "," ) if i != len(data)-1 else f.write( "]" )
            else:
                f.write( " [\"\"]" )

    elif isinstance(data, dict):
        f.write( "\n" + "    " * indent + "{" )
        for k, v in data.iteritems():
            f.write( "\n" + "    " * indent + "\"" + k + "\"" + ": ")
            fwriteKeyVals(v, f, indent + 1)
            if( data.keys()[-1] != k):
                 f.write( "," )
        f.write( "\n" + "    " * indent + "}" )
    elif isinstance( data, bool):
        f.write( "%3d" %  data )
    else:
        f.write("\"" + data + "\"")

def fwriteKeyValsJS(data, f, indent=0):
    if isinstance(data, list):
        try:
            gotdata = isinstance(data[0], list)
        except IndexError:
            gotdata = False

        if gotdata:

            f.write( "\n" + "    " * indent + "[" )
            for i in range(len(data) ):
                if ( i == 0):
                    f.write( "[" )
                else:
                    f.write( "    " * indent + " [" )
                for j in range(len(data[0])):
                    if isinstance( data[i][j], Number):
                        f.write( "%3d" %  data[i][j] )
                    else:
                        dataListLf = data[i][j].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n'+line

                        f.write( "\"" + dataToWrite + "\"")

                    f.write( "," ) if j != len(data[0])-1 else (f.write( "]," ) if i != len(data)-1 else f.write( "]" ))
                f.write( "\n" ) if i != len(data)-1 else f.write( "]" )
        else:
            try:
                gotdata = data[0]
            except IndexError:
                gotdata = 'False'

            if gotdata is not 'False':
                f.write( " [" )
                for i in range(len(data) ):
                    if isinstance(data[i], Number):
                        f.write( "%3d" % data[i] )
                    else:
                        dataListLf = data[i].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n'+line

                        f.write( "\"" + dataToWrite + "\"")
                    f.write( "," ) if i != len(data)-1 else f.write( "]" )
            else:
                f.write( " [\"\"]" )

    elif isinstance(data, dict):
        if(indent):
            f.write( "\n" + "    " * indent + "{" )

        for k, v in data.iteritems():
            f.write( "\n" + "    " * indent + "" + k + "" + ": ")
            fwriteKeyValsJS(v, f, indent + 1)
            if( data.keys()[-1] != k):
                 f.write( "," )

        if(indent):
            f.write( "\n" + "    " * indent + "}" )

    else:
        f.write("\"" + data + "\"")

from PIL import Image

def alpha_composite(dst, src):
    '''
    Return the alpha composite of src and dst.

    Parameters:
    src -- PIL RGBA Image object
    dst -- PIL RGBA Image object

    The algorithm comes from http://en.wikipedia.org/wiki/Alpha_compositing
    '''
    # http://stackoverflow.com/a/3375291/190597
    # http://stackoverflow.com/a/9166671/190597
    src = np.asarray(src)
    dst = np.asarray(dst)
    out = np.empty(src.shape, dtype = 'float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha]/255.0
    dst_a = dst[alpha]/255.0
    out[alpha] = src_a+dst_a*(1-src_a)
    old_setting = np.seterr(invalid = 'ignore')
    out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
    np.seterr(**old_setting)
    out[alpha] *= 255
    np.clip(out,0,255)
    # astype('uint8') maps np.nan (and np.inf) to 0
    out = out.astype('uint8')
    out = Image.fromarray(out, 'RGBA')
    return out
