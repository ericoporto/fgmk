# -*- coding: utf-8 -*-
import os
import sys
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import actions_wdgt, action_dialog, fifl, tile_charaset, base_model

from fgmk.flowlayout import FlowLayout as FlowLayout

# moves will be step and face, for all possibilities tile_charaset.facing
# so a radio to select move or face and for buttons - one for each direction.
# also a follow chara option will be added next and a random movement

moves = {"move":tile_charaset.facing , "face":tile_charaset.facing, "random":"move", "follow": "player"}

class CharasFormat(base_model.BaseFormat):
    def __init__( self ):
        #super().__init__()
        base_model.BaseFormat.__init__(self)

        self.new()

    def new(self):
        self.jsonTree = { "Charas": {} }

    def addChara(self, name, charaset = "", actions = {"type":[1,0],"list":[]}, movements=[], properties={"nocolision":0}):

        self.jsonTree["Charas"][name]= {    "charaset": charaset,
                                            "actions":actions,
                                            "movements":movements,
                                            "properties":properties
                                            }

    def addMovements(self, name, movements):
        self.jsonTree["Charas"][name]["movements"] = movements

    def addActions(self, name, actions):
        self.jsonTree["Charas"][name]["actions"] = actions

    def getCharaset(self,name):
        return self.jsonTree["Charas"][name]["charaset"]



class MoveButtons(QtWidgets.QWidget):
    buttonup = QtCore.pyqtSignal()
    buttondown = QtCore.pyqtSignal()
    buttonleft = QtCore.pyqtSignal()
    buttonright = QtCore.pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.Grid = QtWidgets.QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.setFixedSize(150, 150)

        self.dirbuttons = []
        self.signal = {}
        self.signal["up"] = self.buttonup
        self.signal["down"] = self.buttondown
        self.signal["left"] = self.buttonleft
        self.signal["right"] = self.buttonright

        for i in tile_charaset.facing:
            self.dirbuttons.append(QtWidgets.QPushButton(i))
            self.dirbuttons[-1].setObjectName(i)
            self.dirbuttons[-1].setFixedSize(50, 50)
            self.dirbuttons[-1].clicked.connect(self.bclicked)
            if i == "up":
                self.Grid.addWidget(self.dirbuttons[-1], 0, 1)
            if i == "down":
                self.Grid.addWidget(self.dirbuttons[-1], 2, 1)
            if i == "left":
                self.Grid.addWidget(self.dirbuttons[-1], 1, 0)
            if i == "right":
                self.Grid.addWidget(self.dirbuttons[-1], 1, 2)

    def bclicked(self):
        direction = str(self.sender().objectName())
        self.signal[direction].emit()

class MoveItem(QtWidgets.QListWidgetItem):
    def __init__(self, moveorface, direction = ""):
        #super().__init__(moveorface+direction)
        QtWidgets.QListWidgetItem.__init__(self, moveorface+direction)

        if (direction == ""):
            self.direction = moveorface[4:]
            self.moveorface = moveorface[0:4]
        else:
            self.moveorface = moveorface
            self.direction = direction
        movearray = [str(self.moveorface) , str(self.direction)]
        self.setData(QtCore.Qt.UserRole, movearray)

    def getMarray(self):
        #movearray = self.data(Qt.UserRole).toPyObject() #this was python2
        #python3 doesn't need toPyObject (and doesn't work with it)
        movearray = self.data(QtCore.Qt.UserRole)
        return [str(movearray[0]),str(movearray[1])]

class PropertiesWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.nocolision = QtWidgets.QCheckBox("igone colision")
        self.nocolision.setToolTip("This makes the object ignore the colision map.")
        self.nocolision.setCheckState(QtCore.Qt.Unchecked)

        self.propertys =  {}
        self.propertys['nocolision']=self.nocolision

        for key in self.propertys:
            self.VBox.addWidget(self.propertys[key])

        self.clear()

    def setList(self,listToSet):
        for propertyy in listToSet:
            if(propertyy == 'nocolision'):
                if(listToSet[propertyy]==0 or listToSet[propertyy]==False):
                    self.propertys[propertyy].setCheckState(QtCore.Qt.Unchecked)
                else:
                    self.propertys[propertyy].setCheckState(QtCore.Qt.Checked)

    def clear(self):
        for propertyy in self.propertys:
            if(propertyy == 'nocolision'):
                self.propertys[propertyy].setCheckState(QtCore.Qt.Unchecked)

    def getValue(self):
        properties = {}
        for key in self.propertys:
            properties[key] = self.propertys[key].isChecked()

        return properties


class MoveWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.dirButtons = MoveButtons()
        self.dirButtons.buttonup.connect(self.upbclick)
        self.dirButtons.buttondown.connect(self.downbclick)
        self.dirButtons.buttonleft.connect(self.leftbclick)
        self.dirButtons.buttonright.connect(self.rightbclick)

        self.radiomove = QtWidgets.QRadioButton("move")
        self.radioface = QtWidgets.QRadioButton("face")
        self.random = QtWidgets.QPushButton("random")
        self.follow = QtWidgets.QPushButton("follow")


        self.radioface.setToolTip("Face a direction is when a chara looks at certain direction.")
        self.follow.setToolTip("Chara will make one movement or face in the player direction.")
        self.random.setToolTip("Chara will face or move in a random direction, one time.")


        self.random.clicked.connect(self.randombclick)
        self.follow.clicked.connect(self.followbclick)

        self.movList = QtWidgets.QListWidget(self)
        self.movList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.deselectbutton = QtWidgets.QPushButton("deselect")
        self.deletebutton = QtWidgets.QPushButton("delete")

        self.deselectbutton.clicked.connect(self.deselectbclick)
        self.deletebutton.clicked.connect(self.deletebclick)

        HBoxB = QtWidgets.QHBoxLayout()
        HBoxB.addWidget(self.deselectbutton)
        HBoxB.addWidget(self.deletebutton)

        VBoxR = QtWidgets.QVBoxLayout()

        VBoxR.addWidget(self.radiomove)
        VBoxR.addWidget(self.radioface)
        VBoxR.addWidget(self.random)
        VBoxR.addWidget(self.follow)

        HBoxT = QtWidgets.QHBoxLayout()
        HBoxT.addWidget(self.dirButtons)
        HBoxT.addLayout(VBoxR)

        self.VBox.addLayout(HBoxT)
        self.VBox.addWidget(self.movList)
        self.VBox.addLayout(HBoxB)

        self.radiomove.toggle()

    def setList(self,listToSet):
        self.movList.clear()
        for move in listToSet:
            print(move)
            self.movList.addItem(MoveItem(move[0],move[1]))

    def clear(self):
        self.movList.clear()

    def getValue(self):
        movements = []
        for itemIndex in range(self.movList.count()):
            itemArray = self.movList.item(itemIndex).getMarray()
            movements.append(itemArray)

        return movements

    def deletebclick(self):
        if(self.movList.selectedItems()):
            for item in self.movList.selectedItems():
                itemIndex = self.movList.row(item)
                self.movList.takeItem(itemIndex)
        else:
            for itemIndex in range(self.movList.count()):
                self.movList.takeItem(0)


    def deselectbclick(self):
        for i in range(self.movList.count()):
            item = self.movList.item(i)
            self.movList.setItemSelected(item, False)
        #self.getValue()

    def randombclick(self):
        if(self.radioface.isChecked()):
            self.movList.addItem(MoveItem("facerandom"))
        else:
            self.movList.addItem(MoveItem("moverandom"))

    def followbclick(self):
        if(self.radioface.isChecked()):
            self.movList.addItem(MoveItem("facefollow"))
        else:
            self.movList.addItem(MoveItem("movefollow"))

    def upbclick(self):
        if(self.radioface.isChecked()):
            self.movList.addItem(MoveItem("faceup"))
        else:
            self.movList.addItem(MoveItem("moveup"))

    def downbclick(self):
        if(self.radioface.isChecked()):
            self.movList.addItem(MoveItem("facedown"))
        else:
            self.movList.addItem(MoveItem("movedown"))

    def leftbclick(self):
        if(self.radioface.isChecked()):
            self.movList.addItem(MoveItem("faceleft"))
        else:
            self.movList.addItem(MoveItem("moveleft"))

    def rightbclick(self):
        if(self.radioface.isChecked()):
            self.movList.addItem(MoveItem("faceright"))
        else:
            self.movList.addItem(MoveItem("moveright"))

class ActionsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, ssettings={}, ischara=False , **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.ssettings = ssettings
        self.parent = parent
        self.ischara = ischara

        self.HBox = QtWidgets.QHBoxLayout(self)
        self.HBox.setAlignment(QtCore.Qt.AlignTop)

        self.labelActionList = QtWidgets.QLabel("List of Actions:")
        self.ActionList = QtWidgets.QListWidget(self)

        VBoxActionList = QtWidgets.QVBoxLayout()
        VBoxButtons = QtWidgets.QVBoxLayout()

        self.addActionButton = QtWidgets.QPushButton("Add Action", self)
        self.editActionButton = QtWidgets.QPushButton("Edit Action", self)
        self.removeActionButton = QtWidgets.QPushButton("Remove Action", self)
        self.deselectActionButton = QtWidgets.QPushButton("Deselect Actions", self)

        self.checkboxes = []
        self.checkboxes.append(QtWidgets.QCheckBox("on click", self))
        self.checkboxes.append(QtWidgets.QCheckBox("on over", self))

        self.addActionButton.clicked.connect(self.addAction)
        self.editActionButton.clicked.connect(self.editAction)
        self.removeActionButton.clicked.connect(self.removeAction)
        self.deselectActionButton.clicked.connect(self.deselectAction)

        self.HBox.addLayout(VBoxActionList)
        self.HBox.addLayout(VBoxButtons)

        VBoxActionList.addWidget(self.labelActionList)
        VBoxActionList.addWidget(self.ActionList)

        VBoxButtons.addWidget(self.addActionButton)
        VBoxButtons.addWidget(self.editActionButton)
        VBoxButtons.addWidget(self.removeActionButton)
        VBoxButtons.addWidget(self.deselectActionButton)

        self.checkboxes[0].setCheckState(QtCore.Qt.Checked)
        self.checkboxes[1].setCheckState(QtCore.Qt.Unchecked)

        for checkbox in self.checkboxes:
            VBoxButtons.addWidget(checkbox)

        self.ActionList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.ActionList.itemSelectionChanged.connect(self.enableButtonsBecauseActionList)

        ActionListModel = self.ActionList.model()
        ActionListModel.layoutChanged.connect(self.updateActionFromWidget)

    def setList(self,actionToSet):
        atype = actionToSet['type']
        for i in range(len(atype)):
            if(atype[i]):
                self.checkboxes[i].setCheckState(QtCore.Qt.Checked)
            else:
                self.checkboxes[i].setCheckState(QtCore.Qt.Unchecked)

        listToSet = actionToSet['list']
        self.ActionList.clear()
        for action in listToSet:
            self.ActionList.addItem(actions_wdgt.actionItem(action))

    def clear(self):
        self.ActionList.clear()

    def setAllState(self, state):
        self.addActionButton.setEnabled(state)
        self.removeActionButton.setEnabled(state)
        self.ActionList.setEnabled(state)
        self.labelActionList.setEnabled(state)
        self.deselectActionButton.setEnabled(state)
        self.editActionButton.setEnabled(state)
        self.enableButtonsBecauseActionList()

    def updateActionFromWidget(self):
        i = 0
        while i < self.ActionList.count():
            item = self.ActionList.item(i)
            actionToAdd = item.getAction()
            i += 1

    def editAction(self):
        if(self.ssettings == {} ):
            return

        indexOfAction = self.ActionList.row(self.ActionList.selectedItems()[0])
        selecteditem = self.ActionList.selectedItems()[0]
        actionParamToEdit = selecteditem.getAction()

        actionToEdit = actionParamToEdit[0]
        paramOfEdit = actionParamToEdit[1]

        paramArrayOfEdit = paramOfEdit.split(';')

        newDialogFromName = getattr(action_dialog, str(actionToEdit))

        self.myActionsDialog = newDialogFromName(self.ssettings["gamefolder"],self,paramArrayOfEdit,True)
        if self.myActionsDialog.exec_() == QtWidgets.QDialog.Accepted:
            returnActDlg = str(self.myActionsDialog.getValue())

            actionToAdd = [actionToEdit,str(returnActDlg)]

            self.ActionList.takeItem(indexOfAction)
            self.ActionList.insertItem(indexOfAction,actions_wdgt.actionItem(actionToAdd))

    def deselectAction(self):
        for i in range(self.ActionList.count()):
            item = self.ActionList.item(i)
            self.ActionList.setItemSelected(item, False)

    def addAction(self):
        if(self.ssettings == {} ):
            return

        self.myActionsWidget = actions_wdgt.ActionsWidget(self.ssettings,self,self.ischara)
        if self.myActionsWidget.exec_() == QtWidgets.QDialog.Accepted:
            actionToAdd = self.myActionsWidget.getValue()

            if not self.ActionList.selectedItems():
                self.ActionList.addItem(actions_wdgt.actionItem(actionToAdd))
            else:
                indexOfAction = self.ActionList.row(self.ActionList.selectedItems()[0])
                self.ActionList.insertItem(indexOfAction,actions_wdgt.actionItem(actionToAdd))

    def removeAction(self):
        if(self.ssettings == {} ):
            return

        for item in self.ActionList.selectedItems():
            itemIndex = self.ActionList.row(item)
            self.ActionList.takeItem(itemIndex)

    def enableButtonsBecauseActionList(self):
        enable = True
        if (self.ActionList.currentItem() is None):
            enable = False
        else:
            if (self.ActionList.currentItem().isSelected() == False):
                enable = False

        if (enable):
            self.removeActionButton.setEnabled(True)
            self.deselectActionButton.setEnabled(True)
            self.editActionButton.setEnabled(True)
        else:
            self.removeActionButton.setEnabled(False)
            self.editActionButton.setEnabled(False)
            self.deselectActionButton.setEnabled(False)

    def getValue(self):

        allactions = []
        for itemIndex in range(self.ActionList.count()):
            allactions.append(self.ActionList.item(itemIndex).getAction())

        onclick = self.checkboxes[0].isChecked()
        onover = self.checkboxes[1].isChecked()

        actiontype = [onclick,onover]

        returnvalue = {'list':allactions, 'type':actiontype }

        return returnvalue

