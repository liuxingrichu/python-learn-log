#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import sys

messages = [b'hello world',
            b'nice to meet you',
            b'fine, thanks']

socket_address = ('localhost', 10000)

socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(500)]

for s in socks:
    s.connect(socket_address)

for message in messages:
    for s in socks:
        print('%s sends %s' % (s.getsockname(), message))
        s.send(message)

    for s in socks:
        data = s.recv(1024)
        print('%s receives %s' % (s.getsockname(), data))
        if not data:
            print(sys.stderr, 'closing client', s.getsockname())
