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
import winHelp

if 0:
    import lra

class Datas():

    def __init__(self,parent=''):
        print "Initializing background data"
        self.parent=lra.AppStart() if not parent else parent
        self.linkHelp = 'http://code.google.com/p/lra/wiki/UserDocument'
        self.linkIssues = 'http://code.google.com/p/lra/issues/list'

    def doPopulateColumnsList(self):
        print "Columns List"
        lst = self.parent.rtaskSupport.getAllFlagNames()
        items = self.parent.qlst.populate(self.parent.lstColumns,lst,False,True)
        for eachItem in items:
            self.parent.qsup.setIcon(eachItem, self.parent.mIcon.tag)

    def doPrepareColumns(self):
        print "Show/Hide Columns"
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
        print "Save Columns Vis"
        lst = []
        for i in xrange(0,self.parent.lstColumns.count()-1):
            itm = self.parent.lstColumns.item(i)
            if itm.checkState(): lst.append(str(itm.text()))
        self.parent.mApp.colVis=','.join(lst)

    def doLoadColumns(self):
        print "Load Columns Vis"
        vislst = self.parent.mApp.colVis.split(',')
        for i in xrange(0,self.parent.lstColumns.count()-1):
            itm = self.parent.lstColumns.item(i)
            if itm.text() in vislst:
                itm.setCheckState(QtCore.Qt.Checked)
        self.doPrepareColumns()

    def optAbout(self):
        print "Launch About"
        self.widget = QtGui.QWidget()
        win = winAbout.Ui_winAbout()
        win.setupUi(self.widget)
        self.widget.show()

    def optHelp(self):
        print "Launch Help"
        self.widget = QtGui.QWidget()
        win = winHelp.Ui_Form()
        win.setupUi(self.widget)
        self.widget.show()

    def optOnlineHelp(self):
        print "Launch Online Help"
        webbrowser.open(self.linkHelp)

    def optIssues(self):
        print "Launch Issues"
        webbrowser.open(self.linkIssues)

    def optConsoleShow(self):
        print "Launch Console"
        self.parent.cons.show()