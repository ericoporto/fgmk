
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import current_project, fifl, actions_wdgt
from fgmk.ff import item_format

class EffectWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        #elements
        titleLabel = QtWidgets.QLabel('effect of usable item')
        self.effectsCombobox = QtWidgets.QComboBox(self)
        self.basepSpinbox = QtWidgets.QSpinBox(self)
        self.plusSpinbox = QtWidgets.QSpinBox(self)
        self.atrCombobox = QtWidgets.QComboBox(self)
        basepLabel = QtWidgets.QLabel('roll (modifier')
        atrLabel = QtWidgets.QLabel('+ attribute')
        plusLabel = QtWidgets.QLabel(') + modifier')

        #starting elements
        for i in range(len(item_format.effects_types)):
            effect = item_format.effects_types[i]
            self.effectsCombobox.insertItem(i,effect)
        for i in range(len(item_format.atr_types)):
            atr = item_format.atr_types[i]
            self.atrCombobox.insertItem(i,atr)
        self.basepSpinbox.setToolTip('Modifier based on selected atribute.')
        self.basepSpinbox.setMinimum(-10)
        self.basepSpinbox.setMaximum(10)
        self.basepSpinbox.setSingleStep(1)
        self.plusSpinbox.setToolTip('Value to add on resulting roll of atribute and modifier.')
        self.plusSpinbox.setMinimum(-10)
        self.plusSpinbox.setMaximum(10)
        self.plusSpinbox.setSingleStep(1)
        self.setEnableOthers(False)

        #logic
        self.effectsCombobox.currentIndexChanged.connect(self.effectsChanged)

        #layout
        titleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        basepLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        plusLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        atrLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        VBox = QtWidgets.QVBoxLayout(self)
        HBox1 = QtWidgets.QHBoxLayout()
        HBox2 = QtWidgets.QHBoxLayout()
        HBox1.addWidget(titleLabel)
        HBox1.addWidget(self.effectsCombobox)
        HBox2.addWidget(basepLabel)
        HBox2.addWidget(self.basepSpinbox)
        HBox2.addWidget(atrLabel)
        HBox2.addWidget(self.atrCombobox)
        HBox2.addWidget(plusLabel)
        HBox2.addWidget(self.plusSpinbox)
        VBox.addLayout(HBox1)
        VBox.addLayout(HBox2)

    def effectsChanged(self,index):
        notzero = index != 0
        self.setEnableOthers(notzero)

    def setEnableOthers(self,abool):
        self.basepSpinbox.setEnabled(abool)
        self.atrCombobox.setEnabled(abool)
        self.plusSpinbox.setEnabled(abool)

    def clearOthers(self):
        self.basepSpinbox.setValue(0)
        self.atrCombobox.setCurrentIndex(0)
        self.plusSpinbox.setValue(0)

    def setValue(self,effect_json=item_format.default_effect):
        if(effect_json==item_format.default_effect or effect_json == {}):
            self.clearOthers()
            self.effectsCombobox.setCurrentIndex(0)
            return

        if('basep' in effect_json):
            self.basepSpinbox.setValue(effect_json['basep'])
        else:
            self.basepSpinbox.setValue(0)

        if('plus' in effect_json):
            self.plusSpinbox.setValue(effect_json['plus'])
        else:
            self.plusSpinbox.setValue(0)

        if('atr' in effect_json):
            atr_index = item_format.atr_types.index(effect_json['atr'])
            self.atrCombobox.setCurrentIndex(atr_index)
        else:
            self.atrCombobox.setCurrentIndex(0)

        if('effect' in effect_json):
            effect_index = item_format.effects_types.index(effect_json['effect'][0])
            self.effectsCombobox.setCurrentIndex(effect_index)
        else:
            self.clearOthers()
            self.effectsCombobox.setCurrentIndex(0)

    def getValue(self):
        if(self.effectsCombobox.currentIndex()==0):
            return item_format.default_effect

        effect_json = {}

        effect = self.effectsCombobox.currentText()
        basep = self.basepSpinbox.value()
        plus = self.plusSpinbox.value()
        atr = self.atrCombobox.currentText()

        if(self.atrCombobox.currentIndex()==0 and basep == 0 and plus == 0):
            return item_format.default_effect

        if basep != 0:
            effect_json['basep']=basep
        if plus != 0:
            effect_json['plus']=plus
        if atr != item_format.atr_types[0]:
            effect_json['atr']=atr

        effect_json['effect']=[]
        effect_json['effect'].append(effect)

        return effect_json



class StatModWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)
        #elements
        titleLabel = QtWidgets.QLabel('stat modification')
        self.clearButton = QtWidgets.QPushButton('clear all',self)
        self.stSpinbox = QtWidgets.QSpinBox(self)
        self.dxSpinbox = QtWidgets.QSpinBox(self)
        self.iqSpinbox = QtWidgets.QSpinBox(self)
        stLabel = QtWidgets.QLabel('st')
        dxLabel = QtWidgets.QLabel('dx')
        iqLabel = QtWidgets.QLabel('iq')

        #logic
        self.clearButton.clicked.connect(self.clearAll)
        self.stSpinbox.setToolTip('How much the item will modify strenght.')
        self.stSpinbox.setMinimum(-250)
        self.stSpinbox.setMaximum(250)
        self.stSpinbox.setSingleStep(1)
        self.dxSpinbox.setToolTip('How much the item will modify dexterity.')
        self.dxSpinbox.setMinimum(-250)
        self.dxSpinbox.setMaximum(250)
        self.dxSpinbox.setSingleStep(1)
        self.iqSpinbox.setToolTip('How much the item will modify intelligence.')
        self.iqSpinbox.setMinimum(-250)
        self.iqSpinbox.setMaximum(250)
        self.iqSpinbox.setSingleStep(1)

        #layout and appearance
        titleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        stLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        dxLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        iqLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        VBox = QtWidgets.QVBoxLayout(self)
        statsHBox = QtWidgets.QHBoxLayout()
        statsHBox.addWidget(stLabel)
        statsHBox.addWidget(self.stSpinbox)
        statsHBox.addWidget(dxLabel)
        statsHBox.addWidget(self.dxSpinbox)
        statsHBox.addWidget(iqLabel)
        statsHBox.addWidget(self.iqSpinbox)
        titleHBox = QtWidgets.QHBoxLayout()
        titleHBox.addWidget(titleLabel)
        titleHBox.addWidget(self.clearButton)
        VBox.addLayout(titleHBox)
        VBox.addLayout(statsHBox)

    def clearAll(self):
        self.stSpinbox.setValue(0)
        self.dxSpinbox.setValue(0)
        self.iqSpinbox.setValue(0)

    def setValue(self,stat={'st':0,'dx':0,'iq':0}):
        if stat == item_format.default_statMod:
            self.clearAll()
            return

        if 'st' in stat:
            self.stSpinbox.setValue(stat['st'])
        else:
            self.stSpinbox.setValue(0)

        if 'dx' in stat:
            self.dxSpinbox.setValue(stat['dx'])
        else:
            self.dxSpinbox.setValue(0)

        if 'iq' in stat:
            self.iqSpinbox.setValue(stat['iq'])
        else:
            self.iqSpinbox.setValue(0)

    def getValue(self):
        stat = {}
        st = self.stSpinbox.value()
        dx = self.dxSpinbox.value()
        iq = self.iqSpinbox.value()
        if st != 0:
            stat['st']=st
        if dx != 0:
            stat['dx']=st
        if iq != 0:
            stat['iq']=iq

        if('st' in stat or 'dx' in stat or 'iq' in stat):
            return stat
        else:
            return item_format.default_statMod


