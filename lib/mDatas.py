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

class Datas():

    def __init__(self,parent=''):
        self.parent=lra.AppStart() if not parent else parent

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

    def doSaveList(self):
        pass


class RenderCommand():

    def __init__(self,parent):
        self.parent = parent
        self.mApp = mSettings.Configs() if not parent else self.parent.mApp
        self.mIcon = mIcons.Configs() if not parent else self.parent.mIcon
        self.qsup = oplQtSupport.oplQtSupport(self,self.mApp.iconPath)
        self.qcon = oplQtConnection.oplQtConnection(self)
        self.qtbl = oplQtTable.oplQtTable(self)
        self.qlst = oplQtList.oplQtList(self)

    def commandForRtask(self, rtask=None):
        rt = mRenderTask.RenderTask()
        rt = rtask
        exe = self.mApp.mayarenderexefile
        sfile = rt.file
        opt = ''
        for f in rt.flags:
            fv = self._getFlagNVal(f)
            if fv: opt = opt + fv
        return (exe,opt,sfile)

    def _getFlagNVal(self, flags={}):
        if flags['flagShortName'] and flags['value']:
            return ' -%s %s' % (flags['flagShortName'],flags['value'])
        return