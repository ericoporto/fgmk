from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import Charas, current_project

class CommandAddChara(QtWidgets.QUndoCommand):
    """
    Class for a single chara insert operation.
    This class operates in the visible map
    widget and the map (that has the jsontree), having redo (which is also the
    do action) and undo capabilities.
    """
    def __init__(self, description, pCharasPalWidget,  position=(0, 0), chara=None,):
        super().__init__(description)

        self.pCharasPalWidget = pCharasPalWidget
        self.position = position
        if (chara == None):
            chara = self.pCharasPalWidget.myCharaSelector.getSelected()
        self.chara = chara

    def redo(self):
        self.pCharasPalWidget.addCharaAction(self.position,self.chara, True)

    def undo(self):
        self.pCharasPalWidget.deletePosition(self.position, True)


class CommandDelChara(QtWidgets.QUndoCommand):
    """
    Class for a single chara delete operation.
    This class operates in the visible map
    widget and the map (that has the jsontree), having redo (which is also the
    do action) and undo capabilities.
    """
    def __init__(self, description, pCharasPalWidget,  position, chara):
        super().__init__(description)

        self.pCharasPalWidget = pCharasPalWidget
        self.position = position
        self.chara = chara

    def redo(self):
        self.pCharasPalWidget.deletePosition(self.position, True)

    def undo(self):
        self.pCharasPalWidget.addCharaAction(self.position,self.chara, True)



class CharasPalWidget(QtWidgets.QWidget):
    def __init__(self, mapWdgt, pMap, parent=None, charaInstance=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.mapWdgt = mapWdgt
        self.pMap = pMap
        self.parent = parent

        self.vbox = QtWidgets.QVBoxLayout(self)

        self.charaslist = []
        self.myCharaSelector = Charas.CharaSelector(self, current_project.settings)
        self.vbox.addWidget(self.myCharaSelector)
        self.show()

    def reinit(self):
        for charaplaced in self.charaslist:
            charaplaced[2].stop()
            self.mapWdgt.Grid.removeWidget(charaplaced[2])
            charaplaced[2].deleteLater()

        self.myCharaSelector.update()
        self.charaslist = []

        charalist = self.pMap.getCharaList()
        if(charalist == [''] or not charalist):
            return

        for char in charalist:
            self.addCharaAction((char[1], char[2]), char[0], False)

    def addCharaAction(self, position=(0, 0), chara=None, onmap=True):
        if (chara == None):
            chara = self.myCharaSelector.getSelected()

        if (chara != None):
            scale = self.mapWdgt.myScale / 2.0
            if(self.positionEmpty(position)):
                item = Charas.MiniCharaTile(
                    None, current_project.settings, chara, (0, 0), scale)
                item.rightClicked.connect(self.autodelete)
                self.mapWdgt.Grid.addWidget(item, position[1], position[0])
                if(onmap):
                    self.pMap.insertChara(position[0], position[1], chara)
                self.charaslist.append((chara, position, item))

    def autodelete(self):
        item = self.sender()
        for charaplaced in self.charaslist:
            if(charaplaced[2] == item):
                command = CommandDelChara("deleted chara", self, (charaplaced[1][0], charaplaced[1][1]),charaplaced[0])
                self.parent.commandToStack(command)
                break


    def getCharasList(self):
        charaslist = []
        for charaplaced in self.charaslist:
            charaslist.append(charaplaced[0], charaplaced[
                              1][0], charaplaced[1][1])

        return charaslist

    def deletePosition(self, position=(0, 0), onmap=False):
        for charaplaced in self.charaslist:
            if(charaplaced[1] == position):
                charaplaced[2].stop()
                if(onmap):
                    self.pMap.removeChara(charaplaced[1][0], charaplaced[1][1])
                self.mapWdgt.Grid.removeWidget(charaplaced[2])
                charaplaced[2].deleteLater()
                break

        self.charaslist.remove(charaplaced)


    def positionEmpty(self, position):
        for charaplaced in self.charaslist:
            if(charaplaced[1] == position):
                return False

        else:
            return True

    def getSelected(self):
        return self.myCharaSelector.getSelected()
