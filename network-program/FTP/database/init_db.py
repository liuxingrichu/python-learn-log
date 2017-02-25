#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import hashlib

user_info = [
    {
        'username': 'Tom',
        'password': '123',
        'disk_space': 1024,
        'disk_used': 0,
        'disk_free': 1024,
    },
    {
        'username': 'Lucy',
        'password': '123',
        'disk_space': 512,
        'disk_used': 0,
        'disk_free': 512,
    },
    {
        'username': 'John',
        'password': '123',
        'disk_space': 2048,
        'disk_used': 0,
        'disk_free': 2048,
    },
]


def main():
    user_dict = {}
    for tmp_dict in user_info:
        m = hashlib.md5()
        m.update(tmp_dict['password'].encode())
        tmp_dict['password'] = m.hexdigest()
        m.update(tmp_dict['username'].encode())
        user_dict[m.hexdigest()] = tmp_dict

    with open('user_info.db', 'wb') as f:
        f.write(json.dumps(user_dict).encode())


if __name__ == '__main__':
    main()
