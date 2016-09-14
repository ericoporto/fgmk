# -*- coding: utf-8 -*-
import os
import json
import sys
import re
from numbers import Number
from fgmk.util import print_error

try:
  basestring
except NameError:
  basestring = (str, bytes)

#from here: http://code.activestate.com/recipes/579097-safely-and-atomically-write-to-a-file/
try:
    osreplace = os.replace  # Python 3.3 and better.
except AttributeError:
    if sys.platform == 'win32':
        # FIXME This is definitely not atomic!
        # But it's how (for example) Mercurial does it, as of 2016-03-23
        # https://selenic.com/repo/hg/file/tip/mercurial/windows.py
        def osreplace(source, destination):
            assert sys.platform == 'win32'
            try:
                os.rename(source, dest)
            except OSError as err:
                if err.winerr != 183:
                    raise
                os.remove(dest)
                os.rename(source, dest)
    else:
        # Atomic on POSIX. Not sure about Cygwin, OS/2 or others.
        osreplace = os.rename


def ordered(obj):
    """
    Recursive order a unordered dict. Use for comparing dicts.
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    else:
        return obj

def isJsonEqual(jsonA,jsonB):
    """
    Check if two json tree (dicts) are equal.

    Args:
        jsonA dict: a dict or jsontree.
        jsonB dict: another dict or jsontree.

    Returns:
        bool. True if equal, False if not.
    """
    return ordered(jsonA) == ordered(jsonB)


def writesafe(data, fname, varname=None):
    """
    Write a dict to a file as Json safely.

    Write the content of a dict to a file with name fname~ and if it's content
    is equal to data, renames fname~ to just fname. This function can optionaly
    generate a JS object if varname is not None.

    Args:
        data dict: a dict you wish to write to a file.
        fname str: the file name.
    """
    tempfile = fname+'~'
    try:
        f = open(tempfile, 'w+')
        try:
            if(varname==None):
                fwriteKeyVals(data, f)
            else:
                f.write("var " + varname + "= {\n")
                fwriteKeyValsJS(data,f)
                f.write("};")
        finally:
            f.flush()
            os.fsync(f.fileno())
            f.close()
            if(varname==None):
                try:
                    f = open(tempfile, 'r')
                    tempjsontree = json.load(f)
                    if isJsonEqual(data,tempjsontree):
                        f.close()
                        osreplace(tempfile,fname)
                    else:
                        print_error.printe("written file not equal to data")
                except:
                    print_error.printe("error when checking file")
            else:
                osreplace(tempfile,fname)
    except:
        print_error.printe('error when opening file')



def natural_sort_list(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)


def fwriteKeyVals(data, f, indent=0):
    """
    Recursively write a JSON from dict data to an opened file f.

    Two main differences from regular json writer:
     1 - a 2d matrixes will be printed in square fashion.
     [[ 0, 0],
      [ 0, 0]]

      instead of

     [[0,
       0],
       [0,
       0]]

      or [[0,0],[0,0]]

      2 - dicts should be ordered.
          This should allow placing a json file under version control and have
          sane diffs.
    """

    if isinstance(data, list):
        try:
            gotdata = isinstance(data[0], list)
        except IndexError:
            gotdata = False

        if gotdata:

            f.write("\n" + "    " * indent + "[")
            for i in range(len(data)):
                if (i == 0):
                    f.write("[")
                else:
                    f.write("    " * indent + " [")
                for j in range(len(data[0])):
                    if isinstance(data[i][j], Number):
                        f.write("%3d" % data[i][j])
                    elif isinstance(data[i][j], bool):
                        f.write("%3d" % data[i][j])
                    elif isinstance(data[i][j], basestring):
                        dataListLf = data[i][j].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n' + line

                        f.write("\"" + dataToWrite + "\"")
                    else:
                        f.write(dataToWrite)
                    f.write(",") if j != len(
                        data[0]) - 1 else (f.write("],") if i != len(data) - 1 else f.write("]"))
                f.write("\n") if i != len(data) - 1 else f.write("]")
        else:
            try:
                gotdata = data[0]
            except IndexError:
                gotdata = 'False'

            if gotdata is not 'False':
                f.write(" [")
                for i in range(len(data)):
                    if isinstance(data[i], Number):
                        f.write("%3d" % data[i])
                    elif isinstance(data[i], bool):
                        f.write("%3d" % data[i][j])
                    elif isinstance(data[i], basestring):
                        dataListLf = data[i].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n' + line

                        f.write("\"" + dataToWrite + "\"")
                    else:
                        f.write(dataToWrite)
                    f.write(",") if i != len(data) - 1 else f.write("]")
            else:
                f.write(" []")

    elif isinstance(data, dict):
        f.write("\n" + "    " * indent + "{")
        sorted_data = [ (k,data[k]) for k in natural_sort_list(data) ]
        for k, v in sorted_data:
            f.write("\n" + "    " * indent + "\"" + k + "\"" + ": ")
            fwriteKeyVals(v, f, indent + 1)
            if(sorted_data[-1][0] != k):
                f.write(",")
        f.write("\n" + "    " * indent + "}")
    elif isinstance(data, bool):
        if(data):
            f.write("true")
        else:
            f.write("false")
    elif isinstance(data, basestring):
        f.write("\"" + data + "\"")
    else:
        f.write( str(data) )


def fwriteKeyValsJS(data, f, indent=0):
    """
    Recursively write a JS object from dict data to an opened file f.
    """

    if isinstance(data, list):
        try:
            gotdata = isinstance(data[0], list)
        except IndexError:
            gotdata = False

        if gotdata:

            f.write("\n" + "    " * indent + "[")
            for i in range(len(data)):
                if (i == 0):
                    f.write("[")
                else:
                    f.write("    " * indent + " [")
                for j in range(len(data[0])):
                    if isinstance(data[i][j], Number):
                        f.write("%3d" % data[i][j])
                    else:
                        dataListLf = data[i][j].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n' + line

                        f.write("\"" + dataToWrite + "\"")

                    f.write(",") if j != len(
                        data[0]) - 1 else (f.write("],") if i != len(data) - 1 else f.write("]"))
                f.write("\n") if i != len(data) - 1 else f.write("]")
        else:
            try:
                gotdata = data[0]
            except IndexError:
                gotdata = 'False'

            if gotdata is not 'False':
                f.write(" [")
                for i in range(len(data)):
                    if isinstance(data[i], Number):
                        f.write("%3d" % data[i])
                    else:
                        dataListLf = data[i].split("\n")
                        dataToWrite = dataListLf[0]
                        for line in dataListLf[1:]:
                            dataToWrite += '\\n' + line

                        f.write("\"" + dataToWrite + "\"")
                    f.write(",") if i != len(data) - 1 else f.write("]")
            else:
                f.write(" [\"\"]")

    elif isinstance(data, dict):
        if(indent):
            f.write("\n" + "    " * indent + "{")

        for k, v in data.items():
            f.write("\n" + "    " * indent + "" + k + "" + ": ")
            fwriteKeyValsJS(v, f, indent + 1)
            if(list(data)[-1] != k):
                f.write(",")

        if(indent):
            f.write("\n" + "    " * indent + "}")

    else:
        f.write("\"" + data + "\"")
