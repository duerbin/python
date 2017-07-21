#########################################################################
# -*- coding: utf-8 -*-
#File Name: checkRD.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014年03月07日 星期五 16时55分47秒
#########################################################################
#!/usr/bin/env python
import os
import os.path
import sys
import shutil
import MySQLdb 
import ConfigParser
from Common import logger



def getData(tableN):
	config=ConfigParser.ConfigParser()
	config.read("../cfg/basic.ini")
	mysqlH=config.get("mysql","mysqlH")
	mysqlU=config.get("mysql","mysqlU")
	mysqlP=config.get("mysql","mysqlP")
	mysqlD=config.get("mysql","mysqlD")
	mysqlC=config.get("mysql","mysqlC")
	conn=MySQLdb.connect(host=mysqlH,user=mysqlU,passwd=mysqlP,db=mysqlD,charset=mysqlC)
	logger.debug("mysql connect string is: Host=%s user=%s passwd=%s db=%s charset=%s",mysqlH,mysqlU,mysqlP,mysqlD,mysqlC)
	cursor = conn.cursor()
	#insert
#	sql = "insert into recordT(name,path) values(%s,%s)"
#	param = ("srcpath","/tmp/aa")
#	n = cursor.execute(sql,param) 
#	print n
	#select 
	sql = "select * from "+tableN
	print sql
 	n = cursor.execute(sql)
	rows = cursor.fetchall()
	#print rows
	print rows
	return rows
 	cursor.close()


