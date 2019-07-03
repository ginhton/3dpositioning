import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque
import math

A = 48.8
n = 1.56
txPower = A


# 滑动防脉冲干扰平均滤波法
class rssiFilterIMA:
    def __init__(self, window=10):
        self.chIsFull = False
        self.chIx = 0
        self.achBuf = [None]*window
        self.window = window

    def check(self, rssi):
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
    def __init__(self, window=10, addr=''):
        self.cache = []
        self.cnt = 0
        self.window = window
        self.addr = addr
        self.rssis = []
        self.line = None

        self.prev = None
        self.threshold = 10
        self.rfilter = None

    def prepare(self):
        self.rfilter = rssiFilterIMA(self.window)
        self.preparePlot()

    def preparePlot(self):
        self.rssis = deque([0]*100)
        # ax = plt.axes(xlim=(0, 20), ylim=(0, 10))

        self.line, = plt.plot(self.rssis)
        plt.ion()
        plt.ylim([-90,-30])
        plt.show()

    def run(self, data):
        # if data['addr'] != self.addr:
        #     print('addr %s not match' % data['addr'])
        #     return

        self.cnt = self.cnt + 1
        rssi = int(data['rssi'])
        avg = self.rfilter.check(rssi)
        self.drawRssi(avg)
        # if self.cnt >= self.window:
        #     avg = sum(self.cache) / len(self.cache)
        #     self.prev = avg

        #     self.cache = []
        #     self.cnt = 0

        #     self.drawRssi(avg)

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
        # avg = self.rfilter.check(rssi)
        # avg = self.rfilter.check(rssi)
        self.cache[addr]['rssi'] = self.cache[addr]['rssi'][1:] + [rssi]
        self.cache[addr]['plot'].set_ydata(self.cache[addr]['rssi'])
        self.ax.draw_artist(self.cache[addr]['plot'])
        self.draw()

    # draw average rssi
    def draw(self):
        # self.cache[addr]['plot'].set_ydata(self.cache[addr]['rssi'])
        # self.ax.draw_artist(self.cache[addr]['plot'])
        self.ax.figure.canvas.draw()
        # plt.draw()
        # time.sleep(0.01)
        plt.pause(0.0001)
