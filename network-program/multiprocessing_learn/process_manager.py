#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    多个进程间的数据共享
    实现方式：Manager
        Manager内部实现使用了锁，自己无需加锁
        实际是通过拷贝多份，再合拼
"""

import multiprocessing
import os


def f(d, l):
    d[os.getpid()] = os.getpid()
    l.append(os.getpid())
    print(l)


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        d = manager.dict()
        l = manager.list(range(5))
        p_list = []

        for i in range(10):
            p = multiprocessing.Process(target=f, args=(d, l))
            p.start()
            p_list.append(p)

        for res in p_list:
            res.join()

        print(d)
        print(l)
