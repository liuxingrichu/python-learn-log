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

    cmd_res_size = client.recv(1024)

    if cmd_res_size.decode() == '400':
        print("\t\tno data")
        continue

    # method2: avoid stick package
    client.send("可以接受数据了".encode())

    cmd_res_size = int(cmd_res_size.decode())
    received_size = 0
    received_data = b''

    while received_size < cmd_res_size:
        remainder_size = cmd_res_size - received_size
        if remainder_size > 1024:
            data = client.recv(1024)
            received_data += data
            received_size += 1024
        else:
            # method3: avoid stick package
            data = client.recv(remainder_size)
            received_data += data
            received_size += remainder_size
    else:
        print("\t\tdata receive done")

    print("recv size: ", received_size)
    print(received_data.decode())

client.close()
