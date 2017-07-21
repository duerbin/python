#########################################################################
# -*- coding: utf-8 -*-
#File Name: test.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014年03月17日 星期一 10时07分54秒
#########################################################################
#!/usr/bin/env python
import logging
import logging.config

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("puppet")

logger.debug('This is debug message')
logger.info('This is info message')
logger.warning('This is warning message')

