#
# Raja's Python Library.
#
# General EDL functions used in VFX Context
#
# Copyright (c) 2009-2010 by Raja.All rights reserved.
#
# See the README file for information on usage 
#

"""This python file contains various frequently used function"""
	    
	    
VERSION = "1.0 Beta"

import os
import glob

def dpxFrameToTimeCode(frames,fps):
    
    frames=int(frames)
    
    HH = frames/(60*60*fps)
    MM = frames%(60*60*fps)/(60*fps)
    SS = frames%(60*fps)/fps
    FF = frames%fps
    
    myTimeCode= "%s:%s:%s:%s"%(HH,MM,SS,FF)\

    return timeCodePadding(myTimeCode)

def frameToTimeCode(frames,fps):
    
    spf=1/float(fps)
    
    sec = (int(frames.split(".")[0])/1000)%60

    frame=int(round(((int(frames.split(".")[0])%1000)/spf)/1000,1))

    minutes = (int(frames.split(".")[0])/1000)/60

    hr = minutes/60

    timeCode=str(hr)+":"+str(minutes)+":"+str(sec)+":"+str(frame)
    return timeCodePadding(timeCode)


def offsetTimeCode(offsetTime,timeCode,fps):
    
    secOff=0
    minOff=0
    hrOff=0
    
    hour,minute,sec,frame=timeCode.split(":")    
    sHour,sMinute,sSec,sFrame=offsetTime.split(":")    

    if int(frame)+int(sFrame)>=fps:
        secOff=1
        newFrame=str(int(frame)+int(sFrame)-fps)
    else:newFrame=str(int(frame)+int(sFrame))

    if int(sec)+int(sSec)>=60:
        minOff=1
        newSec=str(int(sec)+int(sSec)-60+secOff)
    else:newSec=str(int(sec)+int(sSec)+secOff)

    if int(minute)+int(sMinute)>60:
        hrOff=1
        newMinute=str(int(minute)+int(sMinute)-60+minOff)
    else:
        newMinute=str(int(minute)+int(sMinute)+minOff)

    newTimeCode=str(int(hour)+int(sHour)+hrOff)+":"+newMinute+":"+newSec+":"+newFrame
    
    return newTimeCode

def timeCodeToFrame(timeCode,fps):
    #print timeCode
    hour,minute,sec,frame=timeCode.split(":")    
    frames=(int(hour)*60*60*fps)+(int(minute)*60*fps)+(int(sec)*fps)+int(frame)
    return frames


def timeCodePadding(timeCode):
    j=""
    for i in timeCode.split(":"):
        if len(i)<2:i="0"+i
        j=j+i+":"
    return j[:-1]


