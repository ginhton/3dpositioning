#!/usr/bin/python
# -*- coding:utf-8 -*-
# data
# dealing with data
#
# ./statics.py folder_of_data

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

from sys import argv, exit
from datetime import datetime
from os import listdir
from os.path import isfile, join, isdir

from utils import file2rssis


class AnalyzeRssi:

    def __init__(self):

        self._cache = None


    def analyze_file(self, filename):

        if (isfile(filename) and filename.endswith(".txt")):

            self._cache = file2rssis(filename)['rssi']
            self._draw(filename)


    def analyze_directory(self, directory):

        if isdir(directory):

            onlyfiles = [join(directory, filename) for filename in listdir(directory) if isfile(join(directory, filename)) and filename.endswith(".txt")]
            sorted_files = sorted(onlyfiles)

            for filename in sorted_files:

                self.analyze_file(filename)


    def analyze_experiment(self, directory):

        if isdir(directory):

            for item in listdir(directory):

                joined_direcory = join(directory, item)
                self.analyze_directory(joined_direcory)


    def _draw(self, filename, save=False):

        avg = round(np.mean(self._cache),2)
        mode = round(stats.mode(self._cache)[0][0], 2)
        cov = round(self._convariance(self._cache), 2)
        title = '-'.join(map(str, [filename, avg, mode, cov]))

        print('filename-mean-mode-cov')
        print(title)

        fig = plt.figure()
        plt.hist(self._cache, bins=50)
        plt.title(title)
        plt.show()

        if save:

            fig.savefig(title+".png")


    def _convariance(self, data):

        return np.cov(data)



def main():

    _x = AnalyzeRssi()
    _x.analyze_experiment('../data/experiment7')


def box_and_whisker(data):

    plt.style.use("ggplot")
    plt.rcParams['axes.unicode_minus'] = False

    df = pd.DataFrame()
    df['data'] = data['rssi']

    df.boxplot()
    plt.show()


def draw_box(filename):

    data = file2rssis(filename)

    if len(data['rssi']) > 0:

        box_and_whisker(data)


if __name__ == '__main__':

    main()

