#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import json

import os
import socketserver
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from conf import server_settings
from conf import protocol
from common.log import logger


class MyFTPServer(socketserver.BaseRequestHandler):
    def authenticate(self, *args):
        data_dict = args[0]
        try:
            with open(server_settings.USER_INFO_PATH, 'r') as f:
                user_dict = json.loads(f.read())
        except FileNotFoundError:
            logger.error("\t请初始化数据库")
            data_dict['status_code'] = protocol.LOGIN_ERROR
            self.request.send(json.dumps(data_dict).encode())
            return

        if data_dict['USER_ID'] in user_dict:
            data_dict['status_code'] = protocol.SUCCESS_CODE
            self.request.send(json.dumps(data_dict).encode())
            logger.info('%s login success' % data_dict['username'])
            # user home
            user_path = os.path.join(server_settings.HOME_PATH,
                                     data_dict['username'])
            if not os.path.exists(user_path):
                os.makedirs(user_path)
        else:
            data_dict['status_code'] = protocol.LOGIN_ERROR
            self.request.send(json.dumps(data_dict).encode())
            logger.warning('%s login fail' % data_dict['username'])

    def push(self, *args):
        cmd_dict = args[0]
        filename = cmd_dict['filename']
        filesize = cmd_dict['filesize']
        user_id = cmd_dict['USER_ID']
        username = cmd_dict['username']

        # check disk space
        with open(server_settings.USER_INFO_PATH, 'r') as f:
            usr_dict = json.loads(f.read())

        if usr_dict[user_id]['disk_free'] < filesize:
            cmd_dict['status_code'] = protocol.DISK_NOT_ENOUGH
            self.request.send(json.dumps(cmd_dict).encode())
            logger.warning('%s of disk space is not enough' % username)
            return
        else:
            cmd_dict['status_code'] = protocol.DISK_ENOUGH
            self.request.send(json.dumps(cmd_dict).encode())

        # receive file
        receive_size = 0
        m = hashlib.md5()
        save_path = os.path.join(server_settings.HOME_PATH, username, filename)

        # same file exist
        if os.path.isfile(save_path):
            old_file_size = os.stat(save_path).st_size
        else:
            old_file_size = 0

        f = open(save_path, 'wb')
        while receive_size < filesize:
            # avoid stick package
            if filesize - receive_size > server_settings.RECV_SIZE:
                SIZE = server_settings.RECV_SIZE
            else:
                SIZE = filesize - receive_size

            data = self.request.recv(SIZE)
            f.write(data)
            m.update(data)
            receive_size += len(data)
        else:
            f.close()
            logger.info('%s transfer file %s done' % (username, filename))

        self.data = self.request.recv(server_settings.RECV_SIZE)
        data_dict = json.loads(self.data.decode())
        if data_dict['FILE_ID'] == m.hexdigest():
            logger.info('%s push file %s success' % (username, filename))
            cmd_dict['status_code'] = protocol.SUCCESS_CODE
            self.request.send(json.dumps(cmd_dict).encode())

            # fresh disk space info
            used_size = filesize - old_file_size
            usr_dict[user_id]['disk_free'] -= used_size
            usr_dict[user_id]['disk_used'] += used_size
            with open(server_settings.USER_INFO_PATH, 'w+') as f:
                f.write(json.dumps(usr_dict))
            logger.info('%s disk space info fresh success' % username)

        else:
            logger.info('push file %s fail' % filename)
            cmd_dict['status_code'] = protocol.FILE_ID_ERROR
            self.request.send(json.dumps(cmd_dict).encode())
            if os.path.isfile(filename):
                os.remove(filename)
                logger.info('%s delete file %s success' % (username, filename))

    def pull(self, *args):
        cmd_dict = args[0]
        filename = cmd_dict['filename']
        username = cmd_dict['username']

        home_path = os.path.join(server_settings.HOME_PATH, username, filename)
        if not os.path.isfile(home_path):
            cmd_dict['status_code'] = protocol.FILE_NOT_EXIST
            self.request.send(json.dumps(cmd_dict).encode())
            logger.warning('%s: %s is not exist' % (username, filename))
            return
        else:
            cmd_dict['status_code'] = protocol.SUCCESS_CODE
            cmd_dict['filesize'] = os.stat(home_path).st_size
            self.request.send(json.dumps(cmd_dict).encode())
            logger.info('%s start to transfer %s' % (username, filename))

        # avoid stick package
        self.request.recv(server_settings.RECV_SIZE)

        m = hashlib.md5()
        f = open(home_path, 'rb')
        for line in f:
            self.request.send(line)
            m.update(line)
        else:
            f.close()
            cmd_dict['FILE_ID'] = m.hexdigest()
            self.request.send(json.dumps(cmd_dict).encode())
            logger.info('%s has finished to transfer %s' % (username, filename))

    def ls(self):
        pass

    def cd(self, dirname):
        pass

    def pwd(self):
        pass

    def quit(self, *args):
        cmd_dict = args[0]
        logger.info('%s quit' % cmd_dict['username'])

    def handle(self):
        while True:
            try:
                self.data = self.request.recv(server_settings.RECV_SIZE)
                if not self.data:
                    break

                cmd_dict = json.loads(self.data.decode())
                action = cmd_dict['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dict)
            except ConnectionResetError:
                logger.warning('client disconnect')
                break


def main():
    server = socketserver.ThreadingTCPServer(
        (server_settings.IP, server_settings.PORT), MyFTPServer)
    server.serve_forever()


if __name__ == '__main__':
    main()
