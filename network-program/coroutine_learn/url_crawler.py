#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gevent import monkey
import gevent
import time
from  urllib.request import urlopen



# 将当前程序进行IO操作，进行标记
# 因为gevent默认是无法知道urllib进行了IO操作
monkey.patch_all()


def f(url):
    print('GET: %s' % url)
    resp = urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))


urls = ['https://www.python.org/',
        'https://www.yahoo.com/',
        'https://github.com/']

start_time = time.time()
for url in urls:
    f(url)
print('同步需要时间: ', time.time() - start_time)

async_start_time = time.time()
gevent.joinall([
    gevent.spawn(f, 'https://www.python.org/'),
    gevent.spawn(f, 'https://www.yahoo.com/'),
    gevent.spawn(f, 'https://github.com/'),
])
print('异步需要时间', time.time() - async_start_time)
