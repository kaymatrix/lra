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
import mIcons
import mSettings
import mRenderTask

class AppStart(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        #Defaults - Setup 1
        self.rtaskCols = ['Status','Name','AddedOn']

        #Initializes Variables/Objects
        self.mApp = mSettings.Configs()
        self.mIcon = mIcons.Configs()
        self.qsup = oplQtSupport.oplQtSupport(self,self.mApp.iconPath)
        self.qcon = oplQtConnection.oplQtConnection(self)
        self.qtbl = oplQtTable.oplQtTable(self)
        self.rtaskSupport=mRenderTask.RenderTaskSupport(self.mIcon)

        #Defaults - Setup 2

        #Initial Setups
        self.doConnections()
        self.doUIReDesigns()

    def doUIReDesigns(self):
        self.setWindowTitle(self.mApp.name)

        self.qsup.setIcon(self,self.mIcon.star)
        self.qsup.setIcon(self.btnStartRender, self.mIcon.home)
        self.qsup.setIcon(self.btnPropApply, self.mIcon.apply)
        self.qsup.setIcon(self.actionProperties, self.mIcon.female)
        self.qsup.setIcon(self.actionRenderTasks, self.mIcon.heart)

        self.qtbl.initializing(self.tblMainList,self.rtaskCols)
        self.qtbl.formatting(self.tblMainList,sortingEnabled=True)

        #Inital Settings 1
        self.actionProperties.setChecked(False)

        #Load Layout
        self.qsup.uiLayoutRestore()

    def doConnections(self):
        #Default Connections
        QtCore.QObject.connect(self.btnStartRender, QtCore.SIGNAL("clicked()"), self.sigBtnActions)
        QtCore.QObject.connect(self.tblMainList, QtCore.SIGNAL("itemClicked(QTableWidgetItem*)"), self.sigTblActions)

        #Custom Connections
        self.qcon.connectToDragDropEx(self.tblMainList,self.sigTblDragDrop)
        self.qcon.connectToClose(self,self.sigWinClose)

    def sigTblActions(self, *arg):
        rows = self.qtbl.getSelectedRowNo(self.tblMainList)
        if rows:
            row = rows[0]
            items = self.qtbl.getRowItems(self.tblMainList,row)
            print items

    def sigBtnActions(self, *arg):
        pass

    def sigWinClose(self, *arg):
        self.qsup.uiLayoutSave()
        self.mApp.saveSettings()
        self.mIcon.saveSettings()

    def sigTblDragDrop(self, *arg):
        files = self.qcon.dropEventInfoEx(arg[0])
        for eachFile in files:
            self.doAddNewRTask(eachFile)

    def doAddNewRTask(self, file):
        rtask = mRenderTask.RenderTask(file)
        rowItems = self.qtbl.addRow(self.tblMainList,['',rtask.fileName,rtask.addedOn],1)
        if rowItems[0]:
            item = rowItems[0]
            icon = self.rtaskSupport.getIconForStatus(rtask.status)
            status = self.rtaskSupport.getStatusNameForStatus(rtask.status)
            self.qtbl.setTag(item,'tag',rtask)
            self.qsup.setIcon(item,icon)
            item.setText(status)
        self.qtbl.resizeColumnsEx(self.tblMainList)



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