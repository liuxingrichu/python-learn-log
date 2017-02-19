#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket

client = socket.socket()

client.connect(('localhost', 9999))

while True:
    cmd = input(">>").strip()
    if len(cmd) == 0:
        continue
    client.send(cmd.encode())

    data = client.recv(1024)
    print(data.decode())

client.close()
