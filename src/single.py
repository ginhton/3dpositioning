import matplotlib.pyplot as plt
import numpy as np

from utils import DrawSingle, KalmanFilter, socketRun, GetDistance, TaskQueue


def main():

    task_queue = TaskQueue()

    df = KalmanFilter()
    dd = GetDistance()
    dw = DrawSingle(ylim_min=0, ylim_max=10, key='distance')

    task_queue.append(df)
    task_queue.append(dd)
    task_queue.append(dw)

    socketRun(task_queue.update, port=8070)


if __name__ == '__main__':

    main()
