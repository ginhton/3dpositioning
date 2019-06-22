#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process
from time import sleep
import math


A = 48.8
n = 1.5
start = 45
cross = 30
title='two algorithm (rssi => distance)'

def d1(txPower, rssi):
  if (rssi == 0):
    return -1.0; # if we cannot determine accuracy, return -1.

  ratio = rssi*1.0/txPower;
  if (ratio < 1.0):
    return math.pow(ratio,10);
  else:
    accuracy =  (0.89976)*math.pow(ratio,7.7095) + 0.111
    return accuracy

def d2(rssi):
    power = (abs(rssi)- A)/(10.0 * n)
    # print("  ", power)
    distance = math.pow(10, power)
    return distance


def test():
    # print(d1(A, 78))
    # print(d2(78))
  x = list(range(start, start + cross))
  dd1 = []
  dd2 = []
  for i in x:
    dd1.append(d1(A, i))
    dd2.append(d2(i))

  plt.plot(x,dd1,color='b', label='algo from github')
  plt.plot(x,dd2,color='r', label='algo from csdn')
  for i in range(cross):
    if x[i] % 5 == 0:
      plt.annotate("(%s)" % round(dd1[i], 2), xy=(x[i], dd1[i]))
      plt.annotate("(%s)" % round(dd2[i], 2), xy=(x[i], dd2[i] + 5))

  plt.xlabel("rssi/dbm")
  plt.ylabel("distance/m")
  plt.legend()
  plt.title('A=%s, n=%s, title=%s' % (A, n, title))
  plt.show()

if __name__ == '__main__':
    test()
