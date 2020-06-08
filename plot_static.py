#!/usr/bin/python3
import json
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits import mplot3d
import helper.extract_feats as feat
import helper.extract_static as static

if __name__ == '__main__':

    # experiemnt for 4 postions:
    f = '1904186b-a659-4f77-841f-b781dd910396.ustracklets.1546553953416.json'
    # f = 'f617a98a-195a-48bf-9e00-16050501709d.ustracklets.1546553952626.json'
    # walking experiment:
    # f = '518df718-06fb-4512-8cc3-c14066fd73a8.ustracklets.1546553952258.json'
    # f = 'cb1895f4-0ef7-4b74-b6f3-14f97414fe18.ustracklets.1546553951350.json'
    with open(os.path.join('/home/joshuakt/Balance/jan2/',f), 'r') as exp:
        data = json.load(exp)
        desc = data['metadata']['description']
        
    sample = 5.0
    distance_threshold = 1.0

    for tracklet in data['data']:
        x = tracklet['x']
        y = tracklet['y']
        z = tracklet['z']
        t = tracklet['t']
        id = tracklet['id']

        xs, ys, ts, idxs = static.extract_static_data(x, y, t, sample, distance_threshold)
        near_point_count = static.n_near_pts(x, y, sample, distance_threshold)

        for i in range(len(xs)):

            fig ,axarr = plt.subplots(2, 3)
            fig.suptitle(f'static phase{i}')

            plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
            axarr[0, 0].plot(xs[i], ys[i])
            axarr[0, 0].set(xlabel='x', ylabel='y', title='x-y positon over time')

            t = np.arange(len(x))
            plot1 = axarr[0, 1].scatter(xs[i], ys[i], c = ts[i])
            axarr[0, 1].set(xlabel='x', ylabel='y')
            cbar = fig.colorbar(plot1, ax=axarr[0, 1])
            cbar.ax.set_ylabel('time')

            axarr[0, 2].plot(ts[i], near_point_count[idxs[i][0]:idxs[i][1]])
            axarr[0, 2].set(xlabel='t', ylabel='# near points', title= '# points near xt over time'+' '+ str(sample)+ ' '+ str(distance_threshold))

            axarr[1, 0].set(xlabel = f,title=desc)
            axarr[1, 0].plot(x, y, 'b')
            axarr[1, 0].plot(xs[i], ys[i], 'r')

            axarr[1, 1].plot(ts[i], xs[i])
            axarr[1, 1].set(xlabel='t', ylabel='x', title='x over time')

            axarr[1, 2].plot(ts[i], ys[i])
            axarr[1, 2].set(xlabel='t', ylabel='y', title='y over time')
       
            static.find_static_phases(x, y, static_min_len=55)

    plt.show()


