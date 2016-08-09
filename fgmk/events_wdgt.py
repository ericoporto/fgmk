# -*- coding: utf-8 -*-
from fgmk import action_dialog, current_project, actions_wdgt, cmd
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk.layer_wdgt import COLISIONLAYER as COLISIONLAYER
from fgmk.layer_wdgt import EVENTSLAYER as EVENTSLAYER



class EventsWidget(QtWidgets.QWidget):
    """
    This widget allows adding actions to an event. It also allows changing the
    current selected Event number and Colision/non Colidable tile for drawing.
    """

    def __init__(self, pMap, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent

        self.HBox = QtWidgets.QHBoxLayout(self)
        self.HBox.setAlignment(QtCore.Qt.AlignTop)

        self.labelEventsList = QtWidgets.QLabel("List of Events:")
        self.EventsList = QtWidgets.QListWidget(self)

        self.labelActionList = QtWidgets.QLabel("List of Actions:")
        self.ActionList = QtWidgets.QListWidget(self)

        VBoxEventsList = QtWidgets.QVBoxLayout()
        VBoxActionList = QtWidgets.QVBoxLayout()
        VBoxLeftButtons = QtWidgets.QVBoxLayout()
        VBoxButtons = QtWidgets.QVBoxLayout()

        VBoxLeftButtons.setAlignment(QtCore.Qt.AlignTop)

        self.labelEventsCurrent = QtWidgets.QLabel("Event Nº")
        self.eventSelectSpinbox = QtWidgets.QSpinBox(self)
        self.eventSelectSpinbox.setToolTip("Event 0 means No Event.")
        self.eventSelectSpinbox.setMinimum(0)
        self.eventSelectSpinbox.setMaximum(100)
        self.eventSelectSpinbox.setSingleStep(1)
        self.eventSelectSpinbox.valueChanged.connect(self.parent.changeEventCurrent)

        self.labelColisionCurrent = QtWidgets.QLabel("Colision")
        self.radiocolision = QtWidgets.QRadioButton("Colide")
        self.radionocolision = QtWidgets.QRadioButton("Clear")
        self.radiocolision.setChecked(True)
        self.radiocolision.toggled.connect(self.radioColisionToggled)
        self.radionocolision.toggled.connect(self.radioNoColisionToggled)
        self.radiocolision.clicked.connect(self.colisionRadioSelected)
        self.radionocolision.clicked.connect(self.colisionRadioSelected)

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

        self.HBox.addLayout(VBoxEventsList, 1)
        self.HBox.addLayout(VBoxActionList, 2)
        self.HBox.addLayout(VBoxLeftButtons)
        self.HBox.addLayout(VBoxButtons)

        VBoxLeftButtons.addWidget(self.labelEventsCurrent)
        VBoxLeftButtons.addWidget(self.eventSelectSpinbox)
        VBoxLeftButtons.addWidget(self.labelColisionCurrent)
        VBoxLeftButtons.addWidget(self.radiocolision)
        VBoxLeftButtons.addWidget(self.radionocolision)

        VBoxEventsList.addWidget(self.labelEventsList)
        VBoxEventsList.addWidget(self.EventsList)

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
            checkbox.stateChanged.connect(self.checkboxesChanged)

        self.ActionList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.EventsList.itemSelectionChanged.connect(
            self.enableButtonsBecauseEventsList)
        self.ActionList.itemSelectionChanged.connect(
            self.enableButtonsBecauseActionList)
#        self.EventsList.itemClicked.connect(self.selectedItemFromEventsList)
        self.EventsList.itemSelectionChanged.connect(
            self.selectedItemFromEventsList)

        # ActionListModel = self.ActionList.model()
        # ActionListModel.layoutChanged.connect(self.updateActionFromWidget)

        self.addActionButton.setEnabled(False)
        self.removeActionButton.setEnabled(False)
        self.ActionList.setEnabled(False)
        self.labelActionList.setEnabled(False)
        self.deselectActionButton.setEnabled(False)
        self.editActionButton.setEnabled(False)

        self.show()

        self.pMap = pMap

    def colisionRadioSelected(self):
        self.parent.changeLayerCurrent(COLISIONLAYER)

    def setColisionValueView(self,colisionValue):
        if(colisionValue==1):
            self.radiocolision.setChecked(True)
        else:
            self.radionocolision.setChecked(True)

    def radioColisionToggled(self):
        if(self.radiocolision.isChecked()):
            self.parent.myMapWidget.currentColision = 1;

    def radioNoColisionToggled(self):
        if(self.radionocolision.isChecked()):
            self.parent.myMapWidget.currentColision = 0;

    # def updateActionFromWidget(self):
    #     print("update action from widget")
    #
    #     self.pMap.removeAllActionsOnEvent(
    #         self.EventsList.selectedItems()[0].whatsThis())
    #     i = 0
    #     while i < self.ActionList.count():
    #         item = self.ActionList.item(i)
    #         actionToAdd = item.getAction()
    #         self.pMap.addActionToEvent(
    #             actionToAdd, self.EventsList.selectedItems()[0].whatsThis())
    #         i += 1

    def editAction(self):
        if self.EventsList.selectedItems() is not None:
            indexOfAction = self.ActionList.row(
                self.ActionList.selectedItems()[0])
            actionParamToEdit = self.pMap.getActionOnEvent(
                indexOfAction, self.EventsList.selectedItems()[0].whatsThis())

            actionToEdit = actionParamToEdit[0]
            paramOfEdit = actionParamToEdit[1]

            paramArrayOfEdit = paramOfEdit.split(';')

            newDialogFromName = getattr(action_dialog, str(actionToEdit))

            self.myActionsDialog = newDialogFromName(
                current_project.settings["gamefolder"], self, paramArrayOfEdit)
            if self.myActionsDialog.exec_() == QtWidgets.QDialog.Accepted:
                returnActDlg = str(self.myActionsDialog.getValue())

                actionToAdd = [actionToEdit, str(returnActDlg)]

                command = cmd.CommandChangeAction("edited action",
                                 self,
                                 indexOfAction,
                                 self.EventsList.selectedItems()[0].whatsThis(),
                                 actionParamToEdit,
                                 actionToAdd)
                cmd.commandToStack(command)


    def changeAction(self, actionindex, eventindex, newaction):
        self.pMap.changeActionOnEvent(actionindex, newaction, eventindex)

        if(len(self.EventsList.selectedItems())>0):
            seleventindex = self.EventsList.selectedItems()[0].whatsThis()
            if(seleventindex==eventindex):
                self.ActionList.takeItem(actionindex)
                self.ActionList.insertItem(
                    actionindex, actions_wdgt.actionItem(newaction))


    def deselectAction(self):
        for i in range(self.ActionList.count()):
            item = self.ActionList.item(i)
            item.setSelected(False)

    def deselectAll(self):
        self.deselectAction()
        for i in range(self.EventsList.count()):
            item = self.EventsList.item(i)
            item.setSelected(False)

        self.enableButtonsBecauseEventsList()

    def checkboxesChanged(self, newState):
        if self.EventsList.selectedItems() is not None:
            checkboxesStates = []
            for checkbox in self.checkboxes:
                checkboxesStates.append(int(checkbox.isChecked()))

            self.pMap.setEventType(str(self.EventsList.selectedItems()[0].whatsThis()),
                                   [int(self.checkboxes[0].isChecked()),
                                    int(self.checkboxes[1].isChecked())
                                    ])

    def updateEventsList(self):
        updatedListOfEvents = self.pMap.getTileListFromLayer(EVENTSLAYER)
        allItemsInEventsList = []
        for index in range(self.EventsList.count()):
            allItemsInEventsList.append([self.EventsList.item(index), index, int(self.EventsList.item(index).whatsThis())])

        for item in allItemsInEventsList:
            for event in updatedListOfEvents[:]:
                if (item[0].whatsThis() == str(event)):
                    updatedListOfEvents.remove(event)
                    break
            else:
                for index in range(self.EventsList.count()):
                    if(item[0] == self.EventsList.item(index)):
                        settonone = self.EventsList.takeItem(index)
                        settonone = None
                        break

        if updatedListOfEvents is not None:
            for event in updatedListOfEvents:
                item = QtWidgets.QListWidgetItem("Event %03d" % event)
                item.setWhatsThis("%d" % event)
                self.EventsList.addItem(item)

        self.EventsList.sortItems()

        self.show()

    def addAction(self):
        self.myActionsWidget = actions_wdgt.ActionsWidget(current_project.settings, self)
        if self.myActionsWidget.exec_() == QtWidgets.QDialog.Accepted:
            actionToAdd = self.myActionsWidget.getValue()

            if self.EventsList.selectedItems() is not None:
                if not self.ActionList.selectedItems():
                    lastactionitem = self.ActionList.count()

                    command = cmd.CommandAddAction("added action",
                                               self,
                                               lastactionitem,
                                               self.EventsList.selectedItems()[0].whatsThis(),
                                               actionToAdd)
                    cmd.commandToStack(command)

                else:
                    indexOfAction = self.ActionList.row(
                        self.ActionList.selectedItems()[0])


                    command = cmd.CommandAddAction("added action",
                                               self,
                                               indexOfAction,
                                               self.EventsList.selectedItems()[0].whatsThis(),
                                               actionToAdd)
                    cmd.commandToStack(command)


    def addActionIndex(self, actionindex, eventindex, acctiontoadd):
        self.pMap.insertActionToEvent(actionindex, acctiontoadd, eventindex)

        if(len(self.EventsList.selectedItems())>0):
            seleventindex = self.EventsList.selectedItems()[0].whatsThis()
            if(seleventindex==eventindex):
                self.ActionList.insertItem(actionindex,
                                           actions_wdgt.actionItem(acctiontoadd))

    def removeAction(self):
        for item in self.ActionList.selectedItems():
            itemIndex = self.ActionList.row(item)

            actiontodel = self.pMap.getActionOnEvent(
                itemIndex, self.EventsList.selectedItems()[0].whatsThis())

            command = cmd.CommandDelAction("deleted action",
                                       self,
                                       itemIndex,
                                       self.EventsList.selectedItems()[0].whatsThis(),
                                       actiontodel)
            cmd.commandToStack(command)

    def removeActionIndex(self, actionindex, eventindex):
        self.pMap.removeActionByIndexOnEvent(actionindex, eventindex)
        if(len(self.EventsList.selectedItems())>0):
            seleventindex = self.EventsList.selectedItems()[0].whatsThis()
            if(seleventindex==eventindex):
                self.ActionList.takeItem(actionindex)

    def selectedItemFromEventsList(self):
        if(len(self.EventsList.selectedItems())>0):
            item = self.EventsList.selectedItems()[0]

            self.ActionList.clear()

            for actionitemInList in self.pMap.getActionListOnEvent(item.whatsThis()):
                self.ActionList.addItem(actions_wdgt.actionItem(actionitemInList))

            state = self.pMap.getEventType(item.whatsThis())

            for i in range(len(self.checkboxes)):
                self.checkboxes[i].setCheckState(2 * state[i])
                self.checkboxes[i].show()

            self.ActionList.show()

    def enableButtonsBecauseEventsList(self):
        if(self.EventsList.currentItem() == None):
            self.addActionButton.setEnabled(False)
            self.removeActionButton.setEnabled(False)
            self.ActionList.setEnabled(False)
            self.labelActionList.setEnabled(False)
            self.deselectActionButton.setEnabled(False)
            self.editActionButton.setEnabled(False)
            return

        if (self.EventsList.currentItem().isSelected() == True):
            self.addActionButton.setEnabled(True)
            self.ActionList.setEnabled(True)
            self.labelActionList.setEnabled(True)
        else:
            self.addActionButton.setEnabled(False)
            self.removeActionButton.setEnabled(False)
            self.ActionList.setEnabled(False)
            self.labelActionList.setEnabled(False)
            self.deselectActionButton.setEnabled(False)
            self.editActionButton.setEnabled(False)

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

    # def getActionListFromEvent(self):
