#########################################################################
# -*- coding: utf-8 -*-
#File Name: ConfigOperater.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014��03��17�� ����һ 10ʱ07��54��
# desc:��װConfigParseģ�� 
#########################################################################
#!/usr/bin/env python
import codecs
import ConfigParser

class CCpOperater:
    """
    ע�⣺Key��ֵֻ����Сд
    """
    config = None
    fileName = ''
        
    def __init__(self, filename, strcode=""):
        self.config = ConfigParser.ConfigParser()
        self.fileName = filename
        if not strcode:
            self.config.read(self.fileName)
        else:
            if strcode.lower() == "utf-8-sig" or strcode.lower() == "utf-8" or strcode.lower() == "utf-16":
                fp = codecs.open(filename, "r", strcode)
                if not fp:
                    raise "config file maybe not exist."
                else:
                    self.config.readfp(fp)
            else:
                self.config.read(self.fileName)

    def writeIni(self, sectionName, keyName, value):
        if sectionName not in self.config.sections():
            self.config.add_section(sectionName)
            
        self.config.set(sectionName, keyName, value)
        self.config.write(open(self.fileName, "w"))

    def readIniStr(self, sectionName, keyName):
        keyName = keyName.lower()
        if sectionName in self.config.sections() and keyName in self.config.options(sectionName):
            return self.config.get(sectionName, keyName)
        else:
            return None

    def readIniInt(self, sectionName, keyName):
        keyName = keyName.lower()
        try:
            if sectionName in self.config.sections() and keyName in self.config.options(sectionName):
                return self.config.getint(sectionName, keyName)
            else:
                return None
        except Exception, e:
            print '    Exception: ', e
            return None

    def __del__(self):
        pass