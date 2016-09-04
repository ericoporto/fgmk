# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from fgmk.ff import mapfile
from fgmk.util.layer_logic import COLISIONLAYER as COLISIONLAYER
from fgmk.util.layer_logic import EVENTSLAYER as EVENTSLAYER

class LayerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        self.LabelLayer = QtWidgets.QLabel("Layer is: %d" % 0)
        self.VBox.addWidget(self.LabelLayer)
        self.ButtonLayer = []

        for i in range(len(mapfile.LayersName)):
            self.ButtonLayer.append(
                QtWidgets.QPushButton(mapfile.LayersName[i]))
            self.ButtonLayer[-1].setObjectName(mapfile.LayersName[i])
            self.ButtonLayer[-1].clicked.connect(self.buttonLayerClicked)
            self.VBox.addWidget(self.ButtonLayer[-1])

        self.setMaximumHeight(180)
        self.show()

    def buttonLayerClicked(self):
        # print self.sender().objectName()
        if str(self.sender().objectName()) == mapfile.LayersName[0]:
            self.changeLayerTo(0)
        elif str(self.sender().objectName()) == mapfile.LayersName[1]:
            self.changeLayerTo(1)
        elif str(self.sender().objectName()) == mapfile.LayersName[2]:
            self.changeLayerTo(2)
        elif str(self.sender().objectName()) == mapfile.LayersName[3]:
            self.changeLayerTo(COLISIONLAYER)
        elif str(self.sender().objectName()) == mapfile.LayersName[4]:
            self.changeLayerTo(EVENTSLAYER)

    def changeLayerTo(self, layerNumber):
        self.parent.changeLayerCurrent(layerNumber)

    def changeLayerView(self, layerNumber):
        self.LabelLayer.setText("Current: %s" %
                                mapfile.LayersName[layerNumber])
