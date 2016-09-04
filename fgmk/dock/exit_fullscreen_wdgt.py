# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class ExitFSWidget(QtWidgets.QWidget):
    """
    Allow exiting fullscreen through clicking in a button.
    This widget will be used in a mouse oriented environment.
    """
    def __init__(self, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self,parent, **kwargs)
        #super().__init__(parent, **kwargs)

        self.parent = parent
        self.VBox = QtWidgets.QVBoxLayout(self)
        self.ButtonExitFS = QtWidgets.QPushButton("exit\nfullscreen")
        self.ButtonExitFS.clicked.connect(self.ExitFS)
        self.VBox.addWidget(self.ButtonExitFS)
        self.setMaximumHeight(60)
        # self.setMinimumHeight(60)
        self.setMaximumWidth(90)
        # self.setMinimumWidth(84)

    def ExitFS(self):
        self.parent.fullscreenViewAction.toggle()
