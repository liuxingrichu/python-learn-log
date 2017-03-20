#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import os
import socket
import sys

IP = 'localhost'
PORT = 9999
RECV_SIZE = 1024
SEND_SIZE = 1024
MD5_SIZE = 32

SUCCESS = 200
NOT_FOUND = 404
MD5_ERROR = 300


class MyClient(object):
    def __init__(self):
        self.myclient = socket.socket()

    def connect(self):
        self.myclient.connect((IP, PORT))

    def get(self, filename):
        tmp_file = filename + '.tmp'
        if os.path.isfile(tmp_file):
            position = os.path.getsize(tmp_file)
        else:
            position = 0

        msg_dict = {'action': 'get',
                    'filename': filename,
                    'position': position,
                    }

        self.myclient.send(json.dumps(msg_dict).encode())

        feedback = self.myclient.recv(RECV_SIZE)
        msg_dict = json.loads(feedback.decode())
        status = msg_dict.get('status')
        if status == NOT_FOUND:
            print('\t%s is not exist.' % filename)
            return

        total_size = msg_dict.get('total')
        recv_size = 0
        m = hashlib.md5()
        with open(tmp_file, 'ab') as f:
            f.seek(position)
            while recv_size < total_size:
                if total_size - recv_size > RECV_SIZE:
                    buffer_size = RECV_SIZE
                else:
                    buffer_size = total_size - recv_size
                data = self.myclient.recv(buffer_size)
                f.write(data)
                m.update(data)
                recv_size += len(data)
                self.process_bar(recv_size, total_size)

        print()
        md5 = self.myclient.recv(RECV_SIZE).decode()
        if m.hexdigest() == md5:
            print('\t%s download success.' % filename)
            if os.path.isfile(filename):
                os.remove(filename)
            os.rename(tmp_file, filename)
        else:
            print('\t%s download fail.' % filename)
            os.remove(tmp_file)

    def put(self, filename):
        if not os.path.isfile(filename):
            print('\t%s is not exist.' % filename)
            return
        total = os.path.getsize(filename)

        msg_dict = {'action': 'put',
                    'filename': filename,
                    'total': total,
                    }
        self.myclient.send(json.dumps(msg_dict).encode())
        data = self.myclient.recv(RECV_SIZE).decode()
        msg_dict = json.loads(data)
        position = msg_dict['position']
        send_size = 0
        total_size = total - position
        m = hashlib.md5()
        with open(filename, 'rb') as f:
            f.seek(position)
            while send_size < total_size:
                if total_size - send_size > SEND_SIZE:
                    buffer_size = SEND_SIZE
                else:
                    buffer_size = total_size - send_size
                data = f.read(buffer_size)
                self.myclient.send(data)
                m.update(data)
                send_size += len(data)
                self.process_bar(send_size, total_size)
        print()
        md5 = self.myclient.recv(MD5_SIZE).decode()
        if md5 == m.hexdigest():
            print('\t%s upload success!' % filename)
            msg_dict['status'] = SUCCESS
            self.myclient.send(json.dumps(msg_dict).encode())
        else:
            print('\t%s upload fail!' % filename)
            msg_dict['status'] = MD5_ERROR
            self.myclient.send(json.dumps(msg_dict).encode())

    def process_bar(self, m, n):
        percent = int(m / n * 100)
        arrow = '=' * int(percent / 10) + '>'
        msg = '\r' + arrow + '%d%%' % percent
        sys.stdout.write(msg)
        sys.stdout.flush()

    def start(self):
        while True:
            cmd_str = input('>> ').strip()
            if not cmd_str:
                continue

            cmd = cmd_str.split(maxsplit=1)[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                args = cmd_str.replace(cmd, '', 1).lstrip()
                func(args)
            else:
                print('\tno function now!')

    def quit(self):
        self.myclient.close()


def main():
    client_obj = MyClient()
    client_obj.connect()
    client_obj.start()


if __name__ == '__main__':
    main()
