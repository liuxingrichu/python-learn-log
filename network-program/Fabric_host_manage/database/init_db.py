#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

host_dict = {
    '10.0.0.10': {'username': 'Tom',
                  'password': '100',
                  'port': 22,
                  },
    '10.0.0.11': {'username': 'Lucy',
                  'password': '110',
                  'port': 22,
                  },
}


def main():
    with open('host_info.db', 'w') as f:
        f.write(json.dumps(host_dict))


if __name__ == '__main__':
    main()
