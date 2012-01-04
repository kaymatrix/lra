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

class AppLog():

    def __init__(self,parent=''):
        self._prn=lra.AppStart() if not parent else parent
        self.timeStamp=True

    def ready(self):
        data = "System Ready!"
        t=self._prn.mUtil.getDateTime()
        newData = '%s: %s' % (t,data) if self.timeStamp else data
        self._prn.tbStatus.setText(newData)

    def disp(self, data=''):
        t=self._prn.mUtil.getDateTime()
        newData = '%s: %s' % (t,data) if self.timeStamp else data
        oldData = str(self._prn.tbStatus.toPlainText())
        finData = '%s\n%s' % (oldData,newData)
        self._prn.tbStatus.setText(finData)
        self._prn.qsup.scrollTextBox(self._prn.tbStatus)

    def clean(self):
        self.__saveLog()
        self._prn.tbStatus.setText('')
        self.ready()


    def save(self):
        name = self.__saveLog()
        self._prn.qsup.showIformationBox(Message='%s saved!' % name)

    def __saveLog(self):
        fname = '%s.log' % (self._prn.mUtil.getDateTime('%Y%m%d%H%M'))
        data = str(self._prn.tbStatus.toPlainText())
        self._prn.mUtil.fileSaveAdv(self._prn.mApp.appLogsFolder, fname, data)
        return fname