def outputCommon(rows,table,fileName):
	fp=open(fileName,"a+")
	if not fp:
		print fileName+"open failed"
		fp.close()
		return -1
	if table=="UserT":
		fp.write("########################################\n")
		fp.write("#UserT"+"\n")
		str1="$client=\""+rows[0][1]+"\"\n"
		str2="$client1=\""+rows[1][1]+"\"\n"
		print str1,str2
		fp.write(str1)
		fp.write(str2)
		fp.write("########################################\n")
	if table=="DataT":
		fp.write("########################################\n")
		fp.write("#DataT\n")
		for row in rows:
			if row[1]=="oracle":
				fp.write("#oracle\n")
				fp.write("$oracleIP=\""+row[2]+"\"\n")
				fp.write("$oraclePort=\""+row[3]+"\"\n")
				fp.write("$oracleName=\""+row[4]+"\"\n")
				fp.write("$oracleUser=\""+row[5]+"\"\n")
				fp.write("$oraclePasswd=\""+row[6]+"\"\n")
				fp.write("$oracleSN=\""+row[7]+"\"\n")
			if row[1]=="mysql_ucds":
				fp.write("#mysql_ucds\n")
				fp.write("$mysqlIP=\""+row[2]+"\"\n")
				fp.write("$mysqlPort=\""+row[3]+"\"\n")
				fp.write("$mysqlDB=\""+row[4]+"\"\n")
				fp.write("$mysqlUser=\""+row[5]+"\"\n")
				fp.write("$mysqlPasswd=\""+row[6]+"\"\n")
				
			if row[1]=="mysql_port":
				fp.write("#mysql_port\n")
				fp.write("$mysqlDB_portal=\""+row[4]+"\"\n")
	if table=="SoftT":
		fp.write("##############################3####\n")
		fp.write("#softT\n")
		
		for row in rows:
			if row[1]=="resin":
				fp.write("#resin\n")
				fp.write("$resin_name=\""+row[2]+"\"\n")
				fp.write("$resin_file=\""+row[3]+"\"\n")
			if row[1]=="jdk":
				fp.write("#jdk\n")
				fp.write("$jdk_name=\""+row[2]+"\"\n")
				fp.write("$jdk_path=\""+row[3]+"\"\n")
			if row[1]=="tomcat":
				fp.write("#tomcat\n")
				fp.write("$tomcat_name=\""+row[2]+"\"\n")
				fp.write("$tomcat_file=\""+row[3]+"\"\n")
			if row[1]=="plat":
				fp.write("#plat\n")
				fp.write("$plat_name=\""+row[2]+"\"\n")
				fp.write("$platSerFile=\""+row[3]+"\"\n")
	if table=="ServiceT":
		fp.write("##############################3####\n")
		fp.write("#ServiceT\n")
		for row in rows:
			if row[1]=="gls":
				fp.write("#gls\n")
				fp.write("$glsIP=\""+row[2]+"\"\n")
				fp.write("$glsP=\""+row[3]+"\"\n")
				fp.write("$glsServantName=\""+row[5]+"\"\n")
			if row[1]=="license":
				fp.write("#license\n")
				fp.write("$licenseIP=\""+row[2]+"\"\n")
				fp.write("$licenseP=\""+row[3]+"\"\n")
			if row[1]=="slee":
				fp.write("#slee\n")
				fp.write("$sleeIP=\""+row[2]+"\"\n")
				fp.write("$sleeP=\""+row[3]+"\"\n")
				fp.write("$sleeName=\""+row[4]+"\"\n")
			if row[1]=="ucds":
				fp.write("#ucds\n")
				fp.write("$ucdsIP=\""+row[2]+"\"\n")
				fp.write("$ucdsP=\""+row[3]+"\"\n")
				fp.write("$ucdsName=\""+row[4]+"\"\n")
			if row[1]=="ucx":
				fp.write("#gls\n")
				fp.write("$ucxIP=\""+row[2]+"\"\n")
				fp.write("$ucxP=\""+row[3]+"\"\n")
			if row[1]=="datakeep":
				fp.write("#datakeep\"\n")
				fp.write("$datakeepIP=\""+row[2]+"\"\n")
				fp.write("$datakeepP=\""+row[3]+"\"\n")
			if row[1]=="cms":
				fp.write("#cms\n")
				fp.write("$cmsIP=\""+row[2]+"\"\n")
				fp.write("$cmsP=\""+row[3]+"\"\n")
				fp.write("$cmsName=\""+row[4]+"\"\n")
				fp.write("$cmsServantName=\""+row[5]+"\"\n")
			if row[1]=="dds":
				fp.write("#dds\n")
				fp.write("$ddsIP=\""+row[2]+"\"\n")
				fp.write("$ddsP=\""+row[3]+"\"\n")
				fp.write("$ddsName=\""+row[4]+"\"\n")
				fp.write("$ddsServantName=\""+row[5]+"\"\n")
			if row[1]=="rms":
				fp.write("#rms\n")
				fp.write("$rmsIP=\""+row[2]+"\"\n")
				fp.write("$rmsP=\""+row[3]+"\"\n")
				fp.write("$rmsName=\""+row[4]+"\"\n")
			if row[1]=="dcs":
				fp.write("#dcs\n")
				fp.write("$dcsIP=\""+row[2]+"\"\n")
				fp.write("$dcsP=\""+row[3]+"\"\n")
				fp.write("$dcsName=\""+row[4]+"\"\n")
			if row[1]=="agent":
				fp.write("#agent\n")
				fp.write("$agentIP=\""+row[2]+"\"\n")
				fp.write("$agentP=\""+row[3]+"\"\n")
			if row[1]=="ss":
				fp.write("#ss\n")
				fp.write("$ssIP=\""+row[2]+"\"\n")
				fp.write("$ssP=\""+row[3]+"\"\n")
				fp.write("$ssName=\""+row[4]+"\"\n")
			if row[1]=="dae":
				fp.write("#dae\n")
				fp.write("$daeIP=\""+row[2]+"\"\n")
				fp.write("$daeP=\""+row[3]+"\"\n")
				fp.write("$daeName=\""+row[4]+"\"\n")
	if table=="CommT":
		fp.write("##############################3####\n")
		fp.write("#CommT\n")
		for row in rows:			
			fp.write('$'+row[1]+'=\"'+row[2]+'\"\n')
	fp.close()
	return 0


def usage(program):
	print "usage: "+program+" FileName"
#if len(sys.argv)!=2:
	#usage(sys.argv[0])
	#exit()	
#else:
	#fileName=sys.argv[1]
	#if not os.path.exists(fileName):
	#	print fileName+" is not exist"
	#	fileAP=os.path.split(fileName)
	#	if not os.path.exists(fileAP[0]):
	#		print fileAP[0]+" is a directory,but not exist"
	#		print "begin to create directory"+fileAP[0]
	#		os.mkdirs(fileAP[0])


rows=getData("UserT")
outputCommon(rows,"UserT","D://a.txt")
rows=getData("DataT")
outputCommon(rows,"DataT","D://a.txt")
rows=getData("SoftT")
outputCommon(rows,"SoftT","D://a.txt")
rows=getData("ServiceT")
outputCommon(rows,"ServiceT","D://a.txt")
rows=getData("CommT")
outputCommon(rows,"CommT","D://a.txt")

raw_input("Press any key to exit!") 
