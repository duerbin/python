#########################################################################
# -*- coding: utf-8 -*-
# File Name: test.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014年03月17日 星期一 10时07分54秒
#########################################################################
#!/usr/bin/env python
import logging
import logging.config
import time

from ConfigOperater import CCpOperater
logging.config.fileConfig("../cfg/logger.conf")
logger = logging.getLogger("puppet")
#test logger
logger.debug('This is debug message')
logger.info('This is info message')
logger.warning('This is warning message')

#ConfigParse
gConf = CCpOperater("../cfg/sys.ini")
#gConf.read("./cfg/sys.ini") 
def common_keyv(strk):
	fp=open("/etc/puppet/manifests/common.pp","r")
#	print strk
	try:
		while True:
			line=fp.readline()
			if not line:
				break
			strt=line.split("=")
			if (strt[0]==strk):
	#			print strt
				return strt[1].split("\"")[1]
	finally:
		fp.close()
def gettime(strf):
	now=time.localtime(time.time())
	return time.strftime(strf,now)


def usage(program):
	print "usage: "+program+" ICEPATH DSTPATH"
i


