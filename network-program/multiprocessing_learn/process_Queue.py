#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    进程信息交互方式一:Queue
        实现了进程间的数据传递
        实际是通过拷贝多份，再合拼
"""

import multiprocessing

import queue
import threading


def f(q):
    q.put([42, None, 'hello'])


if __name__ == '__main__':
    q = multiprocessing.Queue()

    # threading
    # q = queue.Queue()
    # p = threading.Thread(target=f, args=(q,))

    p = multiprocessing.Process(target=f, args=(q,))
    p.start()
    print(q.get())
    p.join()
