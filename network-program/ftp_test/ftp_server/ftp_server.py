#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import socketserver
import json


class NyTCPHandler(socketserver.BaseRequestHandler):
    def push(self, *args):
        'receive client data'
        cmd_dict = args[0]
        filename = cmd_dict['filename']
        filesize = cmd_dict['size']
        if os.path.isfile(filename):
            f = open(filename + '.new', 'wb')
        else:
            f = open(filename, 'wb')
        self.request.send(b'200 ok')
        receive_size = 0
        while receive_size < filesize:
            data = self.request.recv(1024)
            f.write(data)
            receive_size += len(data)
        else:
            print('file [%s] has done' % filename)
            f.close()

    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print(self.data)
                cmd_dict = json.loads(self.data.decode())
                action = cmd_dict['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dict)
            except ConnectionResetError as e:
                print('err:', e)
                break


if __name__ == '__main__':
    IP, PORT = 'localhost', 9999
    server = socketserver.ThreadingTCPServer((IP, PORT), NyTCPHandler)
    server.serve_forever()
