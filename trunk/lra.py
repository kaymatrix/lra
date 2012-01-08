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
import oplQtList
import oplINIRW
import oplPyUtilities
import mIcons
import mSettings
import mRenderTask
import mDatas
import mAction
import mAppLog
import winSettingsInterface

class AppStart(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        #Defaults - Setup 1

        #Initializes Variables/Objects
        self.mApp = mSettings.Configs()
        self.mIcon = mIcons.Configs()
        self.qsup = oplQtSupport.oplQtSupport(self,self.mApp.iconPath)
        self.qcon = oplQtConnection.oplQtConnection(self)
        self.qtbl = oplQtTable.oplQtTable(self)
        self.qlst = oplQtList.oplQtList(self)
        self.mUtil = oplPyUtilities.oplPyUtilities()
        self.mLog = mAppLog.AppLog(self)

        self.winSetting = winSettingsInterface.winSettings(self)

        self.rtaskSupport=mRenderTask.RenderTaskSupport(self, self.mIcon)
        self.mData = mDatas.Datas(self)

        #Initialize
        self.initalize()

        #Defaults - Setup 2
        self.rtaskCols = self.rtaskSupport.getAllFlagNamesWithFixedNames()
        self.rtaskSupport.rcnt = int(self.mApp.rtcounter)

        #Initial Setups
        self.doConnections()
        self.doUIReDesigns()

        #Defaults - Setup 3
        self.fin = mAction.FinalStage(self)
        self.mLog.ready()




    def initalize(self):
        self.groupedWidgets = {
                                self.frmPropFrameRange:[
                                                        self.lePropStartFrame,
                                                        self.lePropEndFrame
                                                       ],
                                self.frmPropProjPath:[
                                                        self.lePropProjPath
                                                     ],
                                self.frmPropFrameAttribs:[
                                                        self.lePropByFrame,
                                                        self.lePropPadding,
                                                     ],
                                self.frmPropRDPath:[
                                                        self.lePropRDPath
                                                     ],
                                self.frmPropOutputFormat:[
                                                        self.lePropOFPath
                                                     ],
                                self.frmPropCam:[
                                                        self.lePropCamAlpha,
                                                        self.lePropCamRGB,
                                                        self.lePropCamDepth,
                                                     ],
                                self.frmPropResAbs:[
                                                        self.lePropXRes,
                                                        self.lePropYRes
                                                     ],
                                self.frmPropResPercentage:[
                                                        self.lePropPercRes
                                                     ],
                                self.frmPropRenderLayer:[
                                                        self.lePropRenderLayer
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
        self.setWindowTitle(self.mApp.name)

        self.qsup.setIcon(self,self.mIcon.app)
        self.qsup.setIcon(self.btnStartRender, self.mIcon.startrender)
        self.qsup.setIcon(self.btnPropApply, self.mIcon.apply)
        self.qsup.setIcon(self.btnRTaskLoad, self.mIcon.load)
        self.qsup.setIcon(self.btnRTaskSave, self.mIcon.save)
        self.qsup.setIcon(self.btnTerminate, self.mIcon.stop)
        self.qsup.setIcon(self.btnSkipRender, self.mIcon.skip)
        self.qsup.setIcon(self.btnAddFile, self.mIcon.plus)
        self.qsup.setIcon(self.btnRemoveFile, self.mIcon.minus)

        self.qsup.setIcon(self.btnSearchAppLog, self.mIcon.search)
        self.qsup.setIcon(self.btnSearchRenderLog, self.mIcon.search)
        self.qsup.setIcon(self.btnSearchRenderTask, self.mIcon.search)

        self.qsup.setIcon(self.btnMoveUp, self.mIcon.up)
        self.qsup.setIcon(self.btnMoveDown, self.mIcon.down)

        self.qsup.setIcon(self.btnLogSave, self.mIcon.save)
        self.qsup.setIcon(self.btnLogClear, self.mIcon.new)

        self.qsup.setIcon(self.actionProperties, self.mIcon.properties)
        self.qsup.setIcon(self.actionRenderTasks, self.mIcon.rendertask)
        self.qsup.setIcon(self.actionColumns, self.mIcon.columns)
        self.qsup.setIcon(self.actionLog, self.mIcon.log)

        self.qsup.setIcon(self.actionNew_List, self.mIcon.new)
        self.qsup.setIcon(self.actionLoad_List, self.mIcon.load)
        self.qsup.setIcon(self.actionSave_List, self.mIcon.save)
        self.qsup.setIcon(self.actionQuit, self.mIcon.quit)
        self.qsup.setIcon(self.actionSettings, self.mIcon.settings)
        self.qsup.setIcon(self.actionHelp, self.mIcon.help)
        self.qsup.setIcon(self.actionReportIssues, self.mIcon.redflag)
        self.qsup.setIcon(self.actionAbout_lra, self.mIcon.about)

        self.qtbl.initializing(self.tblMainList,self.rtaskCols)
        self.qtbl.formatting(self.tblMainList,sortingEnabled=True)

        #Inital Settings 1
        self.actionProperties.setChecked(False)
        self.actionColumns.setChecked(False)

        self.btnRTaskSave.setEnabled(False)
        self.btnStartRender.setEnabled(False)
        self.btnSkipRender.setEnabled(False)
        self.btnTerminate.setEnabled(False)
        self.actionNew_List.setEnabled(False)
        self.actionSave_List.setEnabled(False)

        self.btnRTaskLoad.setEnabled(True)
        self.actionLoad_List.setEnabled(True)

        #Initial Populates
        self.mData.doPopulateColumnsList()
        self.mData.doPrepareColumns()

        #Load Layout
        self.qsup.uiLayoutRestore()

        #Columns Visibity Load
        self.mData.doLoadColumns()

        #Temp
        self.leSearchAppLog.setVisible(0)
        self.leSearchRenderLog.setVisible(0)
        self.leSearchRenderTask.setVisible(0)
        self.btnSearchAppLog.setVisible(0)
        self.btnSearchRenderLog.setVisible(0)
        self.btnSearchRenderTask.setVisible(0)

    def doConnections(self):
        self.qcon.sigConnect(self.btnStartRender, "clicked()", self.sigBtnActions)
        self.qcon.sigConnect(self.btnPropApply, "clicked()", self.sigBtnActions)
        self.qcon.sigConnect(self.btnRTaskLoad, "clicked()", self.sigBtnActions)
        self.qcon.sigConnect(self.btnRTaskSave, "clicked()", self.sigBtnActions)

        self.qcon.sigConnect(self.btnMoveDown, "clicked()", self.sigBtnActions)
        self.qcon.sigConnect(self.btnMoveUp, "clicked()", self.sigBtnActions)

        self.qcon.sigConnect(self.btnAddFile, "clicked()", self.sigBtnActions)
        self.qcon.sigConnect(self.btnRemoveFile, "clicked()", self.sigBtnActions)

        self.qcon.sigConnect(self.btnLogClear, "clicked()", self.sigBtnActions)
        self.qcon.sigConnect(self.btnLogSave, "clicked()", self.sigBtnActions)

        self.qcon.sigConnect(self.tblMainList, "clicked(QModelIndex)", self.sigTblActions)
        self.qcon.sigConnect(self.tblMainList, "itemSelectionChanged ()", self.sigTblActions)
        self.qcon.sigConnect(self.lstColumns, "itemClicked(QListWidgetItem*)", self.sigLstActions)

        self.qcon.sigConnect(self.actionNew_List, "triggered()", self.sigActions)
        self.qcon.sigConnect(self.actionLoad_List, "triggered()", self.sigActions)
        self.qcon.sigConnect(self.actionSave_List, "triggered()", self.sigActions)
        self.qcon.sigConnect(self.actionQuit, "triggered()", self.sigActions)
        self.qcon.sigConnect(self.actionSettings, "triggered()", self.sigActions)
        self.qcon.sigConnect(self.actionAbout_lra, "triggered()", self.sigActions)
        self.qcon.sigConnect(self.actionHelp, "triggered()", self.sigActions)
        self.qcon.sigConnect(self.actionReportIssues, "triggered()", self.sigActions)

        self.qcon.connectDockAndAction(self.dckLog, self.actionLog)
        self.qcon.connectDockAndAction(self.dckRenderTasks, self.actionRenderTasks)
        self.qcon.connectDockAndAction(self.dckProperties, self.actionProperties)
        self.qcon.connectDockAndAction(self.dckColumns, self.actionColumns)

        self.qcon.connectToDragDropEx(self.tblMainList,self.sigTblDragDrop)
        self.qcon.connectToKeyPress(self.tblMainList,self.sigTblKeyPress)
        self.qcon.connectToClose(self,self.sigWinClose)

    def sigActions(self, *arg):
        sender = self.sender()
        if sender is self.actionNew_List:
            self.doRTaskNewList()
        if sender is self.actionLoad_List:
            self.doRTaskLoadList()
        if sender is self.actionSave_List:
            self.doRTaskSaveList()
        if sender is self.actionQuit:
            sys.exit(0)
        if sender is self.actionSettings:
            self.doShowSettings()
        if sender is self.actionHelp:
            self.mData.optHelp()
        if sender is self.actionReportIssues:
            self.mData.optIssues()
        if sender is self.actionAbout_lra:
            self.mData.optAbout()

    def sigLstActions(self, *arg):
        self.sigJammer()
        sender = self.sender()
        if sender is self.lstColumns:
            self.mData.doPrepareColumns()
        self.sigJammer(False)

    def sigTblKeyPress(self, *arg):
        self.sigJammer()
        key = self.qcon.keyEventInfo(arg[0])
        if key=="Delete":
            self.doRTaskDelete()
        if key==16777237:
            self.doRTaskSelected()
        if key==16777235:
            self.doRTaskSelected()
        self.sigJammer(False)

    def sigTblActions(self, *arg):
        self.sigJammer()
        sender = self.sender()
        if sender is self.tblMainList:
            self.doRTaskSelected()
        self.sigJammer(False)

    def sigBtnActions(self, *arg):
        self.sigJammer()
        sender = self.sender()
        if sender == self.btnStartRender:
            self.doStartRender()
        if sender == self.btnPropApply:
            self.doRTaskUpdate()
        if sender == self.btnRTaskLoad:
           self.doRTaskLoadList()
        if sender == self.btnRTaskSave:
            self.doRTaskSaveList()
        if sender == self.btnAddFile:
            self.doRTaskAddFile()
        if sender == self.btnRemoveFile:
            self.doRTaskDelete()
        if sender == self.btnMoveDown:
            self.doRTaskMoveDown()
        if sender == self.btnMoveUp:
            self.doRTaskMoveUp()
        if sender == self.btnLogClear:
            self.mLog.clean()
        if sender == self.btnLogSave:
            self.mLog.save()
        self.sigJammer(False)

    def sigWinClose(self, *arg):
        self.mApp.rtcounter=self.rtaskSupport.rcnt
        self.qsup.uiLayoutSave()
        self.mData.doSaveColumns()
        self.mApp.saveSettings()
        self.mIcon.saveSettings()

    def sigTblDragDrop(self, *arg):
        files = self.qcon.dropEventInfoEx(arg[0])
        for eachFile in files:
            self.doRTaskAdd(eachFile)

    def doShowSettings(self):
        self.winSetting.doLoadSettings()
        self.winSetting.exec_()

    def doRTaskNewList(self):
        self.qtbl.clear(self.tblMainList)
        self.mLog.disp("Starting new list!")

    def doRTaskLoadList(self):
        f = self.qsup.getFileToOpen(FileName='list.lst',FileType='All Files (*);;List Files (*.lst)')
        if not f: return
        self.doRTaskNewList()
        ini = oplINIRW.INIRW(f,True)
        fileIds = ini.getSectionList()
        self.tblMainList.setSortingEnabled(0)
        for fileId in fileIds:
            file = ini.getOption(fileId,'file')
            rt = mRenderTask.RenderTask()
            rt = self.doRTaskAdd(file)
            rt.status = int(ini.getOption(fileId,'status'))
            rt.addedOn = ini.getOption(fileId,'addedOn')
            rt.completedOn = ini.getOption(fileId,'completedOn')
            rt.customCommand  = ini.getOption(fileId,'customcommand')
            self.doStatusUpdate(rt,self.tblMainList.rowCount()-1)
            for eachFlag in ini.getOptionList(fileId):
                if eachFlag <> 'status' and eachFlag <> 'addedon' and eachFlag <> 'completedon' and eachFlag <> 'file':
                    dt={}
                    dt['flagFullName'] = eachFlag.title()
                    dt['flagShortName'] = self.rtaskSupport.getFlagShortNameForFlagFullName(dt['flagFullName'])
                    dt['value'] = str(ini.getOption(fileId, eachFlag))
                    rt.flags.append(dt)

            col = self.qtbl.getHeaderColNo(self.tblMainList,'Added On')
            item = self.tblMainList.item(self.tblMainList.rowCount()-1, col)
            if (item): item.setText(rt.addedOn)

            #Populate First in Table
            for eachFlag in rt.flags:
                columnName = eachFlag['flagFullName']
                value = eachFlag['value']
                col = self.qtbl.getHeaderColNo(self.tblMainList,columnName)
                item = self.tblMainList.item(self.tblMainList.rowCount()-1, col)
                if (item): item.setText(value)
        self.tblMainList.setSortingEnabled(1)
        self.mLog.disp("Loading list..." + f)

    def doRTaskSaveList(self):
        f = self.qsup.getFileToSave(FileName='list.lst',FileType='All Files (*);;List Files (*.lst)')
        if not f: return
        rt = mRenderTask.RenderTask()
        if os.path.exists(f): os.remove(f)
        ini = oplINIRW.INIRW(f,True)
        for r in range(0,self.tblMainList.rowCount()):
            items = self.qtbl.getRowItems(self.tblMainList, r)
            rt = self.qtbl.getTag(items[0])
            ini.setSection(rt.id)
            ini.setOption(rt.id, 'file', rt.file)
            ini.setOption(rt.id, 'addedOn', rt.addedOn)
            ini.setOption(rt.id, 'completedOn', rt.completedOn)
            ini.setOption(rt.id, 'status', rt.status)
            ini.setOption(rt.id, 'customCommand', rt.customCommand)
            for flag in rt.flags:
                ini.setOption(rt.id, flag['flagFullName'], flag['value'])
        self.qsup.showIformationBox("lra","Current list saved, You can load it later!")
        self.mLog.disp("Saving list..." + f)

    def doRTaskSelected(self):
        rtask = self._getSelectedRTask()
        if rtask:
            self.doRTaskFlagPopulate(rtask)

    def doRTaskAddFile(self):
        file = self.qsup.getFileToOpen('Select a file to add to render list...')
        if file:
            self.doRTaskAdd(file)

    def doRTaskAdd(self, file):
        rt = mRenderTask.RenderTask(file)
        rtId = self.rtaskSupport.rcnt+1
        rt.id=str(rtId).zfill(4)
        rowData = [
                    rt.id,                  #ID
                    '',                     #STATUS
                    rt.fileName,            #FILEPATH
                    rt.addedOn,             #ADDEDON
                    rt.completedOn,         #COMPLETEDON
                  ] + self.rtaskSupport.emptyFlags()
        rowItems = self.qtbl.addRow(self.tblMainList,rowData,1)
        self.qtbl.setTag(rowItems[0],'tag',rt)
        rowItems[2].setToolTip(rt.filePath)
        self.doStatusUpdate(rt,self.tblMainList.rowCount()-1)
        self.qtbl.resizeColumnsEx(self.tblMainList)
        self.rtaskSupport.rcnt=rtId

        self.btnStartRender.setEnabled(True)
        self.btnRTaskSave.setEnabled(True)
        self.actionSave_List.setEnabled(True)
        self.mLog.disp("Task added to the list..." + rt.fileName)
        return rt

    def doRTaskMoveDown(self):
        self.__rowSwapLogic("down")

    def doRTaskMoveUp(self):
        self.__rowSwapLogic("up")

    def doRTaskUpdate(self):
        rtask = self._getSelectedRTask()
        rows = self.qtbl.getSelectedRowNo(self.tblMainList)

        if rtask:
            wdgts = self.__enabledFlags()

            #Flags of RTASK Got updated.
            self.rtaskSupport.rtaskUpdateFromUI(rtask, wdgts)
            #Now to update the UI columns.

            row = rows[0]
            #row = self.getRowOfID(rtask[0].id)
            #Clear First
            for widget in self.propWidgets:
                flagFullName,flagShortName = self.rtaskSupport.getFlagInfoCore(widget)
                col = self.qtbl.getHeaderColNo(self.tblMainList,flagFullName)
                item = self.tblMainList.item(row,col)
                if (item): item.setText('')

            #Populate First in Table
            for eachFlag in rtask.flags:
                columnName = eachFlag['flagFullName']
                value = eachFlag['value']
                col = self.qtbl.getHeaderColNo(self.tblMainList,columnName)
                item = self.tblMainList.item(row,col)
                if (item): item.setText(value)

            self.mLog.disp("Task updated..." + rtask.fileName)



    def doRTaskFlagPopulate(self, rtask=None):
        rt = mRenderTask.RenderTask('') if not rtask else rtask
        self.lePropFileName.setText(rt.fileName)
        self.lePropFilePath.setText(rt.filePath)

        #Clear First
        for eachWidget in self.propWidgets:
            group = self.getFlagParentWidget(eachWidget)
            group.setChecked(False)
            self.qsup.setText(eachWidget,'')

        #PopulateNext
        for eachWidget in self.propWidgets:
            for eachFlag in rt.flags:
                flagFullName = eachFlag['flagFullName']
                flagShortName = eachFlag['flagShortName']
                value = eachFlag['value']
                widget = self.rtaskSupport.getWidgetForFlagFullName(flagFullName)
                parentWidget = self.getFlagParentWidget(widget)
                if eachWidget == widget:
                    parentWidget.setChecked(True)
                    self.qsup.setText(widget,value)

        #Special Custom Command
        if rtask.customCommand!='':
            self.frmPropCustoms.setChecked(1)
            self.lePropCustoms.setText(rtask.customCommand)
        else:
            self.frmPropCustoms.setChecked(0)
            self.lePropCustoms.setText('')

    def doRTaskDelete(self):
        rows = self.qtbl.getSelectedRowNo(self.tblMainList)
        if rows:
            for eachRow in rows: self.tblMainList.removeRow(eachRow)
            self.mLog.disp("Task removed!")

    def doStatusUpdate(self, rtask, row):
        rtIcon = self.rtaskSupport.getIconForStatus(rtask.status)
        items = self.qtbl.getRowItems(self.tblMainList,row)
        self.qsup.setIcon(items[1],rtIcon)
        rtStatus = self.rtaskSupport.getStatusNameForStatus(rtask.status)
        items[1].setText(rtStatus)
        items[4].setText(rtask.completedOn)
        self.qtbl.resizeColumnsEx(self.tblMainList)

    def doStartRender(self):
        self.fin.GameOver()



    def __rowSwapLogic(self, mode="down"):
        '''
        mode can either "up" or "down"
        '''
        self.tblMainList.blockSignals(1)
        self.tblMainList.setSortingEnabled(0)
        mode = mode.lower()

        rows = self.qtbl.getSelectedRowNo(self.tblMainList)
        minRowNo = 0
        maxRowNo = self.tblMainList.rowCount()

        if rows:
            selRowNo = rows[0]
            nxtRowNo = selRowNo - 1 if mode == "up" else selRowNo + 1

            if ((mode == "up" and nxtRowNo != minRowNo-1) or
                (mode == "down" and nxtRowNo != maxRowNo)) :

                #Take Items have it hand
                selItems = self.qtbl.takeRowItems(self.tblMainList, selRowNo)
                nxtItems = self.qtbl.takeRowItems(self.tblMainList, nxtRowNo)

                #Replacing new row:
                for col, eachItem in enumerate(selItems):
                    self.tblMainList.setItem(nxtRowNo, col, eachItem)

                #Replacing old row:
                for col, eachItem in enumerate(nxtItems):
                    self.tblMainList.setItem(selRowNo, col, eachItem)

                #self.tblMainList.repaint()
                self.tblMainList.selectRow(nxtRowNo)
                #rtask = self.qtbl.getTag(items[0])
                #rtask = self._getSelectedRTask()
            else:
                #We cant move beyond last row
                pass
        else:
            #No row selected?
            pass
        self.tblMainList.repaint()
        self.tblMainList.blockSignals(0)
        self.tblMainList.setSortingEnabled(1)

    def refreshStatus(self,rt):
        row = self.getRowOfID(rt.id)
        if row>=0:
            #self.doRTaskUpdate()
            self.doStatusUpdate(rt,row)

    def getRowOfID(self, id=-1):
        row = self.qtbl.findRow(self.tblMainList,str(id),True,[0])
        return row[0] if len(row) else -1
    def _getSelectedRTask(self, all=False):
        ret = []
        rows = self.qtbl.getSelectedRowNo(self.tblMainList)
        if rows:
            if all:
                for eachRow in rows:
                    items = self.qtbl.getRowItems(self.tblMainList, eachRow)
                    rtask = self.qtbl.getTag(items[0])
                    ret.append(rtask)
            else:
                ret = None
                items = self.qtbl.getRowItems(self.tblMainList, rows[0])
                ret = self.qtbl.getTag(items[0])

        return ret

    def _getAllRTask(self):
        rows = self.tblMainList.rowCount()
        ret =[]
        for eachRow in range(0,rows):
            items = self.qtbl.getRowItems(self.tblMainList, eachRow)
            rtask = self.qtbl.getTag(items[0])
            ret.append(rtask)
        return ret

    def __enabledFlags(self):
        wdgts = []
        for grp in self.groupedWidgets.keys():
            if grp.isChecked():
                for item in self.groupedWidgets[grp]:
                    wdgts.append(item)
        return wdgts

    def sigJammer(self,jam=True):
        self.dckRenderTasks.blockSignals(jam)
        self.dckProperties.blockSignals(jam)
        self.dckColumns.blockSignals(jam)
        self.actionRenderTasks.blockSignals(jam)
        self.actionProperties.blockSignals(jam)
        self.actionColumns.blockSignals(jam)

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