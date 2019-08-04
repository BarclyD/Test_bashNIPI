from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLineEdit, QLabel
from PyQt5.QtCore import QPoint, QItemSelection
from Delegate import *
from MyTable import *
from MyModel import *
# Модель для работы с HDF-файлом напрямую(недоделал)
#from MyModelWithoutCache import * 
import pyqtgraph as pg
import numpy as np

class Main(QtWidgets.QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent) 

        # Массив для выпадающего списка
        choices = [1, 2, 3, 4, 5]
        # Массив таблицы по умолчанию
        table   = []
        table.append([choices[0], 0, 0, 0, 0])
        table.append([choices[0], 0, 0, 0, 0])
        table.append([choices[0], 0, 0, 0, 0])
        table.append([choices[0], 0, 0, 0, 0])
        # создание модели для таблицы
        self.model = Model(table)

        # создание слоев
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # создание таблицы на основе мадели и расположения
        self.tableView = My_table(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model)

        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Настройка столбцов
        self.tableView.setItemDelegateForColumn(0, Delegate(self,choices))
        self.tableView.setItemDelegateForColumn(1, Delegate_for_col_RO(self))
        self.tableView.setItemDelegateForColumn(2, Delegate_for_col_RO(self))
        self.tableView.setItemDelegateForColumn(3, Delegate_for_table(self))
        self.tableView.setItemDelegateForColumn(4, Delegate_for_table(self))
        # настройка сигналов и combobox
        self.tableView.init_myTable()

        
        self.resize(900, 600)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        #Далее настройка кнопок
        self.ButtonRan = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonRan.setObjectName("ButtonRan")
        self.ButtonRan.clicked.connect(self.tableView.slot_ButtonRan)
        self.horizontalLayout.addWidget(self.ButtonRan)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.ButtonCol = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonCol.setObjectName("ButtonCol")
        self.ButtonCol.clicked.connect(self.tableView.slot_ButtonCol)
        self.horizontalLayout.addWidget(self.ButtonCol)

        self.ButtonRow = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonRow.setObjectName("ButtonRow")
        self.ButtonRow.clicked.connect(self.tableView.slot_ButtonRow)
        self.horizontalLayout.addWidget(self.ButtonRow)

        self.ButtonColDelete = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonColDelete.setObjectName("ButtonColDelete")
        self.ButtonColDelete.clicked.connect(self.tableView.slot_ButtonColDelete)
        self.horizontalLayout.addWidget(self.ButtonColDelete)

        self.ButtonRowDelete = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonRowDelete.setObjectName("ButtonColDelete")
        self.ButtonRowDelete.clicked.connect(self.tableView.slot_ButtonRowDelete)
        self.horizontalLayout.addWidget(self.ButtonRowDelete)

        self.verticalLayout.addLayout(self.horizontalLayout)
        # настройка графика
        self.pyGraph = pg.PlotWidget(self.centralwidget)
        self.pyGraph.setObjectName("pyGraph")
        self.verticalLayout.addWidget(self.pyGraph)
        self.tableView.signalGraph.connect(self.slot_BildGraph)
        
        self.ButtonGraph = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonGraph.setObjectName("ButtonGraph")
        self.ButtonGraph.clicked.connect(self.tableView.slot_ButtonGraph)
        self.verticalLayout.addWidget(self.ButtonGraph)
        #настройка меню окна
        self.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menu)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menu)
        self.menu_3.setObjectName("menu_3")
        self.setMenuBar(self.menuBar)
        self.action_txt = QtWidgets.QAction(self)
        self.action_txt.setObjectName("action_txt")
        self.action_dxf = QtWidgets.QAction(self)
        self.action_dxf.setObjectName("action_dxf")
        self.action_txt_2 = QtWidgets.QAction(self)
        self.action_txt_2.setObjectName("action_txt_2")
        self.action_dxf_2 = QtWidgets.QAction(self)
        self.action_dxf_2.setObjectName("action_dxf_2")
        
        self.action_dxf_2.triggered.connect(self.tableView.slot_ExportDXF)
        self.action_dxf.triggered.connect(self.tableView.slot_ImportDXF)
        self.action_txt_2.triggered.connect(self.tableView.slot_ExportTXT)
        self.action_txt.triggered.connect(self.tableView.slot_ImportTXT)
        
        self.menu_2.addAction(self.action_txt)
        self.menu_2.addAction(self.action_dxf)
        self.menu_3.addAction(self.action_txt_2)
        self.menu_3.addAction(self.action_dxf_2)
        self.menu.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.menu_3.menuAction())
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Test bashNIPI"))
        self.ButtonRan.setText(_translate("MainWindow", "Random"))
        self.ButtonCol.setText(_translate("MainWindow", "Добавить столбец"))
        self.ButtonRow.setText(_translate("MainWindow", "Добавить строку"))
        self.ButtonGraph.setText(_translate("MainWindow", "Построить график"))
        self.ButtonColDelete.setText(_translate("MainWindow", "Удалить столбец"))
        self.ButtonRowDelete.setText(_translate("MainWindow", "Удалить строку"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Импорт таблицы"))
        self.menu_3.setTitle(_translate("MainWindow", "Экспорт таблицы"))
        self.action_txt.setText(_translate("MainWindow", "из txt"))
        self.action_dxf.setText(_translate("MainWindow", "из dxf"))
        self.action_txt_2.setText(_translate("MainWindow", "в txt"))
        self.action_dxf_2.setText(_translate("MainWindow", "в dxf"))
        pass
    
    @QtCore.pyqtSlot(np.ndarray, np.ndarray)
    def slot_BildGraph(self, npX, npY):
        self.pyGraph.clear()
        self.pyGraph.plotItem.plot(npX, npY)
