# -*- coding: utf-8 -*-
from fgmk import action_dialog, current_project, actions_wdgt, cmd
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk.util.layer_logic import COLLISIONLAYER as COLLISIONLAYER
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER

class EventItem(QtWidgets.QListWidgetItem):
    def __init__(self, eventNumber):
        #super().__init__(str(actionAndParameter))
        QtWidgets.QListWidgetItem.__init__(self, '')
        self.setWhatsThis("%d" % eventNumber)
        self.setText("Event %03d" % eventNumber)

class EventAndCollisionPalette(QtWidgets.QWidget):
    """
    Allow changing current event and current collision selection
    """

    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent

        VBox = QtWidgets.QVBoxLayout(self)
        VBox.setAlignment(QtCore.Qt.AlignTop)

        self.labelEventsCurrent = QtWidgets.QLabel("Event Nº")
        self.eventSelectSpinbox = QtWidgets.QSpinBox(self)
        self.eventSelectSpinbox.setToolTip("Event 0 means No Event.")
        self.eventSelectSpinbox.setMinimum(0)
        self.eventSelectSpinbox.setMaximum(100)
        self.eventSelectSpinbox.setSingleStep(1)
        self.eventSelectSpinbox.valueChanged.connect(self.parent.parent.changeEventCurrent)

        self.labelCollisionCurrent = QtWidgets.QLabel("Collision")
        self.radiocollision = QtWidgets.QRadioButton("Colide")
        self.radionocollision = QtWidgets.QRadioButton("Clear")
        self.radiocollision.setChecked(True)
        self.radiocollision.toggled.connect(self.radioCollisionToggled)
        self.radionocollision.toggled.connect(self.radioNoCollisionToggled)
        self.radiocollision.clicked.connect(self.collisionRadioSelected)
        self.radionocollision.clicked.connect(self.collisionRadioSelected)

        VBox.addWidget(self.labelEventsCurrent)
        VBox.addWidget(self.eventSelectSpinbox)
        VBox.addWidget(self.labelCollisionCurrent)
        VBox.addWidget(self.radiocollision)
        VBox.addWidget(self.radionocollision)

    def collisionRadioSelected(self):
        self.parent.parent.changeLayerCurrent(COLLISIONLAYER)

    def setCollisionValueView(self,collisionValue):
        if(collisionValue==1):
            self.radiocollision.setChecked(True)
        else:
            self.radionocollision.setChecked(True)

    def radioCollisionToggled(self):
        if(self.radiocollision.isChecked()):
            self.parent.parent.myMapWidget.currentCollision = 1;

    def radioNoCollisionToggled(self):
        if(self.radionocollision.isChecked()):
            self.parent.parent.myMapWidget.currentCollision = 0;


class EventsWidget(QtWidgets.QWidget):
    """
    This widget allows adding actions to an event. It also allows changing the
    current selected Event number and Collision/non Colidable tile for drawing.
    """

    def __init__(self, pMap, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent

        self.HBox = QtWidgets.QHBoxLayout(self)
        self.HBox.setAlignment(QtCore.Qt.AlignTop)

        self.labelEventsList = QtWidgets.QLabel("List of Events:")
        self.EventsList = QtWidgets.QListWidget(self)

        self.ActionList = actions_wdgt.tinyActionsWdgt(self,current_project.settings,nothis=False)

        self.eventsAndCollision = EventAndCollisionPalette(self)

        VBoxEventsList = QtWidgets.QVBoxLayout()

        self.HBox.addLayout(VBoxEventsList, 1)
        self.HBox.addWidget(self.ActionList, 3)
        self.HBox.addWidget(self.eventsAndCollision)

        VBoxEventsList.addWidget(self.labelEventsList)
        VBoxEventsList.addWidget(self.EventsList)

        self.EventsList.itemSelectionChanged.connect(
            self.enableButtonsBecauseEventsList)
        self.EventsList.itemSelectionChanged.connect(
            self.selectedItemFromEventsList)
        self.ActionList.somethingChanged.connect(self.actionListChanged)

        self.ActionList.setAllState(False)

        self.show()

        self.pMap = pMap

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
                item = EventItem(event)
                self.EventsList.addItem(item)

        self.EventsList.sortItems()

        self.show()

    def actionListChanged(self, previous_actions,current_actions,what,description):
        #Let's get the event when somethingChanged in the actionsList
        if(len(self.EventsList.selectedItems())>0):
            event = self.EventsList.selectedItems()[0].whatsThis()
        else:
            return

        command = cmd.CommandEventAction(description,
            self,
            event,
            current_actions,
            previous_actions,
            what)

        cmd.commandToStack(command)

    def doAction(self, event, actions):
        self.pMap.setEventList(actions, event)
        self.selectedItemFromEventsList()

    def selectedItemFromEventsList(self):
        if(len(self.EventsList.selectedItems())>0):
            item = self.EventsList.selectedItems()[0]

            actions = self.pMap.getActionListOnEvent(item.whatsThis())
            eventType = self.pMap.getEventType(item.whatsThis())
            typeAndActions = {'list':actions, 'type':eventType }

            self.ActionList.setList(typeAndActions)

    def enableButtonsBecauseEventsList(self):
        if(self.EventsList.currentItem() == None):
            self.ActionList.setAllState(False)
            return

        if (self.EventsList.currentItem().isSelected() == True):
            self.ActionList.setAllState(True)
        else:
            self.ActionList.setAllState(False)
