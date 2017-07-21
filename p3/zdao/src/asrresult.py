#########################################################################
# -*- coding: utf-8 -*-
#File Name: oracleSelect.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014年03月11日 星期二 14时55分31秒
#########################################################################
#!/usr/bin/env python
import os
import  xml.dom.minidom
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from Common import logger
from FileDirectory import GetFileList
##############################################################3
#打开xml文档
dstDir='/home/dueb/log/asr/InsertPyRedis/src/resultnew/'
def checkFileType(fileList):
    if len(fileList)==0:
        print "directory is null"
        return 
    for files in fileList:
        split=os.path.splitext(files)        
        if split[1]!='.xml':
            print "%s is not xml file" % files
            continue
        else:
            AnaXmlFile(files)
def AnaXmlFile(xmlfile):
    dom = xml.dom.minidom.parse(xmlfile) 
    root = dom.documentElement     
    name= root.getElementsByTagName('audio')[0].childNodes[0].data.strip()
    print name
    asrresultdesc= root.getElementsByTagName('input')[0].childNodes[0].data.strip()
    asrresult= root.getElementsByTagName('meaning')[0].childNodes[0].data.strip()
    a="%s %s %s\n" % (name,asrresult,asrresultdesc)
    fout=open("result.txt",'a+')
    fout.write(a)
    fout.close()
    #raudio=root.getElementsByTagName('audio')
        


if __name__ == '__main__':
    fileList=GetFileList(dstDir)
    checkFileType(fileList)
   
    
        
    


