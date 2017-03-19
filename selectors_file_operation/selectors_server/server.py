#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import os
import selectors
import socket

IP = '0.0.0.0'
PORT = 9999
RECV_SIZE = 1024
READ_SIZE = 1024


class MyServer(object):
    def __init__(self):
        self.myserver = socket.socket()
        self.myserver.bind((IP, PORT))
        self.myserver.setblocking(False)
        self.myserver.listen(1000)
        self.sel = selectors.SelectSelector()
        self.request = None

    def start(self):
        self.sel.register(self.myserver, selectors.EVENT_READ, self.accept)
        while True:
            for key, mask in self.sel.select():
                callable = key.data
                callable(key.fileobj, mask)

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(True)
        self.request = conn
        self.sel.register(conn, selectors.EVENT_READ, self.handle)

    def handle(self, conn, mask):
        try:
            data = conn.recv(RECV_SIZE)
            data = json.loads(data.decode())
            cmd = data.get('action')
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(data)
            else:
                print('no functions now!')
        except ConnectionResetError:
            self.sel.unregister(conn)
            conn.close()

    def get(self, *args):
        msg_dict = args[0]
        filename = msg_dict['filename']
        position = msg_dict['position']
        if not os.path.isfile(filename):
            msg_dict['status'] = '404'
            self.request.send(json.dumps(msg_dict).encode())
            return
        else:
            msg_dict['status'] = '200'
            total_size = os.path.getsize(filename) - position
            msg_dict['total'] = total_size
            self.request.send(json.dumps(msg_dict).encode())

        send_size = 0
        m = hashlib.md5()
        with open(filename, 'rb') as f:
            f.seek(position)
            while send_size < total_size:
                if total_size - send_size > READ_SIZE:
                    buffer_size = READ_SIZE
                else:
                    buffer_size = total_size - send_size
                data = f.read(buffer_size)
                send_size += len(data)
                m.update(data)
                self.request.send(data)

        self.request.send(m.hexdigest().encode())

    def put(self, *args):
        pass


def main():
    server_obj = MyServer()
    server_obj.start()


if __name__ == '__main__':
    main()
