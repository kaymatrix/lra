from PyQt4 import QtCore, QtGui
from winMain import Ui_MainWindow


class winInterfaceMain(QtGui.QMainWindow, Ui_MainWindow):


    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)


if '__main__' == __name__:
    #import iniConfigReadWrite as ini
    app = QtGui.QApplication(sys.argv)
    ui = winInterfaceMain()
    ui.show()
    z = app.exec_()
    del(app)
    sys.exit(z)