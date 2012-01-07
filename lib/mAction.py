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
import mRTaskStatus as mrts
import os

if 0:
    import lra

class FinalStage():

    def __init__(self, parent):
        self._prn=lra.AppStart() if not parent else parent
        self._prn.qcon.sigConnect(self._prn.btnTerminate, "clicked()", self._doQuitGame)
        self._prn.qcon.sigConnect(self._prn.btnSkipRender, "clicked()", self._doSkillGameLevel)

        self._mRender = RenderCommand(self._prn)
        self.gameCtrl=None


    def GameOver(self):
        self._prn.mLog.disp("Start render requested!")
        self._doBeforeGameBegins()
        self._chooseATaskStartTheGame()
        self._doAfterGameBegins()

    def _chooseATaskStartTheGame(self, arg=None):
        rt = mRenderTask.RenderTask('')
        rt = self._chooseWhichTaskToStartNow()
        if rt:
            self._prn.mLog.disp("Render started for " + rt.id)

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

            self._prn.mLog.disp("Render progressing for " + rt.id)
            self._doAfterEnteringTheStage(rt)

        else:
            #Seems like all task are done - Close all activity
            self._prn.mLog.disp("All Rendering completed!")
            self._doWonTheGameThenWhat()


    def _chooseWhichTaskToStartNow(self):
        rt = mRenderTask.RenderTask('')
        for rtx in self._prn._getAllRTask():
            if rtx.status == mrts.Waiting:
                return rtx
        return None

    def _doLevelCompleteGoNext(self, rt):
        #Job done, Go take the next job and do it.

        #Before that - Save the log
        #Next Clear the old log window
        #Next Call the main GameStart

        self._doSaveGameRunLog(self.__getFileName(rt))

        if self.gameCtrl._unknownError:
            print "UnkownError"
            self._doWonTheGameThenWhat()

        elif (not self.gameCtrl._terminate and not self.gameCtrl._terminateAll):
            #rt = mRenderTask.RenderTask('')
            self._prn.mLog.disp("Current render completed, moving next!")
            self._prn.tbLog.setPlainText('')
            if rt.status == mrts.Rendering:
                rt.status=mrts.Completed
                rt.completedOn=self._prn.mUtil.getDateTime()
                self._prn.refreshStatus(rt)
            self._chooseATaskStartTheGame(rt)

        elif self.gameCtrl._terminate:
            self._prn.mLog.disp("Terminating current render and moving next!")
            self._prn.tbLog.setPlainText('')
            if rt.status == mrts.Rendering:
                rt.status=mrts.Cancelled
                self._prn.refreshStatus(rt)
            self._chooseATaskStartTheGame(rt)

        elif self.gameCtrl._terminateAll:
            self._prn.mLog.disp("Terminating all render task! Stopping Sytem!")
            #self._prn.tbLog.setText('')
            if rt.status == mrts.Rendering:
                rt.status=mrts.Cancelled
                self._prn.refreshStatus(rt)
            self._doWonTheGameThenWhat()

    def _doAfterEnteringTheStage(self, rt):
        self.__lockForRendering()

    def _doBeforeEnteringTheStage(self, rt):
        pass

    def _doBeforeGameBegins(self):
        self.__lockForRendering()

    def _doWonTheGameThenWhat(self):
        #Release all
        self.__lockForRendering(False)

    def _doAfterGameBegins(self):
        pass

    def _doSkillGameLevel(self):
        if self.gameCtrl:
            if self._prn.qsup.showYesNoBox("Confirm","Are you sure to terminate current task and go to next task?"):
                self.gameCtrl.terminate()

    def _doQuitGame(self):
        if self.gameCtrl:
            if self._prn.qsup.showYesNoBox("Confirm","Are you sure to terminate current task and stop rendering?"):
                self.gameCtrl.terminateAll()

    def _doSaveGameRunLog(self, fileName):
        data = self._prn.tbLog.toPlainText()
        logPath = self._prn.mApp.renderLogsFolder
        if not os.path.exists(logPath): os.makedirs(logPath)
        svFile = os.path.join(logPath,fileName)
        if os.path.exists(logPath):
            self._prn.mUtil.fileSave(data,svFile)
        self._prn.mLog.disp("Render log saved to " + svFile)

    def __getFileName(self, rt):
        return '%s_%s.log' % (rt.id,rt.fileName)

    def __lockForRendering(self, lock=True):
        #Something has to be locked first
        self._prn.btnPropApply.setEnabled(not lock)
        self._prn.btnRTaskLoad.setEnabled(not lock)
        self._prn.btnRTaskSave.setEnabled(not lock)
        self._prn.btnStartRender.setEnabled(not lock)
        self._prn.actionLoad_List.setEnabled(not lock)
        self._prn.actionNew_List.setEnabled(not lock)
        self._prn.actionSave_List.setEnabled(not lock)
        self._prn.btnAddFile.setEnabled(not lock)
        self._prn.btnRemoveFile.setEnabled(not lock)

        self._prn.btnTerminate.setEnabled(lock)
        self._prn.btnSkipRender.setEnabled(lock)

class Execution():

    def __init__(self, prn=None, rTask=None, onProcessCompletes=None, logDisplay=None):

        self._withError=False
        self._terminate=False
        self._terminateAll=False
        self._unknownError=False

        if rTask and prn:
            self._prn = prn
            self._rt = rTask
            self._mRender = RenderCommand(self._prn)
            self._onProcessCompletes = onProcessCompletes
            self._txt = logDisplay
            self._chk = self._prn.cbxAutoScroll
            #Get the Game Command
            Exe,Options,File = self._mRender.commandForRtask(self._rt)
            self._exe = Exe
            self._file = File
            self._args = self._processArguments(Options,File)

            if (self._exe and self._file and
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
                if self._rt.status == mrts.Waiting:
                    self._rt.status = mrts.Rendering
                    self._prn.refreshStatus(self._rt)
            else:
                print "Some problem."
                self._unknownError=True
                self._onProcessCompletes()
        else:
            print "No render task or No UIs given for Execution."
            self._unknownError=True
            self._onProcessCompletes()


    def terminate(self):
        print self._rt.id + " Terminate Triggered!"
        self._terminate=True
        self.prc.terminate()

    def terminateAll(self):
        print self._rt.id + " Terminatie All Triggered!"
        self._terminateAll=True
        self.prc.terminate()

    def _processArguments(self, Options=None, File=None):
        lst = []
        if File:
            args = '%s "%s"' % (Options,File)
            if not type(args) is type([]):
                for arg in args.split():
                    if arg:
                        lst.append(arg)
        return lst

    def _onDataComes(self, data):
        oldData = self._txt.toPlainText()
        self._txt.setPlainText(oldData + '\n' +  data)
        self._autoScroll()

    def _onErrorComes(self, data):
        oldData = self._txt.toPlainText()
        self._txt.setPlainText(oldData + '\n' +  data)
        self._autoScroll()

    def _autoScroll(self):
        if self._chk.isChecked():
            vsb = self._txt.verticalScrollBar()
            vsb.setValue(vsb.maximum())
            self._txt.repaint()


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

        if rt.customCommand:
            opt = opt + '%s %s' % (opt, rt.customCommand)

        return (exe,opt,sfile)

    def _getFlagNVal(self, flags={}):
        if flags['flagShortName'] and flags['value']:
            return ' -%s %s' % (flags['flagShortName'],flags['value'])
        return
