import json
import os.path
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import tMat,  TileXtra, fifl, current_project, TileSet



class CommandCTTileType(QtWidgets.QUndoCommand):

    def __init__(self, child, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, description):
        super().__init__(description)

        self.sender = senderTileWdgt
        self.tileX = self.sender.tileX
        self.tileY = self.sender.tileY
        self.Layer = layer
        self.changeTypeTo = changeTypeTo
        self.oldType = self.sender.tileType[layer]

        self.pmyMapWidget = child.myMapWidget
        self.pMap = pMap
        self.ptileset = ptileset

    def redo(self):
        self.pMap.setTile(self.tileX, self.tileY,
                          self.Layer, self.changeTypeTo)
        self.sender.updateTileImageInMap(
            self.changeTypeTo, self.Layer, self.ptileset, self.pmyMapWidget.myScale)
        #print("Type= ", self.changeTypeTo, "  X= " ,self.tileX, "  Y= " , self.tileY)

    def undo(self):
        self.pMap.setTile(self.tileX, self.tileY, self.Layer, self.oldType)
        self.sender.updateTileImageInMap(
            self.oldType, self.Layer, self.ptileset, self.pmyMapWidget.myScale)
        #print("Type= ", self.oldType, "  X= " ,self.tileX, "  Y= " , self.tileY)


class CommandCGroupTType(QtWidgets.QUndoCommand):

    def __init__(self, child, senderTileWdgt, pMap, ptileset, layer,  changeTypeTo, listToChange, description):
        super().__init__(description)

        self.tileX = senderTileWdgt.tileX
        self.tileY = senderTileWdgt.tileY
        self.Layer = layer
        self.changeTypeTo = changeTypeTo

        self.pmyMapWidget = child.myMapWidget
        self.pMap = pMap
        self.ptileset = ptileset

        self.listToChange = listToChange

    def redo(self):
        for change in self.listToChange:
            tile = self.pmyMapWidget.TileList[change[1]][change[0]]
            self.pMap.setTile(change[0], change[1], self.Layer, change[3])
            tile.updateTileImageInMap(
                change[3], self.Layer, self.ptileset, self.pmyMapWidget.myScale)
            #print("Type= ", change[3], "  X= " , change[0], "  Y= " , change[1])

    def undo(self):
        for change in self.listToChange:
            tile = self.pmyMapWidget.TileList[change[1]][change[0]]
            self.pMap.setTile(change[0], change[1], self.Layer, change[2])
            tile.updateTileImageInMap(
                change[2], self.Layer, self.ptileset, self.pmyMapWidget.myScale)
            #print("Type= ", change[2], "  X= " ,change[0], "  Y= " , change[1])


