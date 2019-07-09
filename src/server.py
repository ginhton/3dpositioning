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

from utils import CatchRssi, CatchRssis, FilterWrap, KalmanFilter
from positioning import WCLSimple, WCLN, WCLWindow, TriangulatorN


# parameters
FILENAME = None
f = None


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





# framework
def socketRun(run):
    # socket
    s = socket.socket()
    host = '0.0.0.0'
    port = int(argv[1])

    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    s.bind((host, port))

    print(host, port)

    s.listen(5)

    c,addr = s.accept()
    print('addr ', addr)

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
    return


def main():

    if (len(argv) < 3):

        print('\tusage: ./server.py port mode\n\tmode = realtime, for positioning realtime.\n\tmode = rec, for record data into file\n')
        exit(0)

    mode = argv[2]

    if (mode == 'rec'):

        print('record rssi infos to files')
        openFile()
        socketRun(record)

    elif (mode == 'wrap'):

        wrap = FilterWrap()

        f = KalmanFilter()
        wrap.addfilter(f)

        x = TriangulatorN()
        # x = WCLSimple()
        x.add('d8:a0:1d:60:fe:c6', {"x":-3, "y":0})
        x.add('d8:a0:1d:61:04:de', {"x":0, "y":3})
        x.add('d8:a0:1d:61:04:66', {"x":3, "y":0})
        wrap.addpositioning(x)

        socketRun(wrap.update)

    elif (mode == 'triangulator'):

        x = TriangulatorN()
        x.add('d8:a0:1d:60:fe:c6', {"x":-3, "y":0})
        x.add('d8:a0:1d:61:04:de', {"x":0, "y":3})
        x.add('d8:a0:1d:61:04:66', {"x":3, "y":0})
        socketRun(x.update)

    elif (mode == 'WCLSimple'):

        # x = WCLSimple()
        # x = WCLN(number=2)
        x = WCLWindow()
        x.add('d8:a0:1d:60:fe:c6', {"x":-3, "y":0})
        x.add('d8:a0:1d:61:04:de', {"x":0, "y":3})
        x.add('d8:a0:1d:61:04:66', {"x":3, "y":0})
        socketRun(x.update)

    elif (mode == 'show'):

        socketRun(show)

    elif (mode == 'rssi'):

        adr = "d8:a0:1d:60:fe:c6"
        # c = CatchRssi(10, adr)
        c = CatchRssis(10)
        c.prepare()
        socketRun(c.run)

    else:

        print('\tusage: ./server.py port mode\n\tmode = realtime, for positioning realtime.\n\tmode = rec, for record data into file\n')


if __name__ == '__main__':

    main()
