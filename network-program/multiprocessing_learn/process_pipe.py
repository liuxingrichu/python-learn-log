#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    两个进程信息交互方式二:Pipe
        实现了进程间的数据传递
        实际是通过拷贝多份，再合拼
"""

import multiprocessing


def f(conn):
    conn.send([42, None, 'hello from child'])
    conn.send([42, None, 'hello from child2'])
    print('from parent:', conn.recv())
    conn.close()


if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    print(parent_conn.recv())
    parent_conn.send('hello child')
    p.join()
