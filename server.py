#!/usr/bin/python
# -*- coding:utf-8 -*-
# socket server
# extract data from client and show
#
# ./server.py PORT mode

import socket
import math
from sys import argv, exit
from json import loads
from datetime import datetime

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
    try:
        json_obj = loads(data)
    except ValueError:
        return {"error":data}
    return json_obj


def dataCmp(a, b):
    return a['rrsi ']/ a['len'] > b['rssi'] / b['len']


def rssi2Distance(rssi):
    power = (math.abs(rssi)- 60)/(10.0 * 3.3)
    distance = math.pow(10, power)
    return distance


# https://blog.csdn.net/qq_35651984/article/details/82633843
def threeDAlgo(d0, d1, d2):
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


def positioning(data):
    found = 0

    global cnt
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

    if (cnt > 20 and len(datas) >= 3):
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
        print(threeDAlgo(d0, d1, d2))

        # clear all data
        datas = []
def generateFileName():
    return str(datetime.now())+".txt"

def openFile():
    global f
    if f == None:
        f = open(generateFileName(), 'w')


def record(data):
    print(data)
    f.write(str(data)+'\n')


def closeFile():
    if f != None:
        f.close()


def extractjson(data):
    if (len(data) < 50):
        return [data]
    else:
        return data.decode('utf-8').replace('}{','}#{').split('#')



def socketRun(run):
    # socket
    s = socket.socket()
    host = '0.0.0.0'
    port = int(argv[1])
    s.bind((host, port))

    print(host, port)

    s.listen(5)

    c,addr = s.accept()
    print('addr ', addr)

    while True:
        data = c.recv(1024)
        collections = extractjson(data)

        for item in collections:
            run(extractData(item))




if __name__ == '__main__':

    if (len(argv) < 3):
        print('\tusage: ./server.py port mode\n\tmode = realtime, for positioning realtime.\n\tmode = rec, for record data into file\n')
        exit(0)

    # file
    mode = argv[2]


    if (mode == 'rec'):
        print('record rssi infos to files')
        openFile()
        socketRun(record)
    elif (mode == 'realtime'):
        socketRun(positioning)
    else:
        print('\tusage: ./server.py port mode\n\tmode = realtime, for positioning realtime.\n\tmode = rec, for record data into file\n')

