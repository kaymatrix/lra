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
import mRTaskStatus as mrts
import os


class FinalStage():

    def __init__(self, parent):
        self._prn=lra.AppStart() if not parent else parent
        self._mRender = RenderCommand(self._prn)
        self._prn.qcon.connectToClick(self._prn.btnTerminate, self._doQuitGame)

    def GameOver(self):
        self._doBeforeGameBegins()
        self._chooseATaskStartTheGame()
        self._doAfterGameBegins()

    def _chooseATaskStartTheGame(self, arg=None):
        rt = mRenderTask.RenderTask('')
        rt = self._chooseWhichTaskToStartNow()
        if rt:
            #Got a task to render - Start the render
            self._doBeforeEnteringTheStage(rt)

            #Get the Game Command
            Exe,Options,File = self._mRender.commandForRtask(rt)
            cmdReady = '%s "%s"' % (Options,File) if Exe and File else ''

            if (cmdReady and Exe and File
                 and os.path.exists(Exe)
                 and os.path.exists(File)):
                self.gameCtrl = Execution(
                                prn=self._prn,
                                rTask=rt,
                                onProcessCompletes=self._doLevelCompleteGoNext,
                                logDisplay = self._prn.tbLog
                                )

            self._doAfterEnteringTheStage(rt)
        else:
            #Seems like all task are done - Close all activity
            self._doWonTheGameThenWhat()

    def _chooseWhichTaskToStartNow(self):
        rt = mRenderTask.RenderTask('')
        for rtx in self._prn._getAllRTask():
            if rtx.status == mrts.YetToStart:
                return rtx
        return None

    def _doLevelCompleteGoNext(self, rt):
        #Job done, Go take the next job and do it.

        #Before that - Save the log
        #Next Clear the old log window
        #Next Call the main GameStart

        self._doSaveGameRunLog(self.__getFileName(rt))

        #rt = mRenderTask.RenderTask('')
        self._prn.tbLog.setText('')
        if rt.status == mrts.Rendering:
            rt.status=mrts.RenderedWithNoError
            self._prn.refreshStatus(rt)
        self._chooseATaskStartTheGame(rt)

    def _doAfterEnteringTheStage(self, rt):
        pass

    def _doBeforeEnteringTheStage(self, rt):
        pass

    def _doBeforeGameBegins(self):
        #Something has to be locked first
        self._prn.btnPropApply.setEnabled(False)
        self._prn.btnRTaskLoad.setEnabled(False)
        self._prn.btnRTaskSave.setEnabled(False)
        self._prn.btnStartRender.setEnabled(False)
        self._prn.actionLoad_List.setEnabled(False)
        self._prn.actionNew_List.setEnabled(False)
        self._prn.actionSave_List.setEnabled(False)

        self._prn.btnTerminate.setEnabled(True)

    def _doWonTheGameThenWhat(self):
        #Something has to be locked first
        self._prn.btnPropApply.setEnabled(True)
        self._prn.btnRTaskLoad.setEnabled(True)
        self._prn.btnRTaskSave.setEnabled(True)
        self._prn.btnStartRender.setEnabled(True)
        self._prn.actionLoad_List.setEnabled(True)
        self._prn.actionNew_List.setEnabled(True)
        self._prn.actionSave_List.setEnabled(True)

        self._prn.btnTerminate.setEnabled(False)

    def _doAfterGameBegins(self):
        pass

    def _doQuitGame(self):
        self.gameCtrl.terminate()


    def _doSaveGameRunLog(self, fileName):
        data = self._prn.tbLog.toPlainText()
        logPath = self._prn.mApp.renderLogsFolder
        if not os.path.exists(logPath): os.makedirs(logPath)
        svFile = os.path.join(logPath,fileName)
        if os.path.exists(logPath):
            self._prn.mUtil.fileSave(data,svFile)

    def __getFileName(self, rt):
        return '%s_%s.log' % (rt.id,rt.fileName)


class Execution():

    def __init__(self, prn=None, rTask=None, onProcessCompletes=None, logDisplay=None):

        self._withError=False

        if rTask and prn:
            self._prn = prn
            self._rt = rTask
            self._mRender = RenderCommand(self._prn)
            self._onProcessCompletes = onProcessCompletes
            self._txt = logDisplay
            #Get the Game Command
            Exe,Options,File = self._mRender.commandForRtask(self._rt)
            self._exe = Exe
            self._file = File
            self._args = self._processArguments(Options,File)

            if (self._exe and self._args and self._file and
                os.path.exists(self._exe) and
                os.path.exists(self._file)):
                self.prc = oplQtProcess.Process(self._exe,
                                                self._args,
                                                self._onDataComes,
                                                self._onErrorComes,
                                                self._onCompletion
                                                )
                self.prc.execute()
                print self._rt.id + " Started!"
                if self._rt.status == mrts.YetToStart:
                    self._rt.status = mrts.Rendering
                    self._prn.refreshStatus(self._rt)
        else:
            print "No render task or No UIs given for Execution."

    def terminate(self):
        print self._rt.id + " Terminate Triggered!"
        self.prc.terminate()

    def _processArguments(self, Options=None, File=None):

        lst = []
        if Options and File:
            args = '%s "%s"' % (Options,File)
            if not type(args) is type([]):
                for arg in args.split():
                    if arg:
                        lst.append(arg)
        return lst


    def _onDataComes(self, data):
        oldData = self._txt.toPlainText()
        self._txt.setText(oldData + '\n' +  data)
        vsb = self._txt.verticalScrollBar()
        vsb.setValue(vsb.maximum())

    def _onErrorComes(self, data):
        oldData = self._txt.toPlainText()
        self._txt.setText(oldData + '\n' +  data)
        vsb = self._txt.verticalScrollBar()
        vsb.setValue(vsb.maximum())

    def _onCompletion(self, data):
        print self._rt.id + " Completed!"
        self._onProcessCompletes(self._rt)

class RenderCommand():

    def __init__(self,parent):
        self.parent=lra.AppStart() if not parent else parent
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
