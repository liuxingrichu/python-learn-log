#!/usr/bin/env python
# -*- coding:utf-8 -*-


import socket
import hashlib

client = socket.socket()

client.connect(('localhost', 9999))

while True:
    cmd = input(">>").strip()
    if len(cmd) == 0:
        continue

    if cmd.startswith('get'):
        client.send(cmd.encode())
        server_respond = client.recv(1024)

        client.send("ready to receive file".encode())

        file_total_size = int(server_respond.decode())
        received_size = 0
        filename = cmd.split()[1]
        m = hashlib.md5()
        f = open(filename, 'wb')
        while received_size < file_total_size:
            # avoid stick package
            if file_total_size - received_size > 1024:
                size = 1024
            else:
                size = file_total_size - received_size

            data = client.recv(size)
            f.write(data)
            m.update(data)
            received_size += len(data)
        else:
            f.close()
            server_md5 = client.recv(1024)

            if server_md5.decode() == m.hexdigest():
                print("\t\tfile download success")
            else:
                print("\t\tfile download fail")

client.close()
