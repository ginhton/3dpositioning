import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque
import math
from json import loads
from os.path import isfile

A = 48.8
n = 1.56
txPower = A

# output {"addr":"xxxx", "rssi":[-52, -53, ...]}
def file2rssis(path):

    abfilter = AbnormalValFilter(threshold = 25)
    result = {"addr":"xxxx", "rssi":[]}

    if not isfile(path):

        return result

    f = open(path, 'r')
    line = f.readline()

    if line == '':

        return result

    result['addr'] = eval(line)['addr']
    result['rssi'].append(int(eval(line)['rssi']))
    abfilter.update(int(eval(line)['rssi']))

    for line in f:

        rssi = int(eval(line)['rssi'])
        filtered_rssi = abfilter.update(rssi)

        if (filtered_rssi != None):

            result['rssi'].append(filtered_rssi)

    return result


def parseJSON(data):

    try:

        print(data)
        json_obj = loads(data)

    except ValueError:

        return {"error":data}

    return json_obj



class AddrChecker:

    def __init__(self, handler):

        self.cache = {}
        self.handler = handler

    def update(self, json_obj):

        addr = json_obj['addr']
        rssi = json_obj['rssi']

        if addr not in self.cache:

            self.cache[addr] = self.handler()

        rssi  = self.cache[addr].update(rssi)

        if rssi == None:

            return None

        json_obj['rssi'] = rssi

        print(json_obj)

        return json_obj



# a task has a update method
# it read a json_obj, and generate a json_obj or None
class TaskQueue:

    def __init__(self):

        self.queue = []

    def append(self, task):

        self.queue.append(task)


    def update(self, json_obj):

        if len(self.queue) == 0:

            return None

        ret_json_obj = json_obj

        for task in self.queue:

            ret_json_obj = task.update(ret_json_obj)

            if ret_json_obj == None:

                break

        return ret_json_obj



class FilterWrap:

    def __init__(self):

        self.filter = None
        self.positioning = None

    def addfilter(self, filter):

        self.filter = filter

    def addpositioning(self, positioning):

        self.positioning = positioning

    def update(self, data):

        rssi = int(data['rssi'])
        rssi = self.filter.update(rssi)

        if rssi == None:

            return None

        data['rssi'] = rssi

        return self.positioning.update(data)


class FilterChain:

    def __init__(self):

        self.chain = []

    def add(f):

        self.chain.append(f)

    def clear():

        self.chain = []

    def update(data):

        if len(self.chain) < 1:

            print('no filter')
            return None

        for f in self.chain():

            if hasattr(f, 'update'):

                data = f.update(data)

        return data


class AbnormalValFilter:

    def __init__(self, prev=None, threshold=30):

        self.prev = prev
        self.threshold = threshold

    def update(self, rssi):

        if rssi == None:

            return None

        if (self.prev == None):

            self.prev = rssi
            return rssi

        else:

            if abs(rssi - self.prev) >= self.threshold:

                print('abnormal rssi %d' % rssi)
                return self.prev

            else:

                self.prev = rssi
                return rssi


class KalmanFilter:

    # p = 7.8, or 21, or 39
    def __init__(self, init_x=None, init_p=7.8, r=0.1**2, q=1e-5):

        self.x = init_x
        self.p = init_p
        self.r = r # estimate of measure convariance
        self.q = q # process convariance

    def update(self, rssi):

        if rssi == None:

            return None

        if self.x == None:

            self.x = rssi
            return

        result = self.x
        self.p = self.p + self.q

        k = self.p / (self.p + self.r)
        self.x = result + k*(rssi - result)
        self.p = (1-k)*self.p

        return result

