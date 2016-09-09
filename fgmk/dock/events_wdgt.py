# -*- coding: utf-8 -*-
from fgmk import action_dialog, current_project, actions_wdgt, cmd
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk.util.layer_logic import COLISIONLAYER as COLISIONLAYER
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER

class EventItem(QtWidgets.QListWidgetItem):
    def __init__(self, eventNumber):
        #super().__init__(str(actionAndParameter))
        QtWidgets.QListWidgetItem.__init__(self, '')
        self.setWhatsThis("%d" % eventNumber)
        self.setText("Event %03d" % eventNumber)

class EventAndColisionPalette(QtWidgets.QWidget):
    """
    Allow changing current event and current colision selection
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

        self.labelColisionCurrent = QtWidgets.QLabel("Colision")
        self.radiocolision = QtWidgets.QRadioButton("Colide")
        self.radionocolision = QtWidgets.QRadioButton("Clear")
        self.radiocolision.setChecked(True)
        self.radiocolision.toggled.connect(self.radioColisionToggled)
        self.radionocolision.toggled.connect(self.radioNoColisionToggled)
        self.radiocolision.clicked.connect(self.colisionRadioSelected)
        self.radionocolision.clicked.connect(self.colisionRadioSelected)

        VBox.addWidget(self.labelEventsCurrent)
        VBox.addWidget(self.eventSelectSpinbox)
        VBox.addWidget(self.labelColisionCurrent)
        VBox.addWidget(self.radiocolision)
        VBox.addWidget(self.radionocolision)

    def colisionRadioSelected(self):
        self.parent.parent.changeLayerCurrent(COLISIONLAYER)

    def setColisionValueView(self,colisionValue):
        if(colisionValue==1):
            self.radiocolision.setChecked(True)
        else:
            self.radionocolision.setChecked(True)

    def radioColisionToggled(self):
        if(self.radiocolision.isChecked()):
            self.parent.parent.myMapWidget.currentColision = 1;

    def radioNoColisionToggled(self):
        if(self.radionocolision.isChecked()):
            self.parent.parent.myMapWidget.currentColision = 0;


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

        self.ActionList = actions_wdgt.tinyActionsWdgt(self,current_project.settings,nothis=False)

        self.eventsAndColision = EventAndColisionPalette(self)

        VBoxEventsList = QtWidgets.QVBoxLayout()

        self.HBox.addLayout(VBoxEventsList, 1)
        self.HBox.addWidget(self.ActionList, 3)
        self.HBox.addWidget(self.eventsAndColision)

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