class CharaItem(QtWidgets.QListWidgetItem):
    def __init__(self, aname, jsonTree = {}):
        #super().__init__(aname)
        QtWidgets.QListWidgetItem.__init__(self, aname)

        if(jsonTree == {}):
             jsonTree = {'movements': [], 'actions': {'type': [], 'list': []}, 'charaset': ''}

        self.aname = aname
        self.jsonTree = jsonTree

class CharaList(QtWidgets.QWidget):
    SelectionChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None, ssettings={}, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.VBox = QtWidgets.QVBoxLayout(self)

        self.charaslist = QtWidgets.QListWidget()
        self.charaentry = QtWidgets.QLineEdit()
        self.addbutton = QtWidgets.QPushButton("add")
        self.delbutton = QtWidgets.QPushButton("del")

        self.addbutton.clicked.connect(self.charaslistAddAction)
        self.delbutton.clicked.connect(self.charaslistDelAction)
        self.charaslist.itemSelectionChanged.connect(self.charaslistSelectionChanged)
        self.charaentry.returnPressed.connect(self.charaslistAddAction)

        HBox = QtWidgets.QHBoxLayout()
        HBox.addWidget(self.charaentry)
        HBox.addWidget(self.addbutton)
        HBox.addWidget(self.delbutton)

        self.VBox.addLayout(HBox)
        self.VBox.addWidget(self.charaslist)
        self.charaslistSelectionChanged()

    def charaslistAddAction(self):
        charaName = str(self.charaentry.text()).strip()
        if (len(charaName)>0):
            for itemIndex in range(self.charaslist.count()):
                if (str(self.charaslist.item(itemIndex).aname) == charaName):
                    return

            self.charaslist.addItem(CharaItem(charaName))

    def charaslistDelAction(self):
        if (len(self.charaslist.selectedItems())>0):
            for item in self.charaslist.selectedItems():
                itemIndex = self.charaslist.row(item)
                self.charaslist.takeItem(itemIndex)

    def charaslistSelectionChanged(self):
        if (len(self.charaslist.selectedItems())>0):
            jsonTree = self.charaslist.selectedItems()[0].jsonTree
            name = self.charaslist.selectedItems()[0].aname
            self.returnvalue = {"name": name, "jsonTree":jsonTree}
        else:
            self.returnvalue = {'name': None,  'jsonTree':{'charaset':"",'actions':{},'movements':[],'properties':{}}}

        self.SelectionChanged.emit()

    def setSelected(self,jsonTree):
        if (len(self.charaslist.selectedItems())>0):
            self.charaslist.selectedItems()[0].jsonTree = jsonTree

    def setItem(self,itemTree):
        for itemIndex in range(self.charaslist.count()):
            if (str(self.charaslist.item(itemIndex).aname) == itemTree["name"]):
                self.charaslist.item(itemIndex).jsonTree = itemTree["jsonTree"]


    def clear(self):
        self.charaslist.clear()

    def getCharas(self):
        self.charaslistSelectionChanged()
        charas = CharasFormat()
        for itemIndex in range(self.charaslist.count()):
            charaname = str(self.charaslist.item(itemIndex).aname)
            jt = self.charaslist.item(itemIndex).jsonTree
            print(jt)
            charas.addChara(charaname,jt["charaset"],jt["actions"],jt["movements"],jt["properties"])

        return charas

    def deselect(self):
        for i in range(self.charaslist.count()):
            item = self.charaslist.item(i)
            self.charaslist.setItemSelected(item, False)

    def setList(self,dictToSet):
        self.charaslist.clear()
        for chara in dictToSet:
            charaName = chara
            jsonTree = dictToSet[chara]
            self.charaslist.addItem(CharaItem(charaName,jsonTree))

