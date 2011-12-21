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
                      parentFolder2 + '/lra',
                      parentFolder2 + '/lra/lib',
                      parentFolder2 + '/lra/uis',
                      parentFolder2 + '/lra/res',
                      parentFolder2 + '/opl',
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
from winSettings import Ui_Dialog
import oplQtSupport
import oplQtConnection
import oplQtTable
import oplQtList
import oplINIRW
import mIcons
import mSettings
import mRenderTask
import mDatas

class winSettings(QtGui.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        #Defaults - Setup 1

        #Initializes Variables/Objects
        self.parent = parent
        self.mApp = mSettings.Configs() if not parent else self.parent.mApp
        self.mIcon = mIcons.Configs() if not parent else self.parent.mIcon
        self.qsup = oplQtSupport.oplQtSupport(self,self.mApp.iconPath)
        self.qcon = oplQtConnection.oplQtConnection(self)
        self.qtbl = oplQtTable.oplQtTable(self)
        self.qlst = oplQtList.oplQtList(self)


##        #Initialize
##        self.initalize()
##
##        #Defaults - Setup 2
##        self.rtaskCols = self.rtaskSupport.getAllFlagNamesWithFixedNames()
##        self.rtaskSupport.rcnt = int(self.mApp.rtcounter)
##
##        #Initial Setups
        self.doConnections()
        self.doUIReDesigns()

    def initalize(self):
        self.groupedWidgets = {
                                self.frmPropFrameRange:[
                                                        self.lePropStartFrame,
                                                        self.lePropEndFrame
                                                       ],
                                self.frmPropProjPath:[
                                                        self.lePropProjPath
                                                     ]
                              }
        self.propWidgets = self.__allPropWidgets()
        self.rtaskSupport.initalizeFlags(self.propWidgets)

    def __allPropWidgets(self):
        ret = []
        for each in self.groupedWidgets.keys():
            ret = ret + self.groupedWidgets[each]
        return ret

    def getFlagParentWidget(self, widget):
        ret = None
        for each in self.groupedWidgets.keys():
            if widget in self.groupedWidgets[each]:
                ret = each
        return ret

    def doUIReDesigns(self):
        #self.setWindowTitle(self.mApp.name)

        #self.qsup.setIcon(self,self.mIcon.app)
        self.qsup.setIcon(self.btnApply, self.mIcon.apply)
        self.qsup.setIcon(self.btnCancel, self.mIcon.cancel)


    def doConnections(self):
        self.qcon.sigConnect(self.btnApply, "clicked()", self.sigBtnActions)
        self.qcon.sigConnect(self.btnCancel, "clicked()", self.sigBtnActions)

    def sigBtnActions(self, *arg):
        sender = self.sender()
        if sender == self.btnApply:
           self.close()

        if sender == self.btnCancel:
           self.close()


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
    ui = winSettings()
    ui.show()
    ec = app.exec_()
    app.closeAllWindows()
    app.exit()
    app.quit()
    del(ui)
    del(app)
    sys.exit(ec)