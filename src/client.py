#!/usr/bin/python
# -*- coding: utf-8 -*-
# socket client
# generate fake rssi data timely

import socket
import sys
import time
from json import loads

###############
# file list
#
#
#
# abnornal data: '2019-06-19_10:53:24_3m/2019-06-19 10:12:50.132391.txt'
##################3

f = None
# filename = '2019-06-07_11:05:09/2019-06-04 16:32:36.754252.txt'
# filename = '2019-06-10_20:52:37_00_00_03/2019-06-10 20:32:21.177455.txt'
filename = '../data/2019-06-19_10:55:14_5m/2019-06-19 10:31:43.975761.txt'
sleep_interval = 0.03

def openFile(filename):
    global f
    f = open(filename, 'r')


def generateFakeData():
    return b'{"addr":"00:11:22:33:FF:EE","rssi":-89}'

def generateData():
    return f.readline().strip('\n').encode('utf-8')


def show(data):
    # print(data)
    return

def run():
    loads(generateData())

def socketRun(run):
    s = socket.socket()

    host  = '127.0.0.1'
    port = int(sys.argv[1])

    try:
        s.connect((host, port))
        while True:
            # run()
            c = generateData()
            if c == b'':
                s.close()
                break
            s.send(c)
            time.sleep(sleep_interval)
    except socket.error:
        if s:
            s.close()


if __name__ == '__main__':
    openFile(filename)

    socketRun(show)
    # run()

