#########################################################################
# -*- coding: utf-8 -*-
#File Name: oracleSelect.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014年03月11日 星期二 14时55分31秒
#########################################################################
#!/usr/bin/env python
import cx_Oracle
import sys

def oracle_insert():
	conn=cx_Oracle.connect('SDADMIN/ADMIN@10.130.29.192/ccod')
#conn = cx_Oracle.connect('SDADMIN/ADMIN@10.130.41.208:1521/ccod')
#conn = cx_Oracle.connect('SDADMIN/ADMIN@127.0.0.1:117/ygdb')
	cursor = conn.cursor()
	sqlString = "insert into call_info_test_redial(transtime,dialtime,result,talk_duration,targetdn) values(0,1338,1,1,13465790912)";
	para =""
	count=1000000
	while count>0:
		cursor.execute(sqlString)
		count-=1
	cursor.close()
	conn.commit()
	conn.close()
oracle_insert()
