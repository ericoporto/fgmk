import os
import server
import sys
import json
import TileXtra
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import actionDialog
import TXWdgt
from flowlayout import FlowLayout as FlowLayout
import fifl
import TileCharaset

# moves will be step and face, for all possibilities TileCharaset.facing
# so a radio to select move or face and for buttons - one for each direction.
# also a follow chara option will be added next and a random movement

moves = {"move":TileCharaset.facing , "face":TileCharaset.facing, "random":"move", "follow": "player"}

class CharasFormat(TileCharaset.BaseFormat):
    def __init__( self ):
        TileCharaset.BaseFormat.__init__(self)

        self.new()

    def new(self):
        self.jsonTree = { "Charas": {} }

    def addChara(self, name, charaFile = "", charaSet = "", facing = "down"):

        self.jsonTree["Charas"][name]= {    "charaFile": charaFile, 
                                            "charaSet": charaSet, 
                                            "facing": facing,
                                            "actions":[],
                                            "movements":[]
                                            } 

    def addMovements(self, name, movements):
        self.jsonTree["Charas"][name]["movements"] = movements

    def addActions(self, name, actions):
        self.jsonTree["Charas"][name]["actions"] = actions



class MoveButtons(QWidget):
    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.Grid = QGridLayout(self)

        self.Grid.setHorizontalSpacing(0)
        self.Grid.setVerticalSpacing(0)
        self.Grid.setSpacing(0)
        self.Grid.setContentsMargins(0, 0, 0, 0)

        self.setFixedSize(150, 150)

        self.dirbuttons = []
        self.signal = {}

        for i in TileCharaset.facing:
            self.signal[i] = 'button'+i+'()'
            self.dirbuttons.append(QPushButton(i))
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
        self.emit(SIGNAL(self.signal[direction]))

class MoveItem(QtGui.QListWidgetItem):
    def __init__(self, moveorface, direction = ""):
        super(MoveItem, self).__init__(moveorface+direction)

        if (direction == ""):
            self.direction = moveorface[4:]
            self.moveorface = moveorface[0:4]
        else:
            self.moveorface = moveorface
            self.direction = direction
        movearray = [str(self.moveorface) , str(self.direction)]
        self.setData(Qt.UserRole, movearray)

    def getMarray(self):
        movearray = self.data(Qt.UserRole).toPyObject()
        return [str(movearray[0]),str(movearray[1])]


class MoveWidget(QWidget):
    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.VBox = QVBoxLayout(self)
        self.dirButtons = MoveButtons()
        self.connect(self.dirButtons, SIGNAL('buttonup()'), self.upbclick) 
        self.connect(self.dirButtons, SIGNAL('buttondown()'), self.downbclick) 
        self.connect(self.dirButtons, SIGNAL('buttonleft()'), self.leftbclick) 
        self.connect(self.dirButtons, SIGNAL('buttonright()'), self.rightbclick) 

        self.radiomove = QRadioButton("move")
        self.radioface = QRadioButton("face")
        self.random = QPushButton("random")
        self.follow = QPushButton("follow")


        self.radioface.setToolTip("Face a direction is when a chara looks at certain direction.")
        self.follow.setToolTip("Chara will make one movement or face in the player direction.")
        self.random.setToolTip("Chara will face or move in a random direction, one time.")


        self.random.clicked.connect(self.randombclick)
        self.follow.clicked.connect(self.followbclick)

        self.movList = QListWidget(self)
        self.movList.setDragDropMode(QAbstractItemView.InternalMove)

        self.deselectbutton = QPushButton("deselect")
        self.deletebutton = QPushButton("delete")

        self.deselectbutton.clicked.connect(self.deselectbclick)
        self.deletebutton.clicked.connect(self.deletebclick)

        HBoxB = QHBoxLayout()
        HBoxB.addWidget(self.deselectbutton)
        HBoxB.addWidget(self.deletebutton)

        VBoxR = QVBoxLayout()

        VBoxR.addWidget(self.radiomove)
        VBoxR.addWidget(self.radioface)
        VBoxR.addWidget(self.random)
        VBoxR.addWidget(self.follow)

        HBoxT = QHBoxLayout()
        HBoxT.addWidget(self.dirButtons)
        HBoxT.addLayout(VBoxR)

        self.VBox.addLayout(HBoxT)
        self.VBox.addWidget(self.movList)
        self.VBox.addLayout(HBoxB)

        self.radiomove.toggle()

    def getValue(self):
        movements = []
        for itemIndex in xrange(self.movList.count()):
            itemArray = self.movList.item(itemIndex).getMarray()
            movements.append(itemArray)
            
        return movements

    def deletebclick(self):
        if(self.movList.selectedItems()):
            for item in self.movList.selectedItems():
                itemIndex = self.movList.row(item)
                self.movList.takeItem(itemIndex)
        else:
            for itemIndex in xrange(self.movList.count()):
                self.movList.takeItem(0)


    def deselectbclick(self):
        for i in range(self.movList.count()):
            item = self.movList.item(i)
            self.movList.setItemSelected(item, False)
        self.getValue()

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

