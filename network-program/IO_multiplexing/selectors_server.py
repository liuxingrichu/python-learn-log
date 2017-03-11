#!/usr/bin/env python
# -*- coding:utf-8 -*-

import selectors
import socket

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()
    # print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1000)
    if data:
        # print('echoing', repr(data), 'to', conn)
        conn.send(data)
    else:
        # print('closing', conn)
        sel.unregister(conn)
        conn.close()


sock = socket.socket()
sock.bind(('localhost', 10000))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    # 默认阻塞，不阻塞就有数据了
    # events就是连接的列表
    events = sel.select()

    for key, mask in events:
        # print('key.data: ', key.data)
        # print('key.fileobj:', key.fileobj)
        # key.data就是accept
        callback = key.data
        # key.fileobj就是conn
        callback(key.fileobj, mask)
