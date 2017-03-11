#!/usr/bin/env python
# -*- coding:utf-8 -*-

import select
import socket
import queue

server = socket.socket()
server.bind(('localhost', 9000))
server.listen(1000)

# non-blocking
server.setblocking(False)
msg_dict = dict()

inputs = [server, ]
outputs = list()

while True:
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)
    # print(readable, writeable, exceptional)

    for r in readable:
        if r is server:  # come a new client
            conn, addr = server.accept()
            # print(conn, addr)
            conn.setblocking(False)
            inputs.append(conn)
            msg_dict[conn] = queue.Queue()
        else:
            data = r.recv(1024)
            if data:
                print('receive data: ', data)
                # r.send(data)
                msg_dict[r].put(data)

                outputs.append(r)
            else:
                # print('client is down')
                inputs.remove(r)
                if r in outputs:
                    outputs.remove(r)

                del msg_dict[r]

    for w in writeable:
        try:
            next_msg = msg_dict[w].get_nowait()
        except queue.Empty:
            # print("client [%s]" % w.getpeername()[0], "queue is empty..")
            outputs.remove(w)
        else:
            print("sending msg to [%s]" % w.getpeername()[0], next_msg)
            w.send(next_msg)

    for e in exceptional:
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)
        e.close()

        del msg_dict[e]
