#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    进程间数据是独立
    下面程序使用锁的原因是进程间共享了打印屏幕
    为保证打印数据不会出现乱，而使用
"""

import multiprocessing


def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()


if __name__ == '__main__':
    lock = multiprocessing.Lock()

    for num in range(10):
        multiprocessing.Process(target=f, args=(lock, num)).start()
