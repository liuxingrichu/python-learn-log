#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

RECV_SIZE = 1024
IP = '0.0.0.0'
PORT = 9999

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_PATH = os.path.join(BASE_PATH, 'home')
# LOG_PATH = os.path.join(BASE_PATH, 'log', 'ftp_server.log')
USER_INFO_PATH = os.path.join(BASE_PATH, 'database', 'user_info.db')




