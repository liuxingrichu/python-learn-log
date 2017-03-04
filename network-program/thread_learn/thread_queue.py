#!/usr/bin/env python
# -*- coding:utf-8 -*-

import queue
import threading
import time

q = queue.Queue(maxsize=10)


def Producer():
    count = 0
    while True:
        q.put('bone %s' % count)
        print('produce bone %s' % count)
        count += 1
        time.sleep(0.1)


def Consumer(name):
    while True:
        print('[%s] eats bone [%s]' % (name, q.get()))
        time.sleep(1)


def main():
    p = threading.Thread(target=Producer)
    p.start()
    c1 = threading.Thread(target=Consumer, args=('Honda',))
    c2 = threading.Thread(target=Consumer, args=('Mini',))
    c1.start()
    c2.start()


if __name__ == '__main__':
    main()
