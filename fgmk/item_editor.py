
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_model, current_project, fifl

item_categories=['none','consumable','collectible','weapon','armor']
default_equipable = False
default_unique = False
default_usable = False
default_effect = None
default_statMod = None
default_description = ''
default_icon = None
default_category = None
default_action = None

class base_item:
    def __init__(self,name, equipable=default_equipable,
                            unique=default_unique,
                            usable=default_usable,
                            effect=default_effect,
                            statMod=default_statMod,
                            description=default_description,
                            icon=default_icon,
                            category=default_category,
                            action=default_action):
        normalized_name = str(name)
        normalized_name = normalized_name.title()
        normalized_name = normalized_name.replace(" ", "")

        self.name = name
        self.equipable = equipable
        self.unique = unique
        self.usable = usable
        self.effect = effect
        self.statMod = statMod
        self.description = description
        self.icon = icon
        self.category = category
        self.action = action

    def setname(self,name):
        self.name = name

    def setequipable(self, equipable=True):
        self.equipable = equipable

    def setunique(self, unique=True):
        self.unique = unique

    def setusable(self,usable=True):
        self.usable = usable

    def seteffect(self,effect=default_effect):
        self.effect = effect

    def setstatmod(self,statMod=default_statMod):
        self.statMod = statMod

    def setdescription(self, description=default_description):
        self.description = description

    def seticon(self, icon=default_icon):
        self.icon = icon

    def setcategory(self, category=default_category):
        self.category = category

    def setaction(self,action=default_action):
        self.action = action

    def getnormalname(self):
        normalized_name = str(self.name)
        normalized_name = normalized_name.title()
        normalized_name = normalized_name.replace(" ", "")
        return normalized_name

    def getjsontree(self):
        jsonTree = {}
        jsonTree['name'] = self.name
        if(self.equipable):
            jsonTree['equipable'] = True
        if(self.usable):
            jsonTree['usable'] = True
        if(self.unique):
            jsonTree['unique'] = True
        if(self.effect != None):
            jsonTree['effect'] = self.effect
        if(self.statMod != None):
            jsonTree['statMod'] = self.statMod
        if(self.description != False or self.description != ''):
            jsonTree['description'] = self.description
        if(self.icon != None):
            jsonTree['icon'] = self.icon
        if(self.category != None):
            jsonTree['category'] = self.category
        if(self.action != None):
            jsonTree['action'] = self.action

        return jsonTree


class ItemsFormat(base_model.BaseFormat):
    def __init__(self):
        base_model.BaseFormat.__init__(self)

        self.filename = os.path.join(current_project.settings['gamefolder'],ITEMSFILE)
        self.new()

    def new(self):
        self.jsonTree = {"Items":{}}

    def addItem(self, item):
        self.jsonTree['Items'][item.getnormalname()] = item.getjsontree()
        return self.jsonTree

    def removeItemName(self, name):
        it = base_item(name)
        del self.jsonTree['Items'][it.getnormalname()]
        return self.jsonTree

class ItemCfgWidget(QtWidgets.QWidget):
    def __init__(self, itemd=None, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent
        if(itemd==None):
            self.itemd = base_item('')
        else:
            self.itemd = itemd

        VBox = QtWidgets.QVBoxLayout(self)

        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.radioEquipable = QtWidgets.QRadioButton('equipable',self)
        self.radioUsable = QtWidgets.QRadioButton('usable', self)
        self.radioNone = QtWidgets.QRadioButton('none', self)
        self.checkboxUnique =  QtWidgets.QCheckBox('unique', self)
        self.descriptionLineEdit = QtWidgets.QLineEdit(self)
        self.comboboxCategory = QtWidgets.QComboBox(self)

        for i in range(len(item_categories)):
            category = item_categories[i]
            self.comboboxCategory.insertItem(i,category)

        self.loadItem()

        VBox.addWidget(QtWidgets.QLabel('Item name:'))
        VBox.addWidget(self.nameLineEdit)
        VBox.addWidget(QtWidgets.QLabel('Item properties:'))
        VBox.addWidget(self.radioEquipable)
        VBox.addWidget(self.radioUsable)
        VBox.addWidget(self.radioNone)
        VBox.addWidget(self.checkboxUnique)
        VBox.addWidget(QtWidgets.QLabel('Item description:'))
        VBox.addWidget(self.descriptionLineEdit)
        VBox.addWidget(QtWidgets.QLabel('Item category:'))
        VBox.addWidget(self.comboboxCategory)

    def loadItem(self,item=None):
        if(item!=None):
            self.itemd = item

        self.nameLineEdit.setText(self.itemd.name)
        self.descriptionLineEdit.setText(self.itemd.description)
        self.radioNone.setChecked(True)
        if(self.itemd.equipable != default_equipable):
            self.radioEquipable.setChecked(True)
        if(self.itemd.usable != default_usable):
            self.radioUsable.setChecked(True)
        if(self.itemd.unique != default_unique):
            self.checkboxUnique.setChecked(True)
        else:
            self.checkboxUnique.setChecked(False)
        self.comboboxCategory.setCurrentIndex(0)
        if(self.itemd.category != default_category):
            category_index = item_categories.index(self.itemd.category)
            self.comboboxCategory.setCurrentIndex(category_index)

    def saveItem(self,item=None):
        if(item!=None):
            self.itemd = item

        self.itemd.setname(self.nameLineEdit.text())
        self.itemd.setdescription(self.descriptionLineEdit.text())
        if(self.radioEquipable.isChecked()):
            self.itemd.setequipable()
        if(self.radioUsable.isChecked()):
            self.itemd.setusable()
        if(self.checkboxUnique.isChecked()):
            self.itemd.setunique()
        if(self.comboboxCategory.currentIndex()!=0):
            self.itemd.setcategory(self.comboboxCategory.currentText())
        else:
            self.itemd.setcategory()

        return self.itemd


if __name__ == "__main__":
    from sys import argv, exit

    a = QtWidgets.QApplication(argv)
    m = ItemCfgWidget()
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
