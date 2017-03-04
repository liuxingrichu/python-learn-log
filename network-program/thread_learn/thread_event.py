#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import time
import random

event = threading.Event()


def light():
    if not event.isSet():
        event.set()
    count = 0
    while True:
        if count < 10:
            print('\033[42;1m---green light on-----\033[0m')
        elif count < 13:
            print('\033[43;1m---yellow light on ---\033[0m')
        elif count < 20:
            if event.isSet():
                event.clear()
            print('\033[41;1m---red light on-------\033[0m')
        else:
            count = 0
            event.set()
        time.sleep(1)
        count += 1


def car(name):
    while True:
        if event.is_set():
            print('car {} is running'.format(name))
            time.sleep(random.randrange(5))
        else:
            print('car [%s] is waiting for the green light' % name)
            event.wait()
            print('green light is on. car [%s] can run....' % name)


def main():
    Light = threading.Thread(target=light)
    Light.start()

    for i in range(3):
        t = threading.Thread(target=car, args=(i,))
        t.start()


if __name__ == '__main__':
    main()
