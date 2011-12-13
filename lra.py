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
                      parentFolder1 + '/lra',
                      parentFolder1 + '/lra/lib',
                      parentFolder1 + '/lra/uis',
                      parentFolder1 + '/lra/res',
                      parentFolder1 + '/opl',
                      ##'F:\PYTHON\LIB',
                     ]

    for modulePath in modulePathList:
        if os.path.abspath(modulePath) not in sys.path:
            if os.path.exists(modulePath):
                sys.path.append(os.path.abspath(modulePath))

#Main Modules
from PyQt4 import QtCore, QtGui
import sip

#Custom Modules
from winMain import Ui_MainWindow
import oplQtSupport
import oplQtConnection
import oplQtTable
import clsIcons

class AppStart(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        #Defaults
        self.appName = "Render Assistant"
        self.iconPath = r"F:\Kumaresan\Dev\Python\lra\res\icons"

        #Initializes Variables/Objects
        self.qsup = oplQtSupport.oplQtSupport(self,self.iconPath)
        self.qcon = oplQtConnection.oplQtConnection(self)
        self.qtbl = oplQtTable.oplQtTable(self)
        self.icon = clsIcons.Icons(self.iconPath)

        #Initial Setups
        self.doConnections()
        self.doUIReDesigns()

    def doUIReDesigns(self):
        self.setWindowTitle(self.appName)
        self.qsup.setIcon(self,self.icon.star)
        self.qsup.setIcon(self.btnStartRender, self.icon.info)
        self.qtbl.initializing(self.tblMainList,["FileName"])
        self.qtbl.formatting(self.tblMainList)

        #Load Layout
        self.qsup.uiLayoutRestore()

    def doConnections(self):
        #Default Connections
        QtCore.QObject.connect(self.btnStartRender, QtCore.SIGNAL("clicked()"), self.btnActions)

        #Custom Connections
        self.qcon.connectToDragDropEx(self.tblMainList,self.tblDragDrop)
        self.qcon.connectToClose(self,self.doOnClose)

    def btnActions(self, *arg):
        pass

    def tblDragDrop(self, event):
        files = self.qcon.dropEventInfoEx(event)
        for eachFile in files:
            self.qtbl.addRow(self.tblMainList,[eachFile],1)

    def doOnClose(self, *eve):
        self.qsup.uiLayoutSave()






if '__main__' == __name__:
    try:
        sip.delete(app)
    except:
        try:
            del(app)
        except:
            pass

    inst = QtGui.QApplication.instance()
    if inst:
        inst.exit()
        inst.quit()
        del(inst)

    app = QtGui.QApplication(sys.argv)
    ui = AppStart()
    ui.show()
    ec = app.exec_()
    app.closeAllWindows()
    app.exit()
    app.quit()
    del(ui)
    del(app)
    sys.exit(ec)