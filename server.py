#!/usr/bin/python
# -*- coding:utf-8 -*-
# socket server
# extract data from client and show

import socket
import sys
import json

interval = 10
MAX_DATA = 10
datas = [None]*MAX_DATA
cnt = 0

def extractData(data):
    return json.loads(data)


def position(data):
    datas[cnt] = data
    cnt = (cnt + 1) % MAX_DATA
    # get three point
    # 3-d positioning




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
        position(extractData(c.recv(1024)))
