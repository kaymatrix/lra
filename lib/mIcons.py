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

        self.app = "/01/16/32.png"
        self.rendertask = "/01/16/20.png"
        self.properties = "/04/16/29.png"
        self.columns = "/02/16/30.png"
        self.log = "/02/16/09.png"
        self.startrender = "/03/16/31.png"
        self.apply = "/03/16/02.png"
        self.cancel = "/03/16/01.png"
        self.save = "/02/16/45.png"
        self.load = "/01/16/46.png"
        self.new = "/01/16/22.png"
        self.quit = "/03/16/50.png"
        self.help = "/04/16/15.png"
        self.about = "/04/16/02.png"
        self.settings = "/02/16/36.png"
        self.tag = "/01/16/17.png"
        self.stop = "/03/16/42.png"
        self.skip = "/03/16/37.png"
        self.plus = "/03/16/03.png"
        self.minus = "/03/16/04.png"
        self.down = "/03/16/07.png"
        self.up = "/03/16/08.png"
        self.search = "/01/16/49.png"
        self.redflag = "/02/16/21.png"
        self.tv = "/02/16/28.png"

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

