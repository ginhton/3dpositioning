#!/usr/bin/python
# -*- coding:utf-8 -*-
# socket server
# extract data from client and show

import socket
import sys
import json
import math

# parameters
interval = 10
MAX_DATA = 10
FILENAME = 'record.txt'

# cord
p0_x=0
p0_y=0
p1_x=1
p1_y=2
p2_x=2
p2_y=1


# global variables
datas = []
cnt = 0
f = None



def extractData(data):
    return json.loads(data)


def dataCmp(a, b):
    return a.rrsi / a['len'] > b['rssi'] / b['len']


def rssi2Distance(rssi):
    power = (math.abs(rssi)- 60)/(10.0 * 3.3)
    distance = math.pow(10, power)
    return distance


# https://blog.csdn.net/qq_35651984/article/details/82633843
def 3dAlgo(d0, d1, d2):
    a = p0_x-p2_x
    b = p0_y-p2_y
    c = math.pow(p0_x, 2) - math.pow(p2_x, 2) + math.pow(p0_y, 2) - math.pow(p2_y, 2) + math.pow(d2, 2) - math.pow(d0, 2)
    d = p1_x-p2_x
    e = p1_y-p2_y
    f = math.pow(p1_x, 2) - math.pow(p2_x, 2) + math.pow(p1_y, 2) - math.pow(p2_y, 2) + math.pow(d2, 2) - math.pow(d1, 2)
    x = (b*f-e*c)/(2*b*d-2*a*e)
    y = (a*f-d*c)/(2*a*e-2*b*d)
    return x, y

def updateCoordinate():
    return


def position(data):
    found = 0

    cnt = cnt + 1
    for item in datas:
        if item.addr == data.addr:
            found = 1
            item['rssi ']= item['rssi ']+ data['rssi']
            item['len'] = item['len'] + 1
            break

    if found == 0:
        data['len'] = 1
        datas.append(data)

    if (cnt > 20 && len(datas) >= 3):
        cnt = 0

        # get three point
        # sorted(datas, key=functools.cmp_to_key(dataCmp))
        sorted(datas, key=lambda x:x['rssi']/x['len'], reverse=True)

        rssi0 = datas[0]['rssi'] / datas[0]['len']
        rssi1 = datas[1]['rssi'] / datas[1]['len']
        rssi2 = datas[2]['rssi'] / datas[2]['len']

        # get distance
        d0 = rssi2Distance(rssi0)
        d1 = rssi2Distance(rssi1)
        d2 = rssi2Distance(rssi2)

        # get coordinate
        updateCoordinate()

        # 3-d positioning
        print(3dAlgo(d0, d1, d2))


def openFile():
    if f == None:
        f = open(FILENAME, 'w')


def record(data):
    print('record rssi infos to files')
    f.write(data)


def closeFile():
    if f != None:
        f.close()



if __name__ == '__main__':
    s = socket.socket()
    host = '0.0.0.0'
    port = int(sys.argv[1])
    s.bind((host, port))

    print(host, port)

    s.listen(5)

    c,addr = s.accept()
    print('addr ', addr)

    while True:
        position(extractData(c.recv(1024)))
