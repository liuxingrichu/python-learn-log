#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import time


def run(n):
    semaphore.acquire()
    time.sleep(1)
    print("run the thread: %s\n" % n)
    semaphore.release()


if __name__ == '__main__':

    # 最多允许5个线程同时运行
    semaphore = threading.BoundedSemaphore(5)
    t_objs = list()
    for i in range(20):
        t = threading.Thread(target=run, args=(i,))
        t.start()
        t_objs.append(t)

    for t in t_objs:
        t.join()

    print('----all threads done---')
