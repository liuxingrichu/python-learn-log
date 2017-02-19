#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import os
import hashlib

server = socket.socket()
server.bind(('0.0.0.0', 9999))
server.listen()

while True:
    conn, addr = server.accept()
    while True:
        try:
            data = conn.recv(1024)
        except ConnectionResetError:
            print("\t\tclient is closed.")
            break

        cmd, filename = data.decode().split()

        if os.path.isfile(filename):
            f = open(filename, 'rb')
            m = hashlib.md5()
            file_size = os.stat(filename).st_size
            conn.send(str(file_size).encode())
            conn.recv(1024)
            for line in f:
                conn.send(line)
                m.update(line)

            conn.send(m.hexdigest().encode())
            print("\t\tfile send done")
            f.close()
        else:
            print("file not exist")

server.close()
