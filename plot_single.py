#!/usr/bin/python3
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


if __name__ == '__main__':
    file = input('input file: ')
    with open(os.path.join('/home/joshuakt/Balance/jan2/', file), 'r') as f:
#    with open(os.path.join('/home/joshuakt/Balance/dec23/', file), 'r') as f:
#    with open(os.path.join('/home/joshuakt/Balance/Tracklets2/', file), 'r') as f:
#    with open(os.path.join('/home/joshuakt/Balance/test_reported', file), 'r') as f:

        data = json.load(f)
        desc = data['metadata']['description']

    for tracklet in data['data']:

        x = tracklet['x']
        y = tracklet['y']
        z = tracklet['z']
        t = tracklet['t']
        id = tracklet['id']
        v = [] 
        for i in range(0, len(x) - 1):
            d = ((y[i+1] - y[i])**2 + (x[i+1] - x[i])**2)**.5
            v.append(d)
        v.insert(0, v[0])

        fig ,axarr = plt.subplots(2, 3)
        plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
        axarr[0, 0].plot(x, y)
        axarr[0, 0].set(xlabel='x', ylabel='y', title='x-y positon over time')

        t = np.arange(len(x))
        plot1 = axarr[0, 1].scatter(x, y, c = t)
        axarr[0, 1].set(xlabel='x', ylabel='y', title='Scatter plot of x-y data over time (color chage proportional to time)')
        cbar = fig.colorbar(plot1, ax=axarr[0, 1])
        cbar.ax.set_ylabel('time')

        axarr[1, 0].plot(t, v)
        axarr[1, 0].set(xlabel='t', ylabel='v', title='velocity over time')

        axarr[1, 1].plot(t, y)
        axarr[1, 1].set(xlabel='t', ylabel='y', title='x over time')

        axarr[1, 2].plot(t, x)
        axarr[1, 2].set(xlabel='t', ylabel='x', title='y over time')

        axarr[0, 2].set(title=desc)

        # fig.suptitle('Balancing Test Data')

plt.show()
