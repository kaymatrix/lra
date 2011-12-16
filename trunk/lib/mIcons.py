#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AIAA
#
# Created:     12-12-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import configobj
import oplPyUtilities

class Icons():

    def __init__(self):
        self.noIcon="/04/16/21.png"
        self.male = "/01/16/07.png"
        self.female = "/01/16/10.png"
        self.star = "/01/16/31.png"
        self.heart = "/01/16/33.png"
        self.search = "/01/16/49.png"
        self.info = "/01/16/02.png"
        self.settings = "/01/16/41.png"
        self.home = "/01/16/45.png"
        self.folder = "/01/16/46.png"
        self.pencil = "/01/16/19.png"
        self.puzzle = "/02/16/19.png"
        self.clock = "/02/16/02.png"
        self.apply = "/02/16/02.png"
        self.filter = "/02/16/04.png"
        self.spaner = "/02/16/36.png"
        self.floppy = "/02/16/45.png"
        self.circleRed = "/04/16/01.png"
        self.circleGreen = "/04/16/02.png"
        self.circleBlue = "/04/16/03.png"
        self.circleYellow = "/04/16/04.png"
        self.circlePinkRed = "/04/16/05.png"
        self.circleOrange = "/04/16/06.png"
        self.circlePink = "/04/16/07.png"
        self.circleBlack = "/04/16/08.png"
        self.circleGray = "/04/16/09.png"
        self.circleWhite = "/04/16/10.png"

class Configs(Icons):
    def __init__(self, file="icons.ini", autoLoad=True):
        Icons.__init__(self)
        self._muti = oplPyUtilities.oplPyUtilities()
        self._cfg = configobj.ConfigObj(file)
        if autoLoad: self.loadSettings()

    def loadSettings(self):
        attribs = self._muti.getAttributes(self)
        for eachAttrib in attribs:
            if (self._cfg.dict().has_key(eachAttrib[0])):
                setattr(self,eachAttrib[0],self._cfg[eachAttrib[0]])
            else:
                self._cfg[eachAttrib[0]]=getattr(self,eachAttrib[0])
                self._cfg.write()

    def saveSettings(self):
        attribs = self._muti.getAttributes(self)
        for eachAttrib in attribs:
            self._cfg[eachAttrib[0]]=getattr(self,eachAttrib[0])
        self._cfg.write()

if '__main__' == __name__:
    cfg = Configs()
    #cfg.appName="newName"
    cfg.saveSettings()