class ItemCfgWidget(QtWidgets.QWidget):
    def __init__(self, itemd=None, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent
        if(itemd==None):
            self.itemd = item_format.base_item('')
        else:
            self.itemd = itemd

        VBox = QtWidgets.QVBoxLayout(self)

        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setMaxLength(22)
        self.radioEquipable = QtWidgets.QRadioButton('equipable',self)
        self.radioUsable = QtWidgets.QRadioButton('usable', self)
        self.radioNone = QtWidgets.QRadioButton('none', self)
        self.checkboxUnique =  QtWidgets.QCheckBox('unique', self)
        self.checkboxReusable =  QtWidgets.QCheckBox('reusable', self)
        self.descriptionLineEdit = QtWidgets.QLineEdit(self)
        self.comboboxCategory = QtWidgets.QComboBox(self)

        self.statModWidget = StatModWidget(self)
        self.effectWidget = EffectWidget(self)
        self.actionWidget = actions_wdgt.tinyActionsWdgt(parent=self,
                                                         ssettings=current_project.settings,
                                                         nothis=True,
                                                         isitem=True)

        self.actionWidget.setEnabled(False)
        self.statModWidget.setEnabled(False)
        self.effectWidget.setEnabled(False)
        self.checkboxReusable.setEnabled(False)

        self.radioUsable.toggled.connect(self.radioUsableChanged)
        self.radioEquipable.toggled.connect(self.radioEquipableChanged)

        for i in range(len(item_format.item_categories)):
            category = item_format.item_categories[i]
            self.comboboxCategory.insertItem(i,category)

        self.loadItem()

        VBox.addWidget(QtWidgets.QLabel('Item name:'))
        VBox.addWidget(self.nameLineEdit)
        VBox.addWidget(QtWidgets.QLabel('Item properties:'))
        VBox.addWidget(self.radioEquipable)
        VBox.addWidget(self.radioUsable)
        VBox.addWidget(self.radioNone)
        VBox.addWidget(self.checkboxUnique)
        VBox.addWidget(self.checkboxReusable)
        VBox.addWidget(QtWidgets.QLabel('Item description:'))
        VBox.addWidget(self.descriptionLineEdit)
        VBox.addWidget(QtWidgets.QLabel('Item category:'))
        VBox.addWidget(self.comboboxCategory)
        VBox.addWidget(self.statModWidget)
        VBox.addWidget(self.effectWidget)
        VBox.addWidget(self.actionWidget)

    def radioUsableChanged(self,isusable):
        self.actionWidget.setEnabled(isusable)
        self.effectWidget.setEnabled(isusable)
        self.checkboxReusable.setEnabled(isusable)

    def radioEquipableChanged(self,abool):
        self.statModWidget.setEnabled(abool)

    def newItem(self):
        self.itemd = item_format.base_item('')
        self.loadItem()

    def loadItem(self,item=None):
        if(item!=None):
            self.itemd = item

        self.nameLineEdit.setText(self.itemd.name)
        self.descriptionLineEdit.setText(self.itemd.description)
        self.radioNone.setChecked(True)
        if(self.itemd.equipable != item_format.default_equipable):
            self.radioEquipable.setChecked(True)

        if(self.itemd.usable != item_format.default_usable):
            self.radioUsable.setChecked(True)
        if(self.itemd.unique != item_format.default_unique):
            self.checkboxUnique.setChecked(True)
        else:
            self.checkboxUnique.setChecked(False)

        if(self.itemd.reusable != item_format.default_reusable):
            self.checkboxReusable.setChecked(True)
        else:
            self.checkboxReusable.setChecked(False)

        self.comboboxCategory.setCurrentIndex(0)
        if(self.itemd.category != item_format.default_category):
            category_index = item_format.item_categories.index(self.itemd.category)
            self.comboboxCategory.setCurrentIndex(category_index)

        if(self.itemd.action != item_format.default_action):
            self.actionWidget.setList(self.itemd.action)
        else:
            self.actionWidget.setList([])

        if(self.itemd.statMod != item_format.default_statMod):
            self.statModWidget.setValue(self.itemd.statMod)
        else:
            self.statModWidget.setValue(item_format.default_statMod)

        if(self.itemd.effect != item_format.default_effect):
            self.effectWidget.setValue(self.itemd.effect)
        else:
            self.effectWidget.setValue(item_format.default_effect)

    def getItem(self,item=None):
        if(item!=None):
            self.itemd = item

        self.itemd.setname(self.nameLineEdit.text())
        self.itemd.setdescription(self.descriptionLineEdit.text())

        if(self.statModWidget.getValue() == item_format.default_statMod):
            self.itemd.setstatmod()
        else:
            self.itemd.setstatmod(self.statModWidget.getValue())

        if(self.effectWidget.getValue() == item_format.default_effect):
            self.itemd.seteffect()
        else:
            self.itemd.seteffect(self.effectWidget.getValue())

        if(self.actionWidget.getValue() == []):
            self.itemd.setaction()
        else:
            self.itemd.setaction(self.actionWidget.getValue())

        if(self.checkboxReusable.isChecked()):
            self.itemd.setreusable(True)
        else:
            self.itemd.setreusable(False)

        if(self.radioEquipable.isChecked()):
            self.itemd.setequipable(True)
            self.itemd.setaction()
            self.itemd.seteffect()
            self.itemd.setreusable(False)
        else:
            self.itemd.setequipable(False)

        if(self.radioUsable.isChecked()):
            self.itemd.setusable(True)
            self.itemd.setstatmod()
        else:
            self.itemd.setusable(False)

        if(self.checkboxUnique.isChecked()):
            self.itemd.setunique(True)
        else:
            self.itemd.setunique(False)


        if(self.comboboxCategory.currentIndex()!=0):
            self.itemd.setcategory(self.comboboxCategory.currentText())
        else:
            self.itemd.setcategory()

        return self.itemd

class ItemsList(QtWidgets.QWidget):
    currentItemChanged = QtCore.pyqtSignal(object, 'QString')
    def __init__(self,itemsfname=None, parent=None, ssettings={}, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.itemf = item_format.ItemsFormat(os.path.join(current_project.settings['gamefolder'],fifl.ITEMSFILE))
        self.itemsList = QtWidgets.QListWidget(self)
        self.itemsList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.itemsList.currentItemChanged.connect(self.currentChanged)

        self.load(itemsfname)
        VBox = QtWidgets.QVBoxLayout(self)
        VBox.addWidget(self.itemsList)
        self.setLayout(VBox)

    def getFileName(self):
        return self.itemf.filename

    def new(self):
        self.itemf.new()
        self.load()

    def load(self,itemsfname=None):
        self.itemsList.clear()
        if(itemsfname != None):
            self.itemf.load(itemsfname)

        items = self.itemf.getitemsname()
        for i in range(len(items)):
            item = items[i]
            self.itemsList.addItem(item)

    def newItem(self):
        item = item_format.base_item('newItem')
        needsrefresh = self.itemf.additem(item)
        if(needsrefresh):
            self.load()

        items = self.itemf.getitemsname()
        for i in range(len(items)):
            itemname = items[i]
            if(itemname=='newItem'):
                self.itemsList.setCurrentRow(i)
                return

    def saveItem(self,item):
        needsrefresh = self.itemf.additem(item)
        if(needsrefresh):
            self.load()

    def removeByName(self,itemname):
        self.itemf.removebyname(itemname)
        self.load()

    def save(self,filename=None):
        if(filename!=None):
            self.itemf.save(filename)
        else:
            self.itemf.save()

    def currentItem(self):
        listitem = self.itemsList.currentItem()
        if(listitem != None):
            return listitem.text()
        else:
            return None

    def getCurrentItemDescriptor(self):
        itemname = self.currentItem()
        if(itemname!=None):
            itemjson = self.itemf.getitem(itemname)
            item = item_format.base_item(itemname,jsonTree=itemjson)
            return item

    def currentChanged(self,current,previous):
        if(current == previous):
            return

        previousname = ''
        if(previous != None):
            previousname = previous.text()

        if(current != None):
            itemname = current.text()
            itemjson = self.itemf.getitem(itemname)
            item = item_format.base_item(itemname,jsonTree=itemjson)
            self.currentItemChanged.emit(item,previousname)

class itemsEditorWidget(QtWidgets.QDialog):
    def __init__(self,itemsfname=None, parent=None, ssettings={}, **kwargs):
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.parent = parent

        self.itemsList = ItemsList(itemsfname)
        self.itemsList.currentItemChanged.connect(self.itemChanged)
        self.itemCfg = ItemCfgWidget()

        LVBox = QtWidgets.QVBoxLayout()
        if(parent==None):
            self.toolbarMain = QtWidgets.QToolBar()
            self.toolbarMain.addAction("new\nitems.json",self.newItems)
            self.toolbarMain.addAction("open\nitems.json", self.openItems)
            self.toolbarMain.addAction("save\nitems.json", self.saveItems)
            LVBox.addWidget(self.toolbarMain)
        else:
            self.toolbarMain = QtWidgets.QToolBar()
            self.toolbarMain.addAction("save items", self.saveItems)
            self.toolbarMain.addAction("reopen", self.reopenItems)
            LVBox.addWidget(self.toolbarMain)

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.addAction("+new",self.newItem)
        self.toolbar.addAction("-delete", self.deleteItem)
        self.toolbar.addAction("save", self.saveCurrentItem)
        self.toolbar.addAction("reload", self.reloadCurrentItem)
        LVBox.addWidget(self.toolbar)

        LVBox.addWidget(self.itemsList)

        HBox = QtWidgets.QHBoxLayout(self)
        HBox.addLayout(LVBox)
        HBox.addWidget(self.itemCfg)

    def newItem(self):
        self.itemsList.newItem()

    def deleteItem(self):
        itemname = self.itemsList.currentItem()
        if(itemname != None):
            self.itemsList.removeByName(itemname)

    def saveCurrentItem(self):
        itemname = self.itemsList.currentItem()
        item = self.itemCfg.getItem()
        if(item.name == itemname):
            self.itemsList.saveItem(item)
        else:
            self.itemsList.removeByName(itemname)
            self.itemsList.saveItem(item)

    def reloadCurrentItem(self):
        currentItem = self.itemsList.getCurrentItemDescriptor()
        self.itemCfg.loadItem(currentItem)

    def saveNewItem(self):
        item = self.itemCfg.getItem()
        self.itemsList.saveItem(item)

    def itemChanged(self,currentItem,previousName):
        if(previousName!=None and previousName != ''):
            item = self.itemCfg.getItem()
            if(item.name == previousName):
                self.itemsList.saveItem(item)
            else:
                self.itemsList.removeByName(previousName)
                self.itemsList.saveItem(item)

        if(currentItem!=None):
            self.itemCfg.loadItem(currentItem)
            self.itemCfg.setEnabled(True)
        else:
            self.itemCfg.setEnabled(False)

    def newItems(self):
        self.itemsList.new()

    def reopenItems(self):
        filetoreopen = os.path.join(current_project.settings['gamefolder'], fifl.ITEMSFILE)
        self.itemsList.load(filetoreopen)

    def openItems(self):
        folder_to_open_to=''
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.DESCRIPTORS)

        filename = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        folder_to_open_to,
                        "JSON Items (items.json);;All Files (*)")[0]
        if(filename!=''):
            self.itemsList.load(filename)

    def saveItems(self,filename=''):
        if(filename==''):
            filename = self.itemsList.getFileName()

        if os.path.exists(os.path.dirname(filename)):
            self.saveCurrentItem()
            self.itemsList.save(filename)
        else:
            self.saveItemsAs()

    def saveItemsAs(self):
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.DESCRIPTORS)

        filename, extension = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', folder_to_open_to, 'JSON Items (items.json)')

        if filename != "":
            if filename[-10:] != 'items.json':
                filename = os.path.join(os.path.dirname(filename),'items.json')

            self.saveItems(filename)


def main(filelist=None):
    filetoopen=None

    if (isinstance(filelist, str)):
        if ("items.json" in filelist):
            filetoopen = filelist

    else:
        matching = [s for s in filelist if "items.json" in s]
        if len(matching) > 0:
            filetoopen = matching[0]

    if(filetoopen==None):
        return itemsEditorWidget()
    else:
        current_project.settings['gamefolder'] = os.path.join(os.path.dirname(filetoopen),'../')
        return itemsEditorWidget(itemsfname=filetoopen)

if __name__ == "__main__":
    from sys import argv, exit

    a = QtWidgets.QApplication(argv)
    m = main(argv)
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())
