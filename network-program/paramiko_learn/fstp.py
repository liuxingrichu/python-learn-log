#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko

transport = paramiko.Transport(('IP', 22))

transport.connect(username='*', password='*')

sftp = paramiko.SFTPClient.from_transport(transport)

sftp.put('ssh.py', '/tmp/test.py')

sftp.get('/tmp/test.py', 'local_path')

transport.close()
