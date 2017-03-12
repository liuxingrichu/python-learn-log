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
        if len(cmd_list) != 3:
            print('Err: need 2 parameters, but give %s parameters' % (
                len(cmd_list) - 1))
            return

        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.put(cmd_list[1], cmd_list[2])
        except PermissionError:
            print('%s'.center(36, '-') % self.host)
            print('\033[31;0m\tYou do not have the permission.\033[0m')
        except FileNotFoundError:
            print('%s'.center(36, '-') % self.host)
            print('\033[31;0m\t%s is not exist.\033[0m' % cmd_list[1])
        transport.close()

    def get(self, *args):
        cmd_list = re.split('\s+', args[0])
        if len(cmd_list) != 3:
            print('Err: need 2 parameters, but give %s parameters' % (
                len(cmd_list) - 1))
            return

        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.get(cmd_list[1], cmd_list[2])
        except PermissionError:
            print('%s'.center(36, '-') % self.host)
            print('\033[31;0m\tYou do not have the permission.\033[0m')
            os.remove(cmd_list[2])
        except FileNotFoundError:
            print('%s'.center(36, '-') % self.host)
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
            print('%s'.center(36, '-') % self.host)
            print(result.decode())
            print('end'.center(48, '-'))
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
        print('设备清单'.center(36, '-'))
        for k in host_dict:
            print(k, end='\t')
            for v in host_dict[k]:
                print(v, end='\t')
            print()
        print('end'.center(40, '-'))

        group = input('选择组名：').strip()
        if group == 'q':
            break

        if group not in host_dict:
            continue

        host_list = []
        for host in host_dict[group]:
            host_list.append(host)

        thread_list = []

        while True:
            cmd = input('>>').strip()
            if cmd == 'q':
                break
            if not cmd:
                continue

            for host in host_list:
                port = host_dict[group][host]['port']
                username = host_dict[group][host]['username']
                password = host_dict[group][host]['password']

                host_obj = RemoteHost(host, port, username, password)
                t = threading.Thread(target=host_obj.run, args=(cmd,))
                t.start()
                thread_list.append(t)

            for t in thread_list:
                t.join()


if __name__ == '__main__':
    main()
