#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    存在yield的函数是生成器，只有调用__next__方法才执行
    下面程序是通过yield实现了一个简单的协程
"""

import time
import queue


def consumer(name):
    print("--->starting eating baozi...")
    while True:
        # yield xx #xx 表示返回值，下面程序无返回值
        # new_baozi为输入值
        new_baozi = yield
        print("[%s] is eating baozi %s" % (name, new_baozi))
        # time.sleep(1)


def producer():
    r = con.__next__()
    r = con2.__next__()
    n = 0
    while n < 5:
        n += 1
        con.send(n)
        con2.send(n)
        print("\033[32;1m[producer]\033[0m is making baozi %s" % n)


if __name__ == '__main__':
    con = consumer("c1")
    con2 = consumer("c2")
    p = producer()
