#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

import socket
import hashlib

import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from conf import protocol

RECV_SIZE = 1024
IP = 'localhost'
PORT = 9999


class FTPClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.username = None
        self.USER_ID = None
        self.home = os.path.join(BASE_PATH, 'home')
        self.status = False

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def authenticate(self, username, password):
        m = hashlib.md5(password.encode())
        m.update(username.encode())

        msg_dict = {
            'username': username,
            'action': 'authenticate',
            'USER_ID': m.hexdigest()
        }
        self.client.send(json.dumps(msg_dict).encode())

        recv_dict = self.client.recv(RECV_SIZE)
        data_dict = json.loads(recv_dict.decode())
        if data_dict.get('status_code') == protocol.SUCCESS_CODE:
            self.username = username
            self.USER_ID = m.hexdigest()
            self.home = os.path.join(self.home, username)
            return True
        else:
            return False

    def push(self, *args):
        cmd_list = args[0].split()
        if len(cmd_list) != 2:
            return protocol.AUTH_NUM_ERROR

        filename = cmd_list[1]
        if not os.path.isfile(filename):
            return protocol.ARGS_NAME_ERROR

        filesize = os.stat(filename).st_size
        msg_dict = {
            'username': self.username,
            'USER_ID': self.USER_ID,
            'action': 'push',
            'filename': filename,
            'filesize': filesize,
        }
        self.client.send(json.dumps(msg_dict).encode())
        res = self.client.recv(RECV_SIZE)
        if res == protocol.DISK_NOT_ENOUGH:
            return protocol.DISK_NOT_ENOUGH

        m = hashlib.md5()
        f = open(filename, 'rb')
        for line in f:
            self.client.send(line)
            m.update(line)
        else:
            f.close()

            msg_dict['FILE_ID'] = m.hexdigest()
            self.client.send(json.dumps(msg_dict).encode())
            data = self.client.recv(RECV_SIZE)
            data_dict = json.loads(data.decode())
            if data_dict['status_code'] == protocol.SUCCESS_CODE:
                return protocol.SUCCESS_CODE
            else:
                return protocol.FILE_ID_ERROR

    def pull(self, filename):
        pass


    def ls(self):
        pass

    def cd(self, dirname):
        pass

    def pwd(self):
        pass

    def interaction(self):
        while True:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if not username or not password:
                print('\t\033[31;0m用户名和密码，皆不能为空\033[0m')
                continue

            res = self.authenticate(username, password)
            if not res:
                print('\t\033[31;0m用户名或密码错误\033[0m')
                continue
            else:
                print('\t welcome %s' % username)

            while True:
                cmd = input("Enter command: ").strip()
                if len(cmd) == 0:
                    continue

                cmd_str = cmd.split()[0]
                if hasattr(self, cmd_str):
                    func = getattr(self, cmd_str)
                    res = func(cmd)
                    if res == protocol.AUTH_NUM_ERROR:
                        print('\t\033[31;0m参数个数有误\033[0m')
                    elif res == protocol.ARGS_NAME_ERROR:
                        print('\t\033[31;0m参数有误\033[0m')
                    elif res == protocol.SUCCESS_CODE:
                        print('\t\033[32;0m%s 操作成功\033[0m' % cmd)
                    else:
                        pass
                else:
                    print('\t\033[32;0m请输入help，进行查询\033[0m')

    def help(self, *args):
        msg = """
        ls
        pwd
        cd ..
        cd dirname
        push filename
        pull filename
        """
        print("请输入以下命令：")
        print(msg)

    def quit(self, *args):
        msg_dict = {
            'action': 'quit',
            'username': self.username
        }
        self.client.send(json.dumps(msg_dict).encode())
        self.client.close()
        sys.exit()


def main():
    client_obj = FTPClient()
    client_obj.connect(IP, PORT)
    client_obj.interaction()


if __name__ == '__main__':
    main()
