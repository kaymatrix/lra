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
            self.fileName=os.path.basename(file)
            self.filePath=os.path.dirname(file)
            self.addedOn=self._muti.getDateTime()
            self.status=mrts.YetToStart
        else:
            self.fileName='-'
            self.filePath='-'
            self.addedOn='-'
            self.status=mrts.FileMissing

        self.completedOn='-'

        self.flags={}


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
            flag = (
                    flagFullName,
                    flagShortName,
                    eachProp
                   )
            self.rflags.append(flag)

    def emptyFlags(self):
        #For componsating the column
        ret = []
        for flag in self.rflags:
            ret.append("")
        return ret

    def getFlagNames(self):
        lst=[]
        for name in self.rflags:
            lst.append(name[0])
        return lst

    def getFlagNamesAndFixedNames(self):
        fixed = [
                'ID',
                'Status',
                'File',
                'Added On',
                'Completed On'
                ]
        allCols = fixed + self.getFlagNames()
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

    def rtaskUpdate(self, rtask=None, activeWidgets=[]):
        if rtask and activeWidgets:
            rtask.flags = self.getFlagValues(activeWidgets)

    def getFlagValues(self, widgets=[]):
        res = []
        for rflag in self.rflags:
            if rflag[2] in widgets:
                flagFullName = rflag[0]
                flagShortName = rflag[1]
                widget = rflag[2]
                value = self.parent.qsup.getText(widget)
                dt = {}
                dt['flagFullName'] = flagFullName
                dt['flagShortName'] = flagShortName
                dt['value'] = value
                dt['widget'] = widget
                res.append(dt)
        return res





