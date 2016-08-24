# -*- coding: utf-8 -*-
import json
from PyQt5 import QtCore, QtWidgets
from fgmk import action_dialog, getdata

class actionItem(QtWidgets.QListWidgetItem):
    def __init__(self, actionAndParameter):
        #super().__init__(str(actionAndParameter))
        QtWidgets.QListWidgetItem.__init__(self, str(actionAndParameter))
        self.setText = str(actionAndParameter)
        self.setData(QtCore.Qt.UserRole, actionAndParameter)

    def getAction(self):
        actionAndParameterReturn = self.data(QtCore.Qt.UserRole)
        action = str(actionAndParameterReturn[0])
        parameter = str(actionAndParameterReturn[1])
        return [action, parameter]

class ActionsWidget(QtWidgets.QDialog):
    def __init__(self, psSettings, parent=None, ischaras=False, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.psSettings = psSettings
        self.ischaras = ischaras

        self.mainVBox = QtWidgets.QVBoxLayout(self)
        self.mainVBox.setAlignment(QtCore.Qt.AlignTop)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.mainVBox.addWidget(self.scrollArea)

        self.insideScrollArea = QtWidgets.QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.insideScrollArea)

        self.VBox = QtWidgets.QVBoxLayout(self.insideScrollArea)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)
        self.insideScrollArea.setLayout(self.VBox)

        filepath = getdata.path('actionsList.json')
        f = open(filepath, "r")
        e = json.load(f)
        f.close()

        self.parent = parent
        self.actionButton = []

        for action in e["actionOrder"]:
            self.actionButton.append(QtWidgets.QPushButton(action, self))
            self.actionButton[-1].setMaximumWidth(330)
            self.actionButton[-1].setMinimumWidth(80)
            self.actionButton[-1].setMinimumHeight(24)
            self.VBox.addWidget(self.actionButton[-1])
            self.actionButton[-1].clicked.connect(self.getAction)

        self.setGeometry(300, 40, 350, 650)
        self.setLayout(self.mainVBox)
        self.setWindowTitle('Select Action to add...')

        self.show()

    def getAction(self):

        buttonThatSent = self.sender()
        self.returnValue = buttonThatSent.text()

        if(self.returnValue == "END" or self.returnValue == "ELSE"):
            self.returnValue = [str(self.returnValue), ""]
            self.accept()
        else:
            newDialogFromName = getattr(action_dialog, str(self.returnValue))
            if(self.ischaras is False):
                self.myActionsDialog = newDialogFromName(
                    self.psSettings["gamefolder"], self)
            else:
                self.myActionsDialog = newDialogFromName(
                    self.psSettings["gamefolder"], self, None, True)

            if self.myActionsDialog.exec_() == QtWidgets.QDialog.Accepted:
                returnActDlg = str(self.myActionsDialog.getValue())

                # self.returnValue.append('|')
                self.returnValue = [str(self.returnValue), str(returnActDlg)]
                self.accept()

    def getValue(self):
        return self.returnValue


class tinyActionsWdgt(QtWidgets.QWidget):
    def __init__(self, parent=None, ssettings={}, ischara=False, isitem=False , **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.ssettings = ssettings
        self.parent = parent
        self.ischara = ischara
        self.isitem = isitem

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

        if(not self.isitem):
            self.checkboxes = []
            self.checkboxes.append(QtWidgets.QCheckBox("on click", self))
            self.checkboxes.append(QtWidgets.QCheckBox("on over", self))
            self.checkboxes[0].setCheckState(QtCore.Qt.Checked)
            self.checkboxes[1].setCheckState(QtCore.Qt.Unchecked)

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

        if(not self.isitem):
            for checkbox in self.checkboxes:
                VBoxButtons.addWidget(checkbox)

        self.ActionList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.ActionList.itemSelectionChanged.connect(self.enableButtonsBecauseActionList)

        ActionListModel = self.ActionList.model()
        ActionListModel.layoutChanged.connect(self.updateActionFromWidget)

    def setList(self,actionToSet):
        if(not self.isitem):
            atype = actionToSet['type']
            for i in range(len(atype)):
                if(atype[i]):
                    self.checkboxes[i].setCheckState(QtCore.Qt.Checked)
                else:
                    self.checkboxes[i].setCheckState(QtCore.Qt.Unchecked)

            listToSet = actionToSet['list']
        else:
            listToSet = actionToSet


        self.ActionList.clear()
        for action in listToSet:
            self.ActionList.addItem(actionItem(action))

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
            self.ActionList.insertItem(indexOfAction,actionItem(actionToAdd))

    def deselectAction(self):
        for i in range(self.ActionList.count()):
            item = self.ActionList.item(i)
            self.ActionList.setItemSelected(item, False)

    def addAction(self):
        if(self.ssettings == {} ):
            return

        self.myActionsWidget = ActionsWidget(self.ssettings,self,self.ischara)
        if self.myActionsWidget.exec_() == QtWidgets.QDialog.Accepted:
            actionToAdd = self.myActionsWidget.getValue()

            if not self.ActionList.selectedItems():
                self.ActionList.addItem(actionItem(actionToAdd))
            else:
                indexOfAction = self.ActionList.row(self.ActionList.selectedItems()[0])
                self.ActionList.insertItem(indexOfAction,actionItem(actionToAdd))

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

        if(not self.isitem):
            onclick = self.checkboxes[0].isChecked()
            onover = self.checkboxes[1].isChecked()
            actiontype = [onclick,onover]
            returnvalue = {'list':allactions, 'type':actiontype }

        else:
            returnvalue = allactions

        return returnvalue
