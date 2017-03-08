#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
import threading
import paramiko
import sys
import re

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
DB_PATH = os.path.join(BASE_PATH, 'database')


class RemoteHost(object):
    """
    remote manage host
    """
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def put(self, *args):
        cmd_list = re.split('\s+', args[0])
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.put(cmd_list[1], cmd_list[2])
        except PermissionError:
            print('\033[31;0m\tYou do not have the permission.\033[0m')
        except FileNotFoundError:
            print('\033[31;0m\t%s is not exist.\033[0m' % cmd_list[1])
        transport.close()

    def get(self, *args):
        cmd_list = re.split('\s+', args[0])
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.get(cmd_list[1], cmd_list[2])
        except PermissionError:
            print('\033[31;0m\tYou do not have the permission.\033[0m')
            os.remove(cmd_list[2])
        except FileNotFoundError:
            print('\033[31;0m\t%s is not exist.\033[0m' % cmd_list[1])
            os.remove(cmd_list[2])
        transport.close()

    def run(self, cmd):
        cmd_list = re.split('\s+', cmd)
        action = cmd_list[0]
        if hasattr(self, action):
            func = getattr(self, action)
            func(cmd)
        else:
            self.command(cmd)

    def command(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port, self.username,
                    self.password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        res = stdout.read()
        result = res if res else stderr.read()
        if result:
            print(result.decode())
        ssh.close()


def main():
    try:
        file = os.path.join(DB_PATH, 'host_info.db')
        with open(file, 'r') as f:
            host_dict = json.loads(f.read())
    except FileNotFoundError:
        print("\033[31;0m\thost information isn't exist\033[0m")
        sys.exit()

    while True:
        print('主机信息'.center(26, '-'))
        for n, k in enumerate(host_dict):
            print('主机', n + 1, k)
        print('end'.center(30, '-'))

        host = input('选择主机：').strip()
        if host == 'q':
            break
        if host not in host_dict:
            continue

        port = host_dict[host]['port']
        username = host_dict[host]['username']
        password = host_dict[host]['password']

        host_obj = RemoteHost(host, port, username, password)

        while True:
            cmd = input('[%s@%s]$ '% (username, host)).strip()
            if cmd == 'q':
                break
            if not cmd:
                continue

            t = threading.Thread(target=host_obj.run, args=(cmd,))
            t.start()
            t.join()


if __name__ == '__main__':
    main()
