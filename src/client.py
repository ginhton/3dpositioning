#!/usr/bin/python
# -*- coding: utf-8 -*-
# socket client
# generate fake rssi data timely

import socket
import sys
import time
from json import loads


f = None

# receive rssi from three addresses
filename = '../data/experiment1/2019-06-07_11:05:09/2019-06-07 11:01:23.517382.txt'

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

