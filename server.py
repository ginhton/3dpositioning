#!/usr/bin/python
# -*- coding:utf-8 -*-
# socket server
# extract data from client and show

import socket
import sys


def extractData(data):
    return data[9:26], data[35:38]


if __name__ == '__main__':
    s = socket.socket()
    host = '0.0.0.0'
    port = int(sys.argv[1])
    s.bind((host, port))

    print(host, port)

    s.listen(5)

    c,addr = s.accept();
    print('addr ', addr);

    while True:
        print(extractData(c.recv(1024)))
