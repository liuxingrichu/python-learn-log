#!/usr/bin/env python
# -*- coding:utf-8 -*-

import multiprocessing
import threading
import time


def thread_run():
    print('threading number: ',threading.get_ident())


def run(name):
    time.sleep(2)
    print('hello', name)
    t = threading.Thread(target=thread_run)
    t.start()


if __name__ == '__main__':
    p_list = list()
    for i in range(10):
        p = multiprocessing.Process(target=run, args=('bob %s' % i,))
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()
