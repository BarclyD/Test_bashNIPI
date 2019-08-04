from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import numpy as np

class Model(QtCore.QAbstractTableModel):
    # сигнал по изменении и удалении столбцов
    signal_col3Changed = QtCore.pyqtSignal(QtCore.QModelIndex)
    signal_col4Changed = QtCore.pyqtSignal(QtCore.QModelIndex)
    signal_col3Delete = QtCore.pyqtSignal()
    signal_col4Delete = QtCore.pyqtSignal()
    
    def __init__(self, table):
        super().__init__()
        self.table = np.array(table,int)
    def getTable(self):
        return self.table
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.table)
    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.table[0])
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def data(self, index, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return QtCore.QVariant(int(self.table[index.row()][index.column()]))
    # закрашивания столбца 3 если значение меньше 0
        if role == Qt.BackgroundRole and index.column() == 3:
            if int(self.table[index.row()][index.column()]) < 0:
                return QColor(Qt.red)
            elif int(self.table[index.row()][index.column()]) > 0:
                return QColor(Qt.green)
    def my_data(self, index):
        return int(self.table[index.row()][index.column()])
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self.table[index.row()][index.column()] = value
            self.dataChanged.emit(index,index)
# Значения в столбце 1 должны содержать накопленные значения из другого столбца(3)
            if index.column() == 3:
                self.signal_col3Changed.emit(index)
# Значения в одном из столбцов(2) должны пересчитываться из значений в этой же строчке в другом столбце(4)
            if index.column() == 4:
                self.signal_col4Changed.emit(index)
        if role == QtCore.Qt.DisplayRole:
            self.table[index.row()][index.column()] = int(value)
            self.dataChanged.emit(index,index)
        return True
    #Удаление строки
    def insertRows(self, position=1, rows = 1, parent=QtCore.QModelIndex()):
        position = len(self.table)
        #создание массива необходимо длины заполненого 0
        row_to_be_added = np.zeros(len(self.table[0])-1)
        row_to_be_added = np.concatenate((np.array([1],int),row_to_be_added))
        # Добавление строки в массив
        self.table = np.vstack ((self.table, row_to_be_added))
        self.beginInsertRows(parent, position, position + rows - 1)
        self.endInsertRows()
        return True

    #Добавление столбца    
    def insertColumns(self, position=1, rows = 1, parent=QtCore.QModelIndex()):
        column_to_be_added = np.zeros(len(self.table))
        self.table = np.hstack((self.table, np.atleast_2d(column_to_be_added).T))
        self.beginInsertColumns(parent, position, position + rows - 1)
        self.endInsertColumns()
        return True

    #Удаление строчки
    def removeRows(self, position = 1, rows = 1, parent=QtCore.QModelIndex()):
        if len(self.table)-1 > 0:
            position = len(self.table)-1
            self.table = np.delete(self.table, position, axis=0)
            self.beginRemoveRows(parent, position, position + rows - 1)
            self.endRemoveRows()
            return True
        else:
            return False
    #Удаление столбца    
    def removeColumns(self, position = 1, rows = 1, parent=QtCore.QModelIndex()):
        if len(self.table[0]) > 3:
            position = len(self.table[0])-1
            self.table = np.delete(self.table, position, axis=1)
            self.beginRemoveColumns(parent, position, position + rows - 1)
            self.endRemoveColumns()
            if position == 4:
                for i in range(0, len(self.table)):
                    self.signal_col4Delete.emit()
                    
            return True
        else:
            return False
