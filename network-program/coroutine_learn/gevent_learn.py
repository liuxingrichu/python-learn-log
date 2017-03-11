#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    遇到IO操作，就自动切换
"""

import gevent


def func1():
    print('\033[31;1mrun func1\033[0m')
    gevent.sleep(2)
    print('\033[31;1mgo back func1 again\033[0m')


def func2():
    print('\033[32;1mrun func2\033[0m')
    gevent.sleep(1)
    print('\033[32;1mgo back func2 again\033[0m')


def func3():
    print('run func3')
    gevent.sleep(0)
    print('go back func3 again')


gevent.joinall([
    gevent.spawn(func1),
    gevent.spawn(func2),
    gevent.spawn(func3),
])
