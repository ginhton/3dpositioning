#!/usr/bin/python
# -*- coding: utf-8 -*-
# socket client
# generate fake rssi data timely

import socket
import sys
import time


def generateData():
    return b'{"addr":"00:11:22:33:FF:EE","rssi":-89}'


if __name__ == '__main__':
    s = socket.socket()

    host  = 'localhost'
    port = int(sys.argv[1])

    s.connect((host, port))
    while True:
        s.send(generateData())
        time.sleep(1)
    s.close()
