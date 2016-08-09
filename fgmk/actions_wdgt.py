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
