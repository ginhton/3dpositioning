#!/usr/bin/python
# -*- coding:utf-8 -*-
# data
# dealing with data
#
# ./statics.py folder_of_data

import math
import signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation
from sys import argv, exit
from json import loads, dump
from datetime import datetime
from os import listdir
from os.path import isfile, join, isdir
from scipy import stats
from utils import file2rssis

# parameters
# filename = './2019-06-07_11:12:03_66/2019-06-07 11:05:25.982751.txt'
# dirname = '2019-06-07_11:12:03_66'

# dirnames for experiment-2
# dirnames = [
#     '2019-06-07_11:12:03_66',
#     '2019-06-07_11:25:51_de',
#     '2019-06-07_11:28:13_c6'
# ]

# dirnames for experiment-2 extra experiment
# rssi of 1m distance
dirnames = [
    # '2019-06-07_19:58:24_66_de_c6_1mx3'
    '../data/expriment7'
]
f = None
L = []

def openFile(filename):
    global f, L
    f = None
    L = []
    if not f:
        f = open(filename, 'r')
    for line in f:
        # modify later, cuz there are 3-dit rssi
        # print(line)
        # print(line[39:42])
        rssi = int(line[39:42])
        L.append(rssi)

def draw(txt):
    fig = plt.figure()
    plt.hist(L, bins=50)
    fig.savefig(txt+".png")
    avg =  np.mean(L)
    mode = stats.mode(L)[0][0]
    s = txt+ " mean--> "+ str(avg)+ " mode--> "+ str(mode)
    print(s)
    plt.title(s)
    plt.show()


def getdirs(dirname):
    def joindirs(dirs):
        return join(dirname, dirs)

    dirnames = listdir(dirname)
    return map(joindirs, dirnames)


def main():
    if (len(argv) == 2):
        global dirnames
        # dirnames = [ argv[1] ]
        dirnames = getdirs('../data/experiment7')
    for dirname in dirnames:
        onlyfiles = [join(dirname, ff) for ff in listdir(dirname) if isfile(join(dirname, ff)) and ff.endswith(".txt") ]
        # print(onlyfiles)
        o = sorted(onlyfiles)
        for txt in o:
            openFile(txt)
            draw(txt)


def boxandwhisker(data):
    plt.style.use("ggplot")
    plt.rcParams['axes.unicode_minus'] = False
    # plt.rcParams['font.sans-serif']=['SimHei']

    df = pd.DataFrame()
    df['data'] = data['rssi']

    df.boxplot()
    plt.show()

def drawbox(path):
    data = file2rssis(path)
    if len(data['rssi']) > 0:
        print(data)
        boxandwhisker(data)

def convariance(data):
    return np.cov(data['rssi'])

    # return 'hi'

if __name__ == '__main__':
    # main()
    # drawbox("/home/i/my/temp/3dpositioning/data/2019-06-25_15:36:37_0.5m_8m/2019-06-24 09:33:10.109766.txt")
    # drawbox("/home/i/my/temp/3dpositioning/data/2019-06-25_15:36:37_0.5m_8m/2019-06-24 09:45:02.081323.txt")
    # p = "/home/i/my/temp/3dpositioning/data/2019-06-25_15:36:37_0.5m_8m/2019-06-24 09:45:02.081323.txt"
    # dir = "/home/i/my/temp/3dpositioning/data/2019-06-25_15:36:37_0.5m_8m/"
    # dir = "/home/i/my/temp/3dpositioning/data/2019-06-07_19:58:24_66_de_c6_1mx3"
    dir = "/home/i/my/temp/3dpositioning/data/2019-06-19_10:55:14_5m"

    for p in listdir(dir):
        print(convariance(file2rssis(join(dir, p))))