def editParser(inputFile,fps):
    
    if os.path.lexists(inputFile):
        parseFile,ext = os.path.splitext(inputFile)
        
        editData=[]
        allLines=open(inputFile,"r").readlines()
        
        if ext == ".txt":            
            for n,i in enumerate(allLines):
                if n:
                    TC_IN = frameToTimeCode(i.split(";")[2],fps)
                    TC_LEN = frameToTimeCode(i.split(";")[3],fps)
                    TC_OUT = timeCodePadding(offsetTimeCode(TC_IN,TC_LEN,fps))
                    
                    
            
                    SRTC_IN = frameToTimeCode(i.split(";")[13],fps)
                    SRTC_LEN = frameToTimeCode(i.split(";")[14],fps)
                    SRTC_OUT = timeCodePadding(offsetTimeCode(SRTC_IN,SRTC_LEN,fps))     
                    
                    SRFR_IN = timeCodeToFrame(SRTC_IN,fps)
                    SRFR_OUT = timeCodeToFrame(SRTC_OUT,fps)
                    SRFR_LEN = (SRFR_OUT-SRFR_IN)+1
                    
                    clipName = os.path.basename(i.split(";")[11]).split("_")[3]+"_"+os.path.basename(i.split(";")[11]).split("_")[4]
                    
                    clipNo = n

                    while len(str(clipNo))<= 3:clipNo="0"+str(clipNo)                 
                    
                    
                    curData={}
                    
                    curData['Frame_In'] = SRFR_IN
                    curData['Clip_Name'] = clipName
                    
                    curData['Clip_Number'] = clipNo
                    curData['Frame_Out'] = SRFR_OUT
                    curData['Frame_Length'] = SRFR_LEN
                    
                    curData['TC_In'] = TC_IN
                    curData['TC_Out'] = TC_OUT
                    #curData['TC_Length'] = TC_LEN
                    
                    editData.append(curData)
                    
            return editData
            
        elif ext ==".edl":
            count=0
            for n in range(0,len(allLines),4):
                
                if n >2:
                    count=count+1
                    i=allLines[n].replace("\n","")
                    
                    print i
                    
                    TC_IN = i.split(" ")[-2]               
                    TC_OUT = i.split(" ")[-1]
            
                    SRTC_IN = i.split(" ")[-4]         
                    SRTC_OUT = i.split(" ")[-3]
            
                    
                    SRFR_IN = timeCodeToFrame(SRTC_IN,fps)
                    SRFR_OUT = timeCodeToFrame(SRTC_OUT,fps)
            
                    SRFR_LEN = (SRFR_OUT-SRFR_IN) + 1
            
                    clipName=allLines[n+1].split(":")[-1].replace("\n","")
                    clipName=clipName.replace(" ","")
                    
                    clipNo = count

                    while len(str(clipNo))<= 3:clipNo="0"+str(clipNo)            
                    
                    curData={}
                    
                    curData['Frame_In'] = SRFR_IN
                    curData['Clip_Name'] = clipName
                    
                    curData['Clip_Number'] = clipNo
                    curData['Frame_Out'] = SRFR_OUT
                    curData['Frame_Length'] = SRFR_LEN
                    
                    curData['TC_In'] = TC_IN
                    curData['TC_Out'] = TC_OUT
                    #curData['TC_Length'] = TC_LEN
                    
                    editData.append(curData)
                    
            return editData            
        else:
            print "Not a valid File.Input a EDL or Sony Vegas Text File"
        
    else:
        print "%s doesn't exists.Please Check" % inputFile

def txtToEdl(inputFile,fps):
    if os.path.lexists(inputFile):
        
        parseFile,ext = os.path.splitext(inputFile)
        
        extReqr=[".txt"]
        
        if ext in extReqr :   
            allLines=open(inputFile,"r").readlines()
            
            outEdlName=parseFile+".edl"
            
            newEdl=open(outEdlName,'w')

            #newEdl.write("\n")
            #newEdl.write("TITLE:%s\n"%os.path.basename(outEdlName))
            newEdl.write("TITLE: ( no title )")
            #newEdl.write("\nFCM: NON-DROP FRAME")
            #newEdl.write("\n*FCM: DIGITAL TV 24P")
            newEdl.write("\n")
            for n,i in enumerate(allLines):
                if n:
                        
                    TC_IN = frameToTimeCode(i.split(";")[2],fps)
                    TC_LEN = frameToTimeCode(i.split(";")[3],fps)
                    TC_OUT = timeCodePadding(offsetTimeCode(TC_IN,TC_LEN,fps))
                    
                    SRTC_IN = frameToTimeCode(i.split(";")[13],fps)
                    SRTC_LEN = frameToTimeCode(i.split(";")[14],fps)
                    SRTC_OUT = timeCodePadding(offsetTimeCode(SRTC_IN,SRTC_LEN,fps))
                    
                    event=str(n)
                    print i
                    #print os.path.basename(i.split(";")[11]).split(".")[-2]
                    
                    while len(event)<3:event="0"+event
                    #clipName=os.path.basename(i.split(";")[11]).split(".")[0]#+"."+os.path.basename(i.split(";")[11]).split(".")[1]+".dpx"
                    if "_plate_v" in i.split(";")[11]:
                        clipName=os.path.basename(i.split(";")[11]).split("_")[1]+os.path.basename(i.split(";")[11]).split("_")[2]+".000"+os.path.basename(i.split(";")[11]).split(".")[-2]+".dpx"
                    else:
                        #clipName=os.path.basename(i.split(";")[11]).split("_")[1]
                        clipName=".".join(os.path.basename(i.split(";")[11]).split(".")[0].split("_"))+".dpx"
                        
                    print clipName
                    
                    #newEdl.write( "\n%s  UNKNOWN  V  C  %s %s %s %s"%(event,SRTC_IN,SRTC_OUT,TC_IN,TC_OUT))  
                    #newEdl.write("\n")
                    newEdl.write( "\n%s        %s  V     C        %s %s %s %s"%(event,"01",SRTC_IN,SRTC_OUT,TC_IN,TC_OUT))  
                    newEdl.write( "\n* FROM CLIP NAME:  %s"%clipName)
                    #newEdl.write( "* COMMENT: ")
                    #newEdl.write( "* PROBLEM WITH EDIT: CLIP HAD NO TIMECODE TRACK.")
                    newEdl.write( "\n")
            newEdl.close()        
        else:
                print "Not a valid File.Input a Sony Vegas Text File"
    else:
        print "%s doesn't exists.Please Check" % inputFile
        
