import json
from PyQt5 import QtCore, QtWidgets
from fgmk import action_dialog, getdata

class actionItem(QtWidgets.QListWidgetItem):
    def __init__(self, actionAndParameter):
        super().__init__(str(actionAndParameter))
        self.setText = str(actionAndParameter)
        self.setData(QtCore.Qt.UserRole, actionAndParameter)

    def getAction(self):
        actionAndParameterReturn = self.data(QtCore.Qt.UserRole)
        action = str(actionAndParameterReturn[0])
        parameter = str(actionAndParameterReturn[1])
        return [action, parameter]

class ActionsWidget(QtWidgets.QDialog):
    def __init__(self, psSettings, parent=None, ischaras=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.psSettings = psSettings
        self.ischaras = ischaras

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        filepath = getdata.path('actionsList.json')
        f = open(filepath, "r")
        e = json.load(f)
        f.close()

        self.parent = parent
        self.actionButton = []

        for action in e["actionOrder"]:
            self.actionButton.append(QtWidgets.QPushButton(action, self))
            self.VBox.addWidget(self.actionButton[-1])
            self.actionButton[-1].clicked.connect(self.getAction)

        self.setGeometry(300, 40, 350, 650)
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