class ActionsWidget(QWidget):
    def __init__(self, parent=None, ssettings={}, ischara=False , **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.ssettings = ssettings
        self.parent = parent
        self.ischara = ischara

        self.HBox = QHBoxLayout(self)
        self.HBox.setAlignment(Qt.AlignTop)

        self.labelActionList = QLabel("List of Actions:")
        self.ActionList = QListWidget(self)

        VBoxActionList = QVBoxLayout() 
        VBoxButtons = QVBoxLayout()

        self.addActionButton = QPushButton("Add Action", self)
        self.editActionButton = QPushButton("Edit Action", self)
        self.removeActionButton = QPushButton("Remove Action", self)
        self.deselectActionButton = QPushButton("Deselect Actions", self)

        self.checkboxes = []
        self.checkboxes.append(QCheckBox("on click", self))
        self.checkboxes.append(QCheckBox("on over", self))

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

        self.checkboxes[0].setCheckState(Qt.Checked)
        self.checkboxes[1].setCheckState(Qt.Unchecked)

        for checkbox in self.checkboxes:
            VBoxButtons.addWidget(checkbox)
            checkbox.stateChanged.connect(self.checkboxesChanged)

        self.ActionList.setDragDropMode(QAbstractItemView.InternalMove)

        self.ActionList.itemSelectionChanged.connect(self.enableButtonsBecauseActionList)

        ActionListModel = self.ActionList.model()
        ActionListModel.layoutChanged.connect(self.updateActionFromWidget)

        if(self.ssettings == {} ):
            self.ssettings["gamefolder"] = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),"../Game/"))

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
        indexOfAction = self.ActionList.row(self.ActionList.selectedItems()[0])
        selecteditem = self.ActionList.selectedItems()[0]
        actionParamToEdit = selecteditem.getAction()

        actionToEdit = actionParamToEdit[0]
        paramOfEdit = actionParamToEdit[1]

        paramArrayOfEdit = paramOfEdit.split(';')

        newDialogFromName = getattr(actionDialog, str(actionToEdit))

        self.myActionsDialog = newDialogFromName(self.ssettings["gamefolder"],self,paramArrayOfEdit,True)
        if self.myActionsDialog.exec_() == QtGui.QDialog.Accepted:
            returnActDlg = str(self.myActionsDialog.getValue())

            actionToAdd = [actionToEdit,str(returnActDlg)]

            self.ActionList.takeItem(indexOfAction)
            self.ActionList.insertItem(indexOfAction,TileXtra.actionItem(actionToAdd))                          

    def deselectAction(self):
        for i in range(self.ActionList.count()):
            item = self.ActionList.item(i)
            self.ActionList.setItemSelected(item, False)

    def checkboxesChanged(self, newState):
            checkboxesStates = []
            for checkbox in self.checkboxes:
                checkboxesStates.append(int(checkbox.isChecked()))
            
    def addAction(self):
        self.myActionsWidget = TXWdgt.ActionsWidget(self.ssettings,self,self.ischara)
        if self.myActionsWidget.exec_() == QtGui.QDialog.Accepted:
            actionToAdd = self.myActionsWidget.getValue()
        
            if not self.ActionList.selectedItems():      
                self.ActionList.addItem(TileXtra.actionItem(actionToAdd))
            else:
                indexOfAction = self.ActionList.row(self.ActionList.selectedItems()[0])
                self.ActionList.insertItem(indexOfAction,TileXtra.actionItem(actionToAdd))

    def removeAction(self):

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

    def getAllActions(self):

        allactions = []
        for itemIndex in xrange(self.ActionList.count()):
            allactions.append(self.ActionList.item(itemIndex).getAction())

        return allactions

class CharaItem(QtGui.QListWidgetItem):
    def __init__(self, aname, jsonTree = {}):
        super(CharaItem, self).__init__(aname)

        self.aname = aname
        self.jsonTree = jsonTree

class CharaList(QWidget):
    def __init__(self, parent=None, ssettings={}, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.VBox = QVBoxLayout(self)

        self.charaslist = QListWidget()
        self.charaentry = QLineEdit()
        self.addbutton = QPushButton("add")
        self.delbutton = QPushButton("del")

        self.addbutton.clicked.connect(self.charaslistAddAction)
        self.delbutton.clicked.connect(self.charaslistDelAction)
        self.charaslist.itemSelectionChanged.connect(self.charaslistSelectionChanged)

        HBox = QHBoxLayout()
        HBox.addWidget(self.charaentry)
        HBox.addWidget(self.addbutton)
        HBox.addWidget(self.delbutton)

        self.VBox.addLayout(HBox)
        self.VBox.addWidget(self.charaslist)

    def charaslistAddAction(self):
        charaName = str(self.charaentry.text()).strip()
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
            self.returnvalue = {"name": None, "jsonTree":{}}

        self.emit(SIGNAL("SelectionChanged()"))

    def clear(self):
        self.charaslist.clear()

    def getAll(self):
        items = []
        for itemIndex in xrange(self.charaslist.count()):
            items.append(str(self.charaslist.item(itemIndex).aname),self.charaslist.item(itemIndex).jsonTree)

        return items


class CharaEditor(QWidget):
    def __init__(self, parent=None, ssettings={}, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.layout = QHBoxLayout(self)
        
        self.charalist = CharaList()
        self.csetSelector = TileCharaset.CharasetSelector(self, ssettings)
        self.movement = MoveWidget()

        self.actions = ActionsWidget(parent,ssettings,True)
        self.actions.setAllState(True)
        self.testButton = QPushButton("test", self)
        self.testButton.clicked.connect(self.getAll)

        self.layout.addWidget(self.charalist)
        self.layout.addWidget(self.csetSelector)
        self.layout.addWidget(self.movement)
        self.layout.addWidget(self.actions)
        self.layout.addWidget(self.testButton)
    
    def getAll(self):
        chara = CharasFormat()
        print(self.actions.getAllActions())


if __name__=="__main__":
    from sys import argv, exit

    a=QApplication(argv)
    m=CharaEditor()
    #m=MoveWidget()
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
