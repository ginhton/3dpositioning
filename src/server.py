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

from utils import CatchRssi, CatchRssis, KalmanFilter, AddrChecker, TaskQueue
from positioning import WCLSimple, WCLN, WCLWindow, TriangulatorN


# parameters
FILENAME = None
f = None


# data processing
def extractData(data):

    json_obj = None

    try:

        json_obj = loads(data)

        if not json_obj.__contains__("addr"):

            return None

        if not json_obj.__contains__("rssi"):

            return None

        json_obj['rssi'] = int(json_obj['rssi'])

    except ValueError:

        return None

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

                json_obj = extractData(item)

                if json_obj == None:

                    continue

                run(json_obj)

        except KeyboardInterrupt:

                try:

                    if c:
                        c.close()

                    s.close()
                    exit(0)

                except: pass

                break


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

    elif (mode == 'task'):

        task_queue = TaskQueue()
        addr_checker = AddrChecker(KalmanFilter)

        task_queue.append(addr_checker)

        pos = TriangulatorN()
        # pos = WCLSimple()
        pos.add('d8:a0:1d:60:fe:c6', {"x":-3, "y":0})
        pos.add('d8:a0:1d:61:04:de', {"x":0, "y":3})
        pos.add('d8:a0:1d:61:04:66', {"x":3, "y":0})

        task_queue.append(pos)

        socketRun(task_queue.update)

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

    elif (mode == 'test'):

        kalman_filter = KalmanFilter()
        values = []

        def test_kalman_filter(data):

            rssi = int(data['rssi'])
            val = kalman_filter.update(rssi)
            values.append(val)
            # print(len(values))
            print(val)

            # if (len(values) >= 40):

            #     values = values[1:]

            plt.plot(values, color='r')
            plt.pause(0.05)

        plt.show()

        socketRun(test_kalman_filter)


    else:

        print('\tusage: ./server.py port mode\n\tmode = realtime, for positioning realtime.\n\tmode = rec, for record data into file\n')


if __name__ == '__main__':

    main()
