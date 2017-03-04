#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import time


def run(n):
    print('task', n)
    time.sleep(2)
    print('task done', n, threading.current_thread())


start_time = time.time()
# 存放线程实例
t_objs = []
for i in range(50):
    t = threading.Thread(target=run, args=('t-%s' % i,))
    # 当前线程设置为守护线程
    t.setDaemon(True)
    t.start()
    t_objs.append(t)

# 等待全部线程完成
for t in t_objs:
    t.join()

print('------------all threads has finished.....', threading.current_thread(),
      threading.active_count())
print('cost time', time.time() - start_time)
