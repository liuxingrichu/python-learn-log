#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

import socket
import hashlib

import os
import sys
import time

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from conf import protocol
from client_log import logger

RECV_SIZE = 1024
IP = 'localhost'
PORT = 9999


class FTPClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.username = None
        self.USER_ID = None
        self.home = os.path.join(BASE_PATH, 'home')
        self.show = list()

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
            logger.warning('need 2 parameters, but give %s parameters' %
                           len(cmd_list))
            return

        filename = cmd_list[1]
        if not os.path.isfile(filename):
            logger.warning('file: %s is not exist' % filename)
            return

        filesize = os.stat(filename).st_size
        msg_dict = {
            'username': self.username,
            'USER_ID': self.USER_ID,
            'action': 'push',
            'filename': filename,
            'filesize': filesize,
        }
        self.client.send(json.dumps(msg_dict).encode())

        res_data = self.client.recv(RECV_SIZE)
        res_dict = json.loads(res_data.decode())
        if res_dict['status_code'] == protocol.DISK_NOT_ENOUGH:
            logger.warning('disk space is not enough')
            return

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
            logger.info('upload file: %s success' % filename)
        else:
            logger.info('upload file: %s fail' % filename)

    def pull(self, *args):
        cmd_list = args[0].split()
        if len(cmd_list) != 2:
            logger.warning('need 2 parameters, but give %s parameters' %
                           len(cmd_list))
            return

        filename = cmd_list[1]
        msg_dict = {
            'username': self.username,
            'action': 'pull',
            'filename': filename,
        }
        self.client.send(json.dumps(msg_dict).encode())
        self.data = self.client.recv(RECV_SIZE)
        res_dict = json.loads(self.data.decode())
        if res_dict['status_code'] == protocol.FILE_NOT_EXIST:
            logger.warning('file %s is not exist' % filename)
            return
        else:
            self.client.send(b'ok')
            logger.info('file %s is receiving ...' % filename)

        receive_size = 0
        m = hashlib.md5()
        filesize = res_dict['filesize']
        self.show = [x for x in range(10, 0, -1)]
        f = open(filename, 'wb')
        while receive_size < filesize:
            if filesize - receive_size > RECV_SIZE:
                SIZE = RECV_SIZE
            else:
                SIZE = filesize - receive_size
            data = self.client.recv(SIZE)
            f.write(data)
            m.update(data)
            receive_size += len(data)
            self.show_bar(receive_size, filesize)
        else:
            f.close()
            logger.info('file %s has received done' % filename)
            data = self.client.recv(RECV_SIZE)
            res_dict = json.loads(data.decode())
            if res_dict['FILE_ID'] == m.hexdigest():
                logger.info('file %s has downloaded successfully' % filename)
            else:
                logger.info('file %s has downloaded fail' % filename)
                if os.path.isfile(filename):
                    os.remove(filename)

    def ls(self, *args):
        msg_dict = {
            'username': self.username,
            'action': 'ls',
            'path': self.home,
        }
        self.client.send(json.dumps(msg_dict).encode())
        self.data = self.client.recv(RECV_SIZE)
        res_dict = json.loads(self.data.decode())
        content_list = res_dict['content']
        print('content list'.center(20, '-'))
        for content in content_list:
            print(content)
        print('-' * 20)

    def cd(self, *args):
        cmd_list = args[0].split()
        if len(cmd_list) != 2:
            logger.warning('need 2 parameters, but give %s parameters' %
                           len(cmd_list))
            return

        path_list = self.home.split(os.sep)
        index = path_list.index(self.username)
        if cmd_list[1] == '..':
            if index + 1 < len(path_list):
                path_list.pop()
                self.home = os.sep.join(path_list)
            else:
                logger.warning('You must change directory in home directory')
        else:
            msg_dict = {
                'username': self.username,
                'action': 'cd',
                'dirname': cmd_list[1],
                'path': self.home,
            }
            self.client.send(json.dumps(msg_dict).encode())
            data = self.client.recv(RECV_SIZE)
            res_dict = json.loads(data.decode())
            if res_dict['status_code'] == protocol.SUCCESS_CODE:
                path_list.append(cmd_list[1])
                self.home = os.sep.join(path_list)
            elif res_dict['status_code'] == protocol.FILE_DIR_NOT_EXIST:
                logger.warning('No such file or directory')
            else:
                logger.warning('Not a directory')

    def pwd(self, *args):
        path_list = self.home.split(os.sep)
        index = path_list.index('home')
        if os.path.isfile(path_list[-1]):
            path = '/'.join(path_list[index:-1])
        else:
            path = '/'.join(path_list[index:])
        print('/%s' % path)

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
                print('\t\033[32;0mwelcome %s\033[0m' % username)

            while True:
                path_list = self.home.split(os.sep)
                if os.path.isfile(path_list[-1]):
                    position = path_list[-2]
                else:
                    position = path_list[-1]
                cmd = input('[%s@%s]$ ' % (self.username, position)).strip()
                if len(cmd) == 0:
                    continue

                cmd_str = cmd.split()[0]
                if hasattr(self, cmd_str):
                    func = getattr(self, cmd_str)
                    func(cmd)
                else:
                    print('\t\033[32;0m请输入help，进行查询\033[0m')

                time.sleep(0.1)

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

    def show_bar(self, recv_size, total):
        if int((recv_size / total) * 10) in self.show:
            logger.info('recv ..... {0:.2%}'.format(recv_size / total))
            self.show.pop()


def main():
    client_obj = FTPClient()
    client_obj.connect(IP, PORT)
    client_obj.interaction()


if __name__ == '__main__':
    main()
