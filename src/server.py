#!/usr/bin/python
# -*- coding:utf-8 -*-
# socket server
# extract data from client and show
#
# ./server.py PORT mode

import socket
import math
import signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sys import argv, exit
from json import loads
from datetime import datetime
from multiprocessing import Process, Manager

from utils import CatchRssi, rssi2DistanceCSDN, rssi2DistanceGithub, rssiFilter


# parameters
interval = 20
MAX_DATA = 10
FILENAME = None
FILTER_ON = True
FILTER_THRESHOLD = 30
rfilter = None

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
coords = {}
addr1 = "d8:a0:1d:61:04:de"
addr2 = "d8:a0:1d:60:fe:c6"
addr3 = "d8:a0:1d:61:04:66"
s = None

A = 48.8
n = 1.5
txPower = A

# position coordinate
PX = None
PY = None
d = None

# init functions
def initCoords():
    coords[addr1] = {"x":0,"y":3}
    coords[addr2] = {"x":-3,"y":0}
    coords[addr3] = {"x":3,"y":0}
    PX = 0
    PY = 0

# data processing
def extractData(data):
    try:
        json_obj = loads(data)
    except ValueError:
        return {"error":data}
    return json_obj

def extractjson(data):
    if (len(data) < 50):
        return [data]
    else:
        return data.decode('utf-8').replace('}{','}#{').split('#')


# file processing
def generateFileName():
    return str(datetime.now())+".txt"

def openFile():
    global FILENAME
    global f
    if f == None:
        FILENAME=generateFileName()
        f = open(FILENAME, 'w')

def record(data):
    print(data)
    f.write(str(data)+'\n')

def closeFile():
    if f != None:
        f.close()


# computing
def dataCmp(a, b):
    return a['rrsi ']/ a['len'] > b['rssi'] / b['len']

def updateCoordinate(a0, a1, a2):
    global p0_x, p0_y, p1_x, p1_y, p2_x, p2_y
    p0_x = coords[a0]['x']
    p0_y = coords[a0]['y']
    p1_x = coords[a1]['x']
    p1_y = coords[a1]['y']
    p2_x = coords[a2]['x']
    p2_y = coords[a2]['y']
    return

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


def positioning(data):
    global cnt
    global datas
    global PX, PY

    found = 0
    cnt = cnt + 1

    data['rssi'] = int(data['rssi'])

    for item in datas:
        if item['addr'] == data['addr']:
            found = 1
            item['rssi']= item['rssi']+ data['rssi']
            item['len'] = item['len'] + 1
            break

    if found == 0:
        data['len'] = 1
        datas.append(data)

    if (cnt > interval and len(datas) >= 3):
        cnt = 0

        # get three point
        # sorted(datas, key=functools.cmp_to_key(dataCmp))
        sorted(datas, key=lambda x:x['rssi']/x['len'], reverse=True)

        rssi0 = datas[0]['rssi'] / datas[0]['len']
        rssi1 = datas[1]['rssi'] / datas[1]['len']
        rssi2 = datas[2]['rssi'] / datas[2]['len']

        # get distance
        d0 = rssi2DistanceCSDN(rssi0)
        d1 = rssi2DistanceCSDN(rssi1)
        d2 = rssi2DistanceCSDN(rssi2)

        print('distance : %s %s %s' % (d0 , d1, d2))

        # get coordinate
        updateCoordinate(datas[0]['addr'], datas[1]['addr'], datas[2]['addr'])

        # 3-d positioning
        PX, PY = threeDAlgo(d0, d1, d2)
        d['x'] = PX
        d['y'] = PY
        print(PX, PY)

        # clear all data
        datas = []


# framework
def socketRun(run):
    # socket
    global s
    s = socket.socket()
    host = '0.0.0.0'
    port = int(argv[1])

    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    s.bind((host, port))

    print(host, port)

    s.listen(5)

    c,addr = s.accept()
    print('addr ', addr)

    # if FILTER_ON:
    #     rfilter = rssiFilter(FILTER_THRESHOLD)

    while True:
        try:
            data = c.recv(1024)

            collections = extractjson(data)

            for item in collections:
                tmp = extractData(item)
                if not tmp.__contains__("addr"):
                    continue
                if not tmp.__contains__("rssi"):
                    continue
                # if FILTER_ON:
                    # rfilter.check(int(data["rssi"]))

                run(tmp)

        except KeyboardInterrupt:
                try:
                    if c:
                        c.close()
                    s.close()
                    exit(0)
                except: pass
                break

# draw graph
def draw(d):
    fig, ax = plt.subplots()
    ax.set_xlim([-6,6])
    ax.set_ylim([-6,6])

    dot, = ax.plot([], [], 'o', color='red')

    def dots(i):
        print(d)
        dot.set_data(d["x"], d["y"])

    ani = animation.FuncAnimation(fig, dots, interval=500, repeat=False)
    plt.grid()
    plt.grid(color='b', linewidth='0.5', linestyle='--')

    # ani.save(FILENAME+'.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


def show(data):
    print(data)
    # print('.')
    return


def main():
    global d

    if (len(argv) < 3):
        print('\tusage: ./server.py port mode\n\tmode = realtime, for positioning realtime.\n\tmode = rec, for record data into file\n')
        exit(0)

    mode = argv[2]

    if (mode == 'rec'):
        print('record rssi infos to files')
        openFile()
        socketRun(record)
    elif (mode == 'realtime'):
        initCoords()
        manager = Manager()
        d = manager.dict()
        d["x"] = 0
        d["y"] = 0
        p = Process(target=draw, args=(d,))
        p.start()
        # draw()
        socketRun(positioning)
        # socketRun(show)
        p.join()
    elif (mode == 'show'):
        socketRun(show)
    elif (mode == 'rssi'):
        adr = "d8:a0:1d:60:fe:c6"
        c = CatchRssi(10, adr)
        c.prepare()
        socketRun(c.run)
    else:
        print('\tusage: ./server.py port mode\n\tmode = realtime, for positioning realtime.\n\tmode = rec, for record data into file\n')



if __name__ == '__main__':
    main()