# 滑动防脉冲干扰平均滤波法
class RssiFilterIMA:

    def __init__(self, window=10):

        self.chIsFull = False
        self.chIx = 0
        self.achBuf = [None]*window
        self.window = window

    def update(self, rssi):

        if rssi == None:

            return None

        self.achBuf[self.chIx] = rssi
        self.chIx = self.chIx + 1
        if (self.chIx >= self.window):

            self.chIx = 0
            self.chIsFull = True

        if not self.chIsFull:

            nSum = 0

            for nCnt in range(self.chIx):

                nSum += self.achBuf[nCnt]

            return nSum / self.chIx

        chMaxVal = -140
        chMinVal = 0
        nSum = 0

        for nCnt in range(self.window):

            chTemp = self.achBuf[nCnt]
            nSum += chTemp

            if chTemp > chMaxVal:

                chMaxVal = chTemp

            elif chTemp < chMinVal:

                chMinVal = chTemp

        nSum = nSum - (chMaxVal + chMinVal)
        nSum = nSum / (self.window - 2)

        return nSum


def rssi2DistanceGithub(rssi):

    txPower = 48.8

    if (rssi == 0):

        return -1.0 # if we cannot determine accuracy, return -1.

    ratio = rssi*1.0/txPower

    if (ratio < 1.0):

        return math.pow(ratio,10)

    else:

        accuracy = (0.89976)*math.pow(ratio,7.7095) + 0.111
        return accuracy


def rssi2DistanceCSDN(rssi):

    A = 48.8
    n = 15.6

    power = (abs(rssi)- A)/(10.0 * n)
    distance = math.pow(10, power)

    return distance


class CatchRssi:

    def __init__(self, window=10, addr=None):

        self.cache = []
        self.cnt = 0
        self.window = window
        self.addr = addr
        self.rssis = []
        self.line = None

        self.threshold = 10
        self.rfilter = None

    def prepare(self):

        self.rfilter = rssiFilterIMA(self.window)
        self.preparePlot()

    def preparePlot(self):

        self.rssis = deque([0]*100)
        self.line, = plt.plot(self.rssis)
        plt.ion()
        plt.ylim([-90,-30])
        plt.show()

    def run(self, data):
        if self.addr != None and data['addr'] != self.addr:
            print('addr %s not match' % data['addr'])
            return

        self.cnt = self.cnt + 1
        rssi = int(data['rssi'])
        avg = self.rfilter.update(rssi)
        self.drawRssi(avg)

    # draw average rssi
    def drawRssi(self, avg):

        self.rssis.appendleft(avg)
        datatoplot = self.rssis.pop()
        self.line.set_ydata(self.rssis)
        plt.draw()
        # time.sleep(0.01)
        plt.pause(0.0001)

    # draw distance
    def drawD(self, avg):

        d = rssi2DistanceCSDN(avg)
        plt.ylim([-100,100])

        self.rssis.appendleft(d)
        datatoplot = self.rssis.pop()
        self.line.set_ydata(self.rssis)
        plt.draw()
        # time.sleep(0.01)
        plt.pause(0.0001)


class CatchRssis:

    def __init__(self, window=10):

        self.cache = {}

        self.fig = None
        self.ax = None

        self.window = window
        self.rfilter = None

        self.POINTS = 60

    def prepare(self):

        self.rfilter = rssiFilterIMA(self.window)
        self.preparePlot()

    def preparePlot(self):

        self.fig, self.ax = plt.subplots()
        plt.ion()
        self.ax.set_ylim([-90,-30])
        plt.show()

    def run(self, data):

        if not 'addr' in data:

            print('corrputed data')
            return

        addr = data['addr']

        if not addr in self.cache:

            self.cache[addr] = {}
            self.cache[addr]['rssi'] = [0] * self.POINTS
            self.cache[addr]['plot'], = self.ax.plot(range(self.POINTS), self.cache[addr]['rssi'], label= '%s' % addr[-2:])
            self.ax.figure.canvas.draw()

        rssi = int(data['rssi'])
        # avg = self.rfilter.update(rssi)
        self.cache[addr]['rssi'] = self.cache[addr]['rssi'][1:] + [rssi]
        self.cache[addr]['plot'].set_ydata(self.cache[addr]['rssi'])
        self.ax.draw_artist(self.cache[addr]['plot'])
        self.draw()

    # draw average rssi
    def draw(self):

        self.ax.figure.canvas.draw()
        plt.pause(0.0001)


## end of file