class CharaSelector(QtWidgets.QWidget):
    charaClicked = QtCore.pyqtSignal()
    charaDoubleClicked = QtCore.pyqtSignal()
    def __init__(self, parent=None, ssettings={}, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.ssettings = ssettings

        self.layout = QtWidgets.QHBoxLayout(self)
        self.csetprev = tile_charaset.CharasetPreviewer(self,ssettings)
        self.charaqlist = QtWidgets.QListWidget()

        self.charaqlist.itemSelectionChanged.connect(self.selectionChanged)
        self.charaqlist.itemClicked.connect(self.emitclicked)
        self.charaqlist.itemDoubleClicked.connect(self.emitdoubleclicked)

        self.layout.addWidget(self.csetprev)
        self.layout.addWidget(self.charaqlist)
    def emitdoubleclicked(self):
        self.charaDoubleClicked.emit()

    def emitclicked(self):
        self.charaClicked.emit()

    def update(self):
        if "gamefolder" in self.ssettings:
            if (self.ssettings["gamefolder"] != ""):
                filetoopen = os.path.join(self.ssettings["gamefolder"],fifl.DESCRIPTORS,fifl.CHARAS)
                self.__Open(filetoopen)

                self.csetprev.update()

        if self.charaqlist.count() > 0:
            self.charaqlist.setCurrentRow(0)

    def setList(self,dictToSet):
        self.charaqlist.clear()
        for chara in dictToSet:
            charaName = chara
            jsonTree = dictToSet[chara]
            self.charaqlist.addItem(CharaItem(charaName,jsonTree))

    def __Open(self,charafile = None):
        if(charafile == None):
            charafile = self.charafile

        self.charafile = charafile
        charas = CharasFormat()
        charas.load(charafile)
        self.setList(charas.jsonTree["Charas"])

    def selectionChanged(self):
        if(self.charaqlist.selectedItems()):
            charaset = str(self.charaqlist.selectedItems()[0].jsonTree["charaset"])
            self.csetprev.select(charaset)

    def getSelected(self):
        if(self.charaqlist.selectedItems()):
            charaname = str(self.charaqlist.selectedItems()[0].aname)
            return charaname
        else:
            return None


class MiniCharaTile(QtWidgets.QWidget):
    def __init__(self, parent=None, ssettings={}, chara="", position=(0,0), scale=1, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.chara = chara
        self.position = position

        if "gamefolder" in ssettings:
            filetoopen = os.path.join(ssettings["gamefolder"],fifl.DESCRIPTORS,fifl.CHARAS)
            charas = self.__Open(filetoopen)
            charaset = charas.getCharaset(chara)

            self.csetprev = tile_charaset.CharasetPreviewer(self,ssettings,None,scale)
            self.csetprev.select(charaset)
            self.whsize = self.csetprev.whsize
            self.setFixedSize(self.whsize)

        else:
            return False

        self.setToolTip(chara)

    clicked = QtCore.pyqtSignal()
    rightClicked = QtCore.pyqtSignal()

    def stop(self):
        self.csetprev.stop()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()

    def __Open(self,charafile = None):
        if(charafile == None):
            charafile = self.charafile

        self.charafile = charafile
        charas = CharasFormat()
        charas.load(charafile)
        return charas



class CharaEditor(QtWidgets.QDialog):
    def __init__(self, parent=None, ssettings={}, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.charalist = CharaList()
        self.csetSelector = tile_charaset.CharasetSelector(self, ssettings)
        self.movement = MoveWidget()
        self.properties = PropertiesWidget()

        self.actions = ActionsWidget(parent,ssettings,True)
        self.actions.setAllState(True)
        self.reopen = QtWidgets.QPushButton("Reopen", self)
        self.reopen.clicked.connect(self.reopenfile)
        self.save = QtWidgets.QPushButton("Save", self)
        self.save.clicked.connect(self.savefile)

        HBoxRS = QtWidgets.QHBoxLayout()
        HBoxRS.addWidget(self.reopen)
        HBoxRS.addWidget(self.save)

        VBox = QtWidgets.QVBoxLayout()
        VBox.addWidget(self.charalist)
        VBox.addLayout(HBoxRS)
        VBox.addWidget(self.properties)

        self.layout.addLayout(VBox)
        self.layout.addWidget(self.csetSelector)
        self.layout.addWidget(self.movement)
        self.layout.addWidget(self.actions)

        self.charalist.SelectionChanged.connect(self.charaSelectionChanged)

        self.oldSelection = self.charalist.returnvalue

        if "gamefolder" in ssettings:
            filetoopen = os.path.join(ssettings["gamefolder"],fifl.DESCRIPTORS,fifl.CHARAS)
            self.__Open(filetoopen)

    def reopenfile(self):
        self.__Open()

    def savefile(self):
        self.__Save()


    def __Open(self,charafile = None):
        if(charafile == None):
            charafile = self.charafile

        self.charafile = charafile
        charas = CharasFormat()
        charas.load(charafile)
        self.charalist.setList(charas.jsonTree["Charas"])

    def __Save(self,charafile = None):
        if(charafile == None):
            charafile = self.charafile

        charas = self.charalist.getCharas()
        charas.save(charafile)


    def getAll(self):
        charas = {}
        charas = self.charalist.getCharas()
        print(charas.jsonTree)


    def charaSelectionChanged(self):
        newSelection = self.charalist.returnvalue

        if(self.oldSelection['name'] == None):
            self.oldSelection['name'] = newSelection['name']
        else:
            charaset = self.csetSelector.getValue()
            movements = self.movement.getValue()
            actions = self.actions.getValue()
            properties = self.properties.getValue()
            self.oldSelection["jsonTree"] = { "charaset":charaset,"movements":movements,"actions":actions, "properties":properties }
            self.charalist.setItem(self.oldSelection)

        if(newSelection['jsonTree'] == {}):
            self.movement.clear()
            self.actions.clear()
            self.csetSelector.reset()
            self.properties.clear()
        else:
            self.csetSelector.select(newSelection['jsonTree']['charaset'])
            self.movement.setList(newSelection['jsonTree']['movements'])
            self.actions.setList(newSelection['jsonTree']['actions'])
            self.properties.setList(newSelection['jsonTree']['properties'])

        self.oldSelection = newSelection


if __name__=="__main__":
    from sys import argv, exit

    a=QtWidgets.QApplication(argv)
    #m=CharaEditor()
    #m=MoveWidget()
    #m=CharaSelector()
    m=MiniCharaTile(None,{"gamefolder":"basegame"},"WeirdGuy")
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
