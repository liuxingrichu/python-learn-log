#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import os

server = socket.socket()

server.bind(('localhost', 9999))
server.listen()

while True:
    conn, addr = server.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            print("client is closed.")
            break
        cmd_res = os.popen(data.decode()).read()
        if len(cmd_res) == 0:
            conn.send("no data".encode())
        else:
            conn.send(cmd_res.encode())

server.close()
