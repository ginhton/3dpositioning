#!/usr/bin/python
# -*- coding: utf-8 -*-
# socket client
# generate fake rssi data timely

import socket
import sys
import time
from json import loads


f = None
filename = '2019-06-04 16:32:36.754252.txt'
sleep_interval = 0.1

def openFile(filename):
    global f
    f = open(filename, 'r')


def generateFakeData():
    return b'{"addr":"00:11:22:33:FF:EE","rssi":-89}'

def generateData():
    # return bytearray(f.readline().strip('\n'), 'utf-8')
    return f.readline().strip('\n').encode('utf-8')


def show(data):
    # print(data)
    return

def run():
    loads(generateData())

def socketRun(run):
    s = socket.socket()

    host  = 'localhost'
    port = int(sys.argv[1])

    s.connect((host, port))
    while True:
        # run()
        s.send(generateData())
        time.sleep(sleep_interval)
    s.close()


if __name__ == '__main__':
    openFile(filename)

    socketRun(show)
    # run()

