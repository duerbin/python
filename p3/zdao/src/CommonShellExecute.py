#########################################################################
# -*- coding: utf-8 -*-
#File Name: oracleSelect.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014年03月11日 星期二 14时55分31秒
#########################################################################
#!/usr/bin/env python
import sys
import os


basePath=os.getcwd()
print basePath
outfile="%s/%s" % (basePath,"outlresultlog")
print outfile
if(os.path.exists(outfile)):
	os.remove(outfile)


def usage(program):
	print "usage: "+program+" log_MaxIndex"

def deLogCheck(maxLogIndex):
	while maxLogIndex>0:
		logfile="DialEngine.log.%d" % maxLogIndex
		print logfile
		maxLogIndex-=1
		checkfile(logfile)
	checkfile(DialEngine.log)

def checkfile(filename):
	filePath="%s/%s" % (basePath,filename)
	print filePath 
	cmd="cat %s >> %s" % (filePath,outfile)
	print cmd
	os.system(cmd)


if __name__=="__main__":
	if len(sys.argv)!=2:
		usage(sys.argv[0])
		exit()
	maxLogIndex=int(sys.argv[1])
	deLogCheck(maxLogIndex)
