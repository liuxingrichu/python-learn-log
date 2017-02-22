#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import socket


class FTPClient(object):
    def __init__(self):
        self.client = socket.socket()

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def cmd_pull(self):
        pass

    def cmd_push(self, *args):
        cmd_list = args[0].split()
        if len(cmd_list) > 1:
            filename = cmd_list[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dict = {
                    'action': 'push',
                    'filename': filename,
                    'size': filesize,
                    'overridden': True,
                }
                self.client.send(json.dumps(msg_dict).encode())
                # avoid stick package, rev :200
                server_response = self.client.recv(1024)
                f = open(filename, 'rb')
                for line in f:
                    self.client.send(line)
                else:
                    print('file send done')
                    f.close()
            else:
                print(filename, 'is not exist')

    def help(self):
        msg = """
        ls
        pwd
        cd ..
        pull filename
        push filename
        """

    def interactive(self):
        # self.authenticate()
        while True:
            cmd = input('>>').strip()
            if len(cmd) == 0:
                continue
            cmd_str = cmd.split()[0]

            if hasattr(self, 'cmd_%s' % cmd_str):
                func = getattr(self, 'cmd_%s' % cmd_str)
                func(cmd)
            else:
                self.help()

ftp = FTPClient()
ftp.connect('localhost', 9999)
ftp.interactive()