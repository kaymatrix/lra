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

class Datas():

    def __init__(self,parent=''):
        self.parent=lra.AppStart() if not parent else parent

    def doPopulateColumnsList(self):
        lst = self.parent.rtaskSupport.getAllFlagNames()
        self.parent.qlst.populate(self.parent.lstColumns,lst,False,True)

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


