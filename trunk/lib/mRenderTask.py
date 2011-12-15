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

class RenderTaskSupport():

    def __init__(self, iconsObj):
        self.mIcon= mIcons.Configs() if not iconsObj else iconsObj
        self._muti=oplPyUtilities.oplPyUtilities()

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




