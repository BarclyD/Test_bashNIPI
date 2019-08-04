from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from MyModel import *
import pyqtgraph as pg
import numpy as np
import random
import h5py

class My_table(QtWidgets.QTableView):

    #Слот для изменения столбца 1, содержит накопленные значения из столбца 3(там где выдан сигнал)
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def slot_updateColum1(self,index1):
        index_out = self.model().index(index1.row(),1)
        cur_value = self.model().my_data(index1)
        bef_value = self.model().my_data(index_out)
        slot_value = cur_value + bef_value
        self.model().setData(index_out, slot_value, QtCore.Qt.EditRole)
        
    #Слот для изменения столбца 2
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def slot_updateColum2(self,index1):
        index_out = self.model().index(index1.row(),2)
        #Здесь записывается закон изменения столбца 2 от столбца 4
        slot_value = int(self.model().my_data(index1)) + 2
        self.model().setData(index_out, slot_value, QtCore.Qt.EditRole)

    #Слот для обнуления столбца 2, нужен когда удаляется столбец 4
    @QtCore.pyqtSlot()
    def slot_NulColum2(self):
        for i in range(0, self.model().rowCount()):
            self.model().setData(self.model().index(i,2),0,QtCore.Qt.EditRole)

    #слот для добавления строчки
    @QtCore.pyqtSlot()
    def slot_ButtonRow(self):
        self.model().insertRows()
        self.openPersistentEditor(self.model().index(self.model().rowCount()-1, 0))
    #слот для добавления столбца
    @QtCore.pyqtSlot()
    def slot_ButtonCol(self):
        self.model().insertColumns()
    #слот для заполнения таблицы, начиная со столбца3, случайными значениями
    @QtCore.pyqtSlot()
    def slot_ButtonRan(self):
        for i in range(3, self.model().columnCount()):
            for j in range(0, self.model().rowCount()):
                self.model().setData(self.model().index(j,i), random.randint(-1000,1000), QtCore.Qt.EditRole)
    #слот для удаления строчки
    @QtCore.pyqtSlot()
    def slot_ButtonRowDelete(self):
        self.model().removeRows()
    #слот для удаления столбца
    @QtCore.pyqtSlot()
    def slot_ButtonColDelete(self):
        self.model().removeColumns()

    #сигнал для построения графика
    signalGraph = QtCore.pyqtSignal(np.ndarray, np.ndarray)
    #слот для построения графика при нажатии на кнопку
    @QtCore.pyqtSlot()
    def slot_ButtonGraph(self):
        indList = self.selectedIndexes()
        if len(indList) == (self.model().rowCount()*2):
            col1 = indList[0].column()
            col2=col1
            j=1

            #В цикле ищет второй столбец
            while col2 == col1 and (j < self.model().rowCount()*2):
                col2=indList[j].column()
                j+=1

            #Заполнение двух массивов Х и У
            self.npX = np.array([])
            self.npY = np.array([])
            for i in indList:
                if i.column() == col1:
                    self.npX = np.append(self.npX, [self.model().my_data(i)])
                elif i.column() == col2:
                    self.npY = np.append(self.npY, [self.model().my_data(i)])
                else:
                    print("Выделены не 2 столбца")
                    return
            self.signalGraph.emit(self.npX, self.npY)

    #метод для подключения сигналов и одиночного нажатия по выплывающему списку
    def init_myTable(self):
        self.model().signal_col3Changed.connect(self.slot_updateColum1)
        self.model().signal_col4Changed.connect(self.slot_updateColum2)
        self.model().signal_col4Delete.connect(self.slot_NulColum2)

        for row in range(self.model().rowCount()):
            self.openPersistentEditor(self.model().index(row, 0))

    #Слот для экспорта в DXF файл
    @QtCore.pyqtSlot(bool)
    def slot_ExportDXF(self, checked):
        #вызов диалогового окна
        path, _filter = QtWidgets.QFileDialog.getSaveFileName(self, "Export DXF", "C:\\Users","*.hdf5")
        with h5py.File(path, 'w') as f:
            dset = f.create_dataset('table', data=self.model().getTable())
            f.close()
            
    #Слот для импорта в DXF файл
    @QtCore.pyqtSlot(bool)
    def slot_ImportDXF(self, checked):
        path, _filter = QtWidgets.QFileDialog.getOpenFileName(self, "Import DXF", "C:\\Users","*.hdf5")
        with h5py.File(path, 'r') as f:
           data = f['table']
           nm = np.array
           nm = data[:]
           Mod = Model(nm)
           self.setModel(Mod)
           self.init_myTable()
           f.close()

    #Слот для экспорта в TXT файл
    @QtCore.pyqtSlot(bool)
    def slot_ExportTXT(self, checked):
        path, _filter = QtWidgets.QFileDialog.getSaveFileName(self, "Export TXT", "C:\\Users","*.txt")
        np.savetxt(path, self.model().getTable(), fmt='%1.0f')

    #Слот для импорт в TXT файл
    @QtCore.pyqtSlot(bool)
    def slot_ImportTXT(self, checked):
        path, _filter = QtWidgets.QFileDialog.getOpenFileName(self, "Export TXT", "C:\\Users","*.txt")
        nm = np.array
        nm = np.loadtxt(path)
        Mod = Model(nm)
        self.setModel(Mod)
        self.init_myTable()
