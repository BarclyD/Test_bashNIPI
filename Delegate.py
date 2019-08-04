from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGridLayout, QWidget, QApplication, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, QPoint, Qt
import numpy as np

# делегат для combobox
class Delegate(QtWidgets.QItemDelegate):
    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices
    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QComboBox(parent)
        for element in self.items:
            self.editor.addItem(str(element))
        return self.editor
    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)
    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.DisplayRole)
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

# делегат для всей остольной таблцы
class Delegate_for_table(QtWidgets.QStyledItemDelegate, QtWidgets.QItemDelegate):
    def __init__(self, owner):
        super().__init__(owner)
    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QLineEdit(parent)
        # ввод только int
        valid = QIntValidator(self.editor)
        self.editor.setValidator(valid)
        return self.editor
    # через делегат закрасить не получилось
    '''
    def paint(self, painter, option, index):
        opt = QtWidgets.QStyleOptionViewItem(option)
        if index.data() > 0:
            # opt.font.setBold(True)
            opt.palette.setColor(DisplayRole, Qt.red)
        super().paint(painter, opt, index)
    '''
    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.EditRole)
        editor.setText(str(value))
    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, QtCore.Qt.EditRole)
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

# делегат для столбцов только для чтения
class Delegate_for_col_RO(QtWidgets.QItemDelegate):
    def __init__(self, owner):
        super().__init__(owner)
    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QLineEdit(parent)
        self.editor.setReadOnly(True)
        return self.editor
    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.EditRole)
        editor.setText(str(value))
    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, QtCore.Qt.EditRole)
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
