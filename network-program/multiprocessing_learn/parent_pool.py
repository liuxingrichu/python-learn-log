#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    系统起多个线程，会导致CPU切换过于频换，系统反应变慢。
    系统起多个进程，会导致系统奔溃，故使用进程池。
"""

from  multiprocessing import Process, Pool
import os
import time


def Foo(i):
    time.sleep(2)
    print('son process: ', os.getpid())
    return i + 100


def Bar(arg):
    print('-->exec done:', arg, os.getpid())


if __name__ == '__main__':
    # 运行进程池内，同时放入5个执行
    pool = Pool(5)

    print('parent process: ', os.getpid())
    for i in range(10):
        # 并行执行， callback是回调函数，func执行完，就执行callback
        # 父进程调用callback
        pool.apply_async(func=Foo, args=(i,), callback=Bar)
        # 串行执行
        # pool.apply(func=Foo, args=(i,))
        # pool.apply_async(func=Foo, args=(i,))

    print('end')
    pool.close()
    # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    pool.join()

    # 注：一定是先close，再join
