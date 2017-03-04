#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import time

"""
    锁内为线性执行
"""

def run():
    lock.acquire()
    global num
    num += 1
    # time.sleep(1)
    lock.release()


num = 0
lock = threading.Lock()
t_objs = []

for i in range(50):
    t = threading.Thread(target=run)
    t.start()
    t_objs.append(t)

for t in t_objs:
    t.join()

print('--------all threads has finished ....')
print('num:', num)