print editParser("d:/edl/TFM_cut8.3_REEL3.edl",24)


def dpxFileNaming(inputFile,fps):
    frame=inputFile.split(".")[-2]
    print frame
    print dpxFrameToTimeCode(frame,fps)
    
def dpxRename(inputDir,check=0):
    test=check
    #print inputDir
    dpxData=glob.glob(inputDir+'*.dpx')
       
    
    for oldPath in dpxData:
        oldName = os.path.basename(oldPath)
        
        if "_PLA_OUT_" not in oldName:
          
            if len(oldName.split("_")) == 6:
                
                baseDir = "\\".join(oldPath.split("\\")[0:-1])
                
                newFrame = oldPath.split(".")[-2]

                if len(oldName.split("."))!=2:
                    
                    if "_Alpha" not in oldName:

                        #print len(oldName.split("."))
                        
                        #print oldName
                        if "_plate_v" in oldName:
                            clipName=os.path.basename(oldName).split("_")[1]+os.path.basename(oldName).split("_")[2]
                        else:
                            
                            clipName=os.path.basename(oldName).split("_")[1]+os.path.basename(oldName).split("_")[2]
                        
                        while len(str(newFrame))<= 6: newFrame="0"+str(newFrame) 
                        
                        newPath=baseDir+"\\"+clipName+"_"+newFrame+"."+oldName.split(".")[-1]
                        
                        
                        if test==1:print newPath
                        else:
                            print newPath
                            os.rename(oldPath,newPath)
                        
            elif len(oldName.split("_")) == 3:
                #print "Yes"
                baseDir = "\\".join(oldPath.split("\\")[0:-1])
                
                newFrame = oldName.split("_")[2].split(".")[0]
                
                #print newFrame

                if len(oldName.split("."))==2:
                    
                    if "_Alpha" not in oldName:

                        #print len(oldName.split("."))
                        
                        #print oldName
                        if "_plate_v" in oldName:
                            clipName=os.path.basename(oldName).split("_")[1]+os.path.basename(oldName).split("_")[2]
                        else:                            
                            clipName=os.path.basename(oldName).split("_")[0]
                        
                        while len(str(newFrame))<= 6: newFrame="0"+str(newFrame) 
                        #print newFrame
                        newPath=baseDir+"\\"+clipName+"_"+newFrame+"."+oldName.split(".")[-1]
                        
                        
                        if test==1:print newPath
                        else:
                            print newPath
                            os.rename(oldPath,newPath)

        if "_PLA_OUT_" in os.path.basename(oldName):
            
            if len(oldName.split("_")) == 6:
                
                baseDir = "\\".join(oldPath.split("\\")[0:-1])
                
                newFrame = oldPath.split(".")[-2]

                if len(oldName.split("."))!=2:
                    if "_Alpha" not in oldName:

                        #print len(oldName.split("."))
                        
                        #print oldName
                        if "_plate_v" in oldName:
                            clipName=os.path.basename(oldName).split("_")[1]+os.path.basename(oldName).split("_")[2]
                        else:
                            
                            clipName=os.path.basename(oldName).split("_")[3]+os.path.basename(oldName).split("_")[4]
                        
                        while len(str(newFrame))<= 6: newFrame="0"+str(newFrame) 
                        
                        newPath=baseDir+"\\"+clipName+"_"+newFrame+"."+oldName.split(".")[-1]
                        
                        
                        if test==1:print newPath
                        else:
                            print newPath
                            os.rename(oldPath,newPath)
