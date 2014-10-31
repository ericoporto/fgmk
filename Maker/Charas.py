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


class CharaEditor(QWidget):
    def __init__(self, parent=None, ssettings={}, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.HBox = QHBoxLayout(self)
        
        self.csetSelector = TileCharaset.CharasetSelector(self, ssettings)
        self.HBox.addWidget(self.csetSelector)

        self.actions = ActionsWidget(parent,ssettings,True)
        self.actions.setAllState(True)
        self.HBox.addWidget(self.actions)

        self.testButton = QPushButton("test", self)
        self.testButton.clicked.connect(self.getAllActions)
        self.HBox.addWidget(self.testButton)
    
    def getAllActions(self):
        print(self.actions.getAllActions())


if __name__=="__main__":
    from sys import argv, exit

    a=QApplication(argv)
    m=CharaEditor()
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
