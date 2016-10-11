from PyQt5 import QtWidgets
from fgmk import game_init, current_project, miniWdgt

class text(QtWidgets.QWidget):
    """
    Simple plain text entry that supports multi line
    """
    def __init__(self, labelText=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QWidget.__init__(self, **kwargs)

        if(labelText==None):
            self.LabelText = QtWidgets.QLabel("text:")
        else:
            self.LabelText = QtWidgets.QLabel(labelText)

        self.TextEdit = QtWidgets.QPlainTextEdit()

        VBox = QtWidgets.QVBoxLayout(self)
        VBox.addWidget(self.LabelText)
        VBox.addWidget(self.TextEdit)

    def getValue(self):
        text = str(self.TextEdit.toPlainText())
        textListLf = text.split("\n")
        textToReturn = textListLf[0]
        for line in textListLf[1:]:
            textToReturn += '\\n' + line
        return textToReturn

    def edit(self, param):
        self.TextEdit.setPlainText(param)


class linetext(QtWidgets.QWidget):
    """
    Simple single line text entry
    """
    def __init__(self, labelText=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QWidget.__init__(self, **kwargs)

        if(labelText==None):
            self.LabelText = QtWidgets.QLabel("short text:")
        else:
            self.LabelText = QtWidgets.QLabel(labelText)

        self.LineEdit = QtWidgets.QLineEdit()

        VBox = QtWidgets.QVBoxLayout(self)
        VBox.addWidget(self.LabelText)
        VBox.addWidget(self.LineEdit)

    def getValue(self):
        text = str(self.LineEdit.toPlainText())
        return text

    def edit(self, param):
        self.LineEdit.setText(param)


class map(QtWidgets.QWidget):
    def __init__(self, labelText=None, nothis=True, myMap=None, **kwargs):
        #super().__init__(parent, **kwargs)
        QWidget.__init__(self, **kwargs)

        if(labelText==None):
            self.LabelText = QtWidgets.QLabel("select map:")
        else:
            self.LabelText = QtWidgets.QLabel(labelText)

        self.initFile = game_init.openInitFile(current_project.settings['gamefolder'])

        self.myMap = myMap
        self.nothis = nothis

        self.levelSelector = miniWdgt.levelSelector(nothis=self.nothis)
        self.myMiniMapViewer = miniWdgt.MiniMapViewer(
                                    mapAtStart=self.levelSelector.itemText(0),
                                    nothis=self.nothis,
                                    myMap=self.myMap,
                                    indicative=0)

        self.levelSelector.currentIndexChanged.connect(self.updateMap)

        VBox = QtWidgets.QVBoxLayout(self)
        VBox.addWidget(self.levelSelector)
        VBox.addWidget(self.myMiniMapViewer)

        VBox = QtWidgets.QVBoxLayout(self)
        VBox.addWidget(self.LabelText)
        VBox.addLayout(VBox)

    def updateMap(self, levelIndex):
        self.myMiniMapViewer.updateMap(self.levelSelector.itemText(levelIndex))

    def getValue(self):
        text = str(self.levelSelector.currentText())
        return text

    def edit(self, param):
        self.levelSelector.edit(param)
