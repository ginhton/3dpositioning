#!/usr/bin/python
# -*- coding:utf-8 -*-
# 3 point positioning algorithm
#
# ./p3algo.py

import socket
import math
import signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sys import argv, exit
from json import loads

from utils import CatchRssi, rssi2DistanceCSDN, rssi2DistanceGithub, rssiFilter

p0_x = 3
p0_y = 0
p1_x = 0
p1_y = 3
p2_x = -3
p2_y = 0


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

def main():
    d0 = 0.86
    d1 = 3
    d2 = 3
    for i in range(20):
        d0 = d0 + 0.10
        [x, y] = threeDAlgo(d0, d1, d2)
        print('d0 is %s, (x,y ) is (%s, %s)' % (d0, x, y))

if __name__ == '__main__':
    main()
