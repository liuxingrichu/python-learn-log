#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from conf import server_settings

"""
#log level from high to low
logging.CRITICAL
logging.ERROR
logging.WARNING
logging.INFO
logging.DEBUG
logging.NOTSET
"""


# create logger
logger = logging.getLogger('mylogger')

# set logger level, default: logging.WARNING
logger.setLevel(logging.DEBUG)

# create file handler and save log file path
fh = logging.FileHandler('server_log.log')

# create console handler
ch = logging.StreamHandler()

# set a pattern for formatter
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# formatter = logging.Formatter(
#     '%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add handler for logger
logger.addHandler(fh)
logger.addHandler(ch)
