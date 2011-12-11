#-------------------------------------------------------------------------------
# Name:        lra - Entry Module
# Purpose:
#
# Author:      AIAA
#
# Created:     11-12-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import os

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()


#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()

####Adjust these Parent Folder to reach root folder####
    parentFolder1 = os.path.dirname(currentFolder)
    parentFolder2 = os.path.dirname(parentFolder1)

####Pass parentFolder Level to reach Root folder####
    rootFolder = os.path.dirname(parentFolder2)
    rootFolderParent = os.path.dirname(rootFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                      parentFolder2 + '\lra\trunk',
                      parentFolder2 + '\lra\trunk\lib',
                      parentFolder2 + '\lra\trunk\uis',
                      parentFolder2 + '\opl',
                      ##'F:\PYTHON\LIB',
                     ]

    for modulePath in modulePathList:
        if modulePath not in sys.path:
            if os.path.exists(modulePath):
                sys.path.append(modulePath)


from PyQt4 import QtCore, QtGui
from MainUI import Ui_Dialog


class MainApplication(QtGui.QMainWindow, Ui_Dialog):


    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)


if '__main__' == __name__:
    #import iniConfigReadWrite as ini
    app = QtGui.QApplication(sys.argv)
    ui = MainApplication()
    ui.show()
    z = app.exec_()
    del(app)
    sys.exit(z)
