#-------------------------------------------------------------------------------
# Name:        RenderTaskProperties
# Purpose:
#
# Author:      AIAA
#
# Created:     15-12-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import oplPyUtilities
import lra
import oplQtSupport
import oplQtConnection
import oplQtTable
import oplQtList
import oplINIRW
import mIcons
import mSettings
import mRenderTask
import oplQtProcess

import winAbout
import webbrowser



class Datas():

    def __init__(self,parent=''):
        self.parent=lra.AppStart() if not parent else parent
        self.linkHelp = 'http://code.google.com/p/lra/wiki/UserDocument'
        self.linkIssues = 'http://code.google.com/p/lra/issues/list'

    def doPopulateColumnsList(self):
        lst = self.parent.rtaskSupport.getAllFlagNames()
        items = self.parent.qlst.populate(self.parent.lstColumns,lst,False,True)
        for eachItem in items:
            self.parent.qsup.setIcon(eachItem, self.parent.mIcon.tag)

    def doPrepareColumns(self):
        itms = self.parent.qlst.getAllItem(self.parent.lstColumns)
        for itm in itms:
            txt = itm.text()
            chk = itm.checkState()
            cno = self.parent.qtbl.getHeaderColNo(self.parent.tblMainList, txt)
            if chk:
                self.parent.tblMainList.showColumn(cno)
            else:
                self.parent.tblMainList.hideColumn(cno)
        self.parent.qtbl.resizeColumnsEx(self.parent.tblMainList)

    def doSaveColumns(self):
        lst = []
        for i in xrange(0,self.parent.lstColumns.count()-1):
            itm = self.parent.lstColumns.item(i)
            if itm.checkState(): lst.append(str(itm.text()))
        self.parent.mApp.colVis=','.join(lst)

    def doLoadColumns(self):
        vislst = self.parent.mApp.colVis.split(',')
        for i in xrange(0,self.parent.lstColumns.count()-1):
            itm = self.parent.lstColumns.item(i)
            if itm.text() in vislst:
                itm.setCheckState(QtCore.Qt.Checked)
        self.doPrepareColumns()

    def optAbout(self):
        self.widget = QtGui.QWidget()
        win = winAbout.Ui_winAbout()
        win.setupUi(self.widget)
        self.widget.show()

    def optHelp(self):
        webbrowser.open(self.linkHelp)

    def optIssues(self):
        webbrowser.open(self.linkIssues)