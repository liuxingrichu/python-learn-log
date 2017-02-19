#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import os
import time

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

        cmd_res = os.popen(data.decode()).read()

        if len(cmd_res) == 0:
            # send must not empty, 400：no data
            conn.send("400".encode())
            continue
        """
        send cmd_res size
        assure server send data size and client receive data size same
        must encode cmd_res, especially, Chinese character.
        """
        cmd_size = conn.send(str(len(cmd_res.encode())).encode())

        # method1: avoid stick package(不推荐)
        # time.sleep(0.5)

        # method2: avoid stick package
        conn.recv(1024)

        conn.send(cmd_res.encode())

server.close()
