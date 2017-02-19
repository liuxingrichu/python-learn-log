#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    实现类
    """

    def handle(self):
        """
        复写
        """
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                self.request.send(self.data.upper())
            except ConnectionResetError as e:
                print("err: ", e)
                break


if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    # only client
    # server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # supervene
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