class newProject(QtWidgets.QDialog):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.returnValue = {"name": "NewFile", "baseFolder": ""}

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        HBoxFolder = QtWidgets.QHBoxLayout()
        self.LineEditFolder = QtWidgets.QLineEdit()
        self.LineEditFolder.setReadOnly(True)
        self.LineEditFolder.setText(str(self.returnValue["baseFolder"]))
        self.buttonFolder = QtWidgets.QPushButton("Browse")
        self.buttonFolder.clicked.connect(self.selectGameFolder)
        HBoxFolder.addWidget(self.LineEditFolder)
        HBoxFolder.addWidget(self.buttonFolder)

        HBoxName = QtWidgets.QHBoxLayout()
        self.LineEditName = QtWidgets.QLineEdit()
        self.LineEditName.setText(str(self.returnValue["name"]))
        self.LineEditName.editingFinished.connect(self.validateLineEditName)
        HBoxName.addWidget(QtWidgets.QLabel("Name:"))
        HBoxName.addWidget(self.LineEditName)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(QtWidgets.QLabel("THIS FUNCTION IS NOT COMPLETE YET"))
        self.VBox.addWidget(QtWidgets.QLabel("Select folder to create game:"))
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(QtWidgets.QLabel("Set game name:"))
        self.VBox.addLayout(HBoxName)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('New game current_projectect...')

    def validateLineEditName(self):
        tempStr = str(self.LineEditName.text())
        tempStr = tempStr.title()
        tempStr = tempStr.replace(" ", "")
        self.LineEditName.setText(tempStr)
        self.returnValue["name"] = self.LineEditName.text()
        self.validateIsOk()

    def selectGameFolder(self):
        self.LineEditFolder.setText(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.returnValue["baseFolder"] = self.LineEditFolder.text()
        self.validateIsOk()

    def validateIsOk(self):
        if self.returnValue["name"] != "" and self.returnValue["baseFolder"] != "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def getValue(self):
        return self.returnValue


class newFile(QtWidgets.QDialog):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        gamefolder = ""
        if "gamefolder" in current_project.settings:
            gamefolder = os.path.join(current_project.settings["gamefolder"])
            if not os.path.isdir(gamefolder):
                gamefolder = ""

        self.returnValue = {"name": "NewFile", "width": 15, "height": 15, "gameFolder": gamefolder

                            }

        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.setAlignment(QtCore.Qt.AlignTop)

        HBoxFolder = QtWidgets.QHBoxLayout()
        self.LineEditFolder = QtWidgets.QLineEdit()
        self.LineEditFolder.setReadOnly(True)
        self.LineEditFolder.setText(str(self.returnValue["gameFolder"]))
        self.buttonFolder = QtWidgets.QPushButton("Browse")
        self.buttonFolder.clicked.connect(self.selectGameFolder)
        HBoxFolder.addWidget(self.LineEditFolder)
        HBoxFolder.addWidget(self.buttonFolder)

        HBoxSize = QtWidgets.QHBoxLayout()
        self.LineEditWidth = QtWidgets.QLineEdit()
        self.LineEditWidth.setInputMask("000")
        self.LineEditWidth.setText(str(self.returnValue["width"]))
        self.LineEditWidth.editingFinished.connect(self.validateLineEditWidth)
        self.LineEditHeight = QtWidgets.QLineEdit()
        self.LineEditHeight.setInputMask("000")
        self.LineEditHeight.setText(str(self.returnValue["height"]))
        self.LineEditHeight.editingFinished.connect(
            self.validateLineEditHeight)
        HBoxSize.addWidget(QtWidgets.QLabel("Width:"))
        HBoxSize.addWidget(self.LineEditWidth)
        HBoxSize.addWidget(QtWidgets.QLabel("Height:"))
        HBoxSize.addWidget(self.LineEditHeight)

        HBoxName = QtWidgets.QHBoxLayout()
        self.LineEditName = QtWidgets.QLineEdit()
        self.LineEditName.setText(str(self.returnValue["name"]))
        self.LineEditName.editingFinished.connect(self.validateLineEditName)
        HBoxName.addWidget(QtWidgets.QLabel("Name:"))
        HBoxName.addWidget(self.LineEditName)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.VBox.addWidget(QtWidgets.QLabel("Select game folder:"))
        self.VBox.addLayout(HBoxFolder)
        self.VBox.addWidget(QtWidgets.QLabel("Set map properties:"))
        self.VBox.addLayout(HBoxSize)
        self.VBox.addLayout(HBoxName)
        self.VBox.addWidget(self.buttonBox)

        self.setGeometry(300, 40, 350, 650)
        self.setWindowTitle('New map...')

    def validateLineEditWidth(self):
        if int(self.LineEditWidth.text()) < 15:
            self.LineEditWidth.setText("15")
        elif int(self.LineEditWidth.text()) > 100:
            self.LineEditWidth.setText("100")
        else:
            self.LineEditWidth.setText(str(int(self.LineEditWidth.text())))
        self.returnValue["width"] = int(self.LineEditWidth.text())
        self.validateIsOk()

    def validateLineEditHeight(self):
        if int(self.LineEditHeight.text()) < 15:
            self.LineEditHeight.setText("15")
        elif int(self.LineEditHeight.text()) > 100:
            self.LineEditHeight.setText("100")
        else:
            self.LineEditHeight.setText(str(int(self.LineEditHeight.text())))
        self.returnValue["height"] = int(self.LineEditHeight.text())
        self.validateIsOk()

    def validateLineEditName(self):
        tempStr = str(self.LineEditName.text())
        tempStr = tempStr.title()
        tempStr = tempStr.replace(" ", "")
        self.LineEditName.setText(tempStr)
        self.returnValue["name"] = self.LineEditName.text()
        self.validateIsOk()

    def selectGameFolder(self):
        self.LineEditFolder.setText(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.returnValue["gameFolder"] = self.LineEditFolder.text()
        self.validateIsOk()

    def validateIsOk(self):
        if self.returnValue["name"] != "" and self.returnValue["gameFolder"] != "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def getValue(self):
        return self.returnValue
