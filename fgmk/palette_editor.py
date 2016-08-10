import os
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_model, current_project, fifl

class T:
    def __init__(self,id,pos,anim=None):
        self.id=str(id)
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.anim=anim

    def set(self,id,pos,anim=None):
        self.id=str(id)
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.anim=anim

    def setxy(self,x,y):
        self.pos=(x,y)
        self.x=x
        self.y=y

    def setid(self,id):
        self.id=str(id)

    def setanim(anim=None):
        self.anim=anim

class PaletteFormat(base_model.BaseFormat):
    def __init__(self):
        base_model.BaseFormat.__init__(self)
        self.new()

    def new(self):
        self.jsonTree = {'tileImage': '',
                         'tiles': {},
                         'tilesAnimated': {}}

    def addAnimTile(self,tileT):
        self.jsonTree['tilesAnimated'][tileT.id].append([tileT.x,tileT.y])

    def addTile(self,tileT):
        self.jsonTree['tiles'][tileT.id] = [tileT.x,tileT.y]

    def delTile(self,tilen):
        return self.jsonTree['tiles'].pop(str(tilen), None)


class PaletteEditorWidget(QtWidgets.QDialog):
    def __init__(self, parent=None, ssettings={}, **kwargs):
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.pal = PaletteFormat()

        self.mainVBox = QtWidgets.QVBoxLayout(self)
        self.mainVBox.setAlignment(QtCore.Qt.AlignTop)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        self.mainVBox.addWidget(scrollArea)
        insideScrollArea = QtWidgets.QWidget(scrollArea)
        scrollArea.setWidget(insideScrollArea)
        VBox = QtWidgets.QVBoxLayout(insideScrollArea)
        VBox.setAlignment(QtCore.Qt.AlignTop)
        insideScrollArea.setLayout(VBox)

        HBox=QtWidgets.QHBoxLayout()
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.buttonClicked[QtWidgets.QAbstractButton].connect(self.buttonClicked)
        buttons=[{'name':'new' , 'id':0, 'objname':'new_pal' },
                 {'name':'open', 'id':1, 'objname':'open_pal'},
                 {'name':'save', 'id':2, 'objname':'save_pal'},
                 {'name':'del', 'id':3, 'objname':'del_pal'}]
        for b in buttons:
            button = QtWidgets.QPushButton(b['name'])
            button.setObjectName(b['objname'])
            self.buttonGroup.addButton(button, b['id'])
            HBox.addWidget(button)

        VBox.addLayout(HBox)

    def buttonClicked(self, button):
        if  (button.objectName()=='new_pal'):
            self.pal.new()
        elif(button.objectName()=='open_pal'):
            self.openPalette()
        elif(button.objectName()=='save_pal'):
            self.pal.addTile((1,(1,1)))
            self.pal.addTile((2,(1,1)))
            print(self.pal.jsonTree)


    def openPalette(self):
        folder_to_open_to=""
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.LEVELS)

        filename = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        folder_to_open_to,
                        "JSON Palette (*.pal.json);;All Files (*)")[0]
        if(filename!=''):
            self.pal.load(filename)


if __name__ == "__main__":
    from sys import argv, exit

    a = QtWidgets.QApplication(argv)
    m = PaletteEditorWidget()
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
