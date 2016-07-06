import os
from numbers import Number
from fgmk import printerror

try:
  basestring
except NameError:
  basestring = (str, bytes)

def writesafe(data, fname, varname=None):
    tempfile = fname+'~'
    try:
        f = open(tempfile, 'w+')
        try:
            if(varname==None):
                fwriteKeyVals(data, f)
            else:
                f.write("var " + self.levelName + "= {\n")
                fwriteKeyValsJS(data,f)
                f.write("};")
        finally:
            f.flush()
            os.fsync(f.fileno())
            f.close()
            os.replace(tempfile,fname)
    except:
        printerror.printe('error when opening file')



def fwriteKeyVals(data, f, indent=0):
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
                f.write(" [\"\"]")

    elif isinstance(data, dict):
        f.write("\n" + "    " * indent + "{")
        for k, v in data.items():
            f.write("\n" + "    " * indent + "\"" + k + "\"" + ": ")
            fwriteKeyVals(v, f, indent + 1)
            if(list(data)[-1] != k):
                f.write(",")
        f.write("\n" + "    " * indent + "}")
    elif isinstance(data, bool):
        f.write("%3d" % data)
    elif isinstance(data, basestring):
        f.write("\"" + data + "\"")
    else:
        f.write( str(data) )


def fwriteKeyValsJS(data, f, indent=0):
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

        
