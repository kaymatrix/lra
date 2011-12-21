#-------------------------------------------------------------------------------
# Name:        RENDER TASK
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
import os
import mRTaskStatus as mrts
import mIcons

class ERenderStatus():

    def __ini__(self):
        self.YetToStart=1
        self.Rendering=2
        self.RenderedWithNoError=3
        self.RenderedWithError=4
        self.RenderCancelled=5
        self.FileMissing=6

class RenderTask():

    def __init__(self, file=''):
        self._muti=oplPyUtilities.oplPyUtilities()

        if file and os.path.exists(file):
            self.file=file
            self.fileName=os.path.basename(file)
            self.filePath=os.path.dirname(file)
            self.addedOn=self._muti.getDateTime()
            self.status=mrts.YetToStart
        else:
            self.file='-'
            self.fileName='-'
            self.filePath='-'
            self.addedOn='-'
            self.status=mrts.FileMissing

        self.completedOn='-'

        self.flags=[]


class RenderTaskSupport():

    def __init__(self, parent, iconsObj):
        self.mIcon= mIcons.Configs() if not iconsObj else iconsObj
        self._muti=oplPyUtilities.oplPyUtilities()
        self.rcnt=0
        self.rflags=[]
        self.parent=parent

    def initalizeFlags(self, propertyWidgets=[]):
        for eachProp in propertyWidgets:
            info = self.getFlagInfoCore(eachProp)
            flagFullName = info[0]
            flagShortName = info[1]
            flag = {
                    "FLAG_FULL_NAME": flagFullName,
                    "FLAG_SHORT_NAME": flagShortName,
                    "FLAG_WIDGET": eachProp
                   }
            self.rflags.append(flag)

    def emptyFlags(self):
        #For componsating the column
        ret = []
        for flag in self.rflags:
            ret.append("")
        return ret

    def getAllFlagNames(self):
        lst=[]
        for flag in self.rflags:
            lst.append(flag['FLAG_FULL_NAME'])
        return lst

    def getAllFlagNamesWithFixedNames(self):
        fixed = [
                'ID',
                'Status',
                'File',
                'Added On',
                'Completed On'
                ]
        allCols = fixed + self.getAllFlagNames()
        return allCols

    def getFlagInfoCore(self, widget):
        flagFullName = ""
        flagShortName = ""
        if widget and hasattr(widget,"property"):
            flagFullName = str(widget.property("flagFullName").toString())
            flagShortName = str(widget.property("flagShortName").toString())
        return (flagFullName,flagShortName)

    def getIconForStatus(self,status):
        if status==mrts.FileMissing:
            return self.mIcon.circleOrange

        if status==mrts.RenderCancelled:
            return self.mIcon.circleWhite

        if status==mrts.RenderedWithError:
            return self.mIcon.circleGray

        if status==mrts.RenderedWithNoError:
            return self.mIcon.circleBlack

        if status==mrts.Rendering:
            return self.mIcon.circleGreen

        if status==mrts.YetToStart:
            return self.mIcon.circleRed

    def getStatusNameForStatus(self,status):
        atrs =  self._muti.getAttributes(mrts)
        for atr in atrs[0:len(atrs)-4]:
            if len(atr)==2 and atr[1]==status:
                return atr[0]

    def rtaskUpdateFromUI(self, rtask=None, activeWidgets=[]):
        if rtask and activeWidgets:
            rtask.flags = self.getFlagValuesFromWidgets(activeWidgets)

    def getFlagValuesFromWidgets(self, widgets=[]):
        '''
        rtaskFlagWithValue = [
                                {
                                    'flagFullName': "Some Flag",
                                    'flagShortName': "SF",
                                    'value': "some value",
                                },

                                {
                                    'flagFullName': "Some Flag2",
                                    'flagShortName': "SF2",
                                    'value': "some value2",
                                },
                             ]
        '''

        res = []
        for rflag in self.rflags:
            if rflag['FLAG_WIDGET'] in widgets:
                flagFullName = rflag['FLAG_FULL_NAME']
                flagShortName = rflag['FLAG_SHORT_NAME']
                widget = rflag['FLAG_WIDGET']
                value = self.parent.qsup.getText(widget)
                dt = {}
                dt['flagFullName'] = flagFullName
                dt['flagShortName'] = flagShortName
                dt['value'] = value
                res.append(dt)
        return res

    def getWidgetForFlagFullName(self, flagName):
        for rflag in self.rflags:
            if flagName == rflag['FLAG_FULL_NAME']:
                return rflag['FLAG_WIDGET']
        return None

    def getFlagShortNameForFlagFullName(self, flagName):
        for rflag in self.rflags:
            if flagName == rflag['FLAG_FULL_NAME']:
                return rflag['FLAG_SHORT_NAME']
        return None

    def getFlagFullNameForWidget(self, flagWidget):
        for rflag in self.rflags:
            if flagWidget == rflag['FLAG_WIDGET']:
                return rflag['FLAG_FULL_NAME']
        return None




