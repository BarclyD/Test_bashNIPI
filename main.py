import sys
from MyMainWindow import *
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    app.exec_()
