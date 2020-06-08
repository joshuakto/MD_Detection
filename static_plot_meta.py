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
import helper.compute_ellipse as cell


if __name__ == '__main__':
    # exp = input('Process Experiment: ')
    exp = 'jan2'
    for _,_,i in os.walk(os.path.join('/home/joshuakt/Balance', exp)):
        for f in i:
            with open(os.path.join('/home/joshuakt/Balance/jan2/',f), 'r') as exp:
                data = json.load(exp)
            desc = data['metadata']['description']
                
            sample = 5.0
            distance_threshold = 1.0

            exp_type = ['walking']

            if all(typ in desc for typ in exp_type):

                for tracklet in data['data']:
                    x = tracklet['x']
                    y = tracklet['y']
                    z = tracklet['z']
                    t = tracklet['t']
                    id = tracklet['id']

                    xs, ys, ts, idxs = static.extract_static_data(x, y, t, sample, distance_threshold)
                    near_point_count = static.n_near_pts(x, y, sample, distance_threshold)

                    for i in range(len(xs)):
                        fig ,axarr = plt.subplots(3, 3)
                        fig.suptitle(f'static phase{i}')

                        plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
                        axarr[1, 0].plot(xs[i], ys[i], 'r')
                        axarr[1, 0].set(xlabel='x', ylabel='y', title='x-y positon over time')

                        plot1 = axarr[0, 0].scatter(xs[i], ys[i], c = ts[i])
                        axarr[0, 0].set(xlabel='x', ylabel='y')
                        cbar = fig.colorbar(plot1, ax=axarr[0, 0])
                        cbar.ax.set_ylabel('time')

                        axarr[0, 2].plot(ts[i], near_point_count[idxs[i][0]:idxs[i][1]])
                        axarr[0, 2].set(xlabel='t', ylabel='# near points', title= '# points near xt over time'+' '+ str(sample)+ ' '+ str(distance_threshold))

                        axarr[2, 0].set(xlabel = f,title=desc)
                        axarr[2, 0].plot(x, y, 'b')
                        axarr[2, 0].plot(xs[i], ys[i], 'r')

                        # find ellipse and plot
                        (sx, sy) = feat.calibrate_center(xs[i], ys[i])
                        axarr[0, 1].scatter(sx, sy, c = ts[i])
                        pri_ax, sec_ax = cell.extract_axes(sx, sy)
                        axarr[0, 1].plot([0, pri_ax[0]], [0, pri_ax[1]], 'r')
                        axarr[0, 1].plot([0, sec_ax[0]], [0, sec_ax[1]], 'b')
                        e = cell.best_fit_ellipse(sx, sy)
                        axarr[0, 1].add_patch(e)
                        e_area = cell.area(sx, sy)
                        axarr[0, 1].set(xlabel=f'area of ellipse: {e_area}', ylabel='y')
                        axarr[0, 1].set_ylim(-.6, .6)
                        axarr[0, 1].set_xlim(-.6, .6)

                        axarr[1, 2].plot(ts[i], ys[i], 'r')
                        axarr[1, 2].set(xlabel='t', ylabel='y', title='y over time')

                        axarr[1, 1].plot(ts[i], xs[i], 'r')
                        axarr[1, 1].set(xlabel='t', ylabel='x', title='x over time')

                        axarr[2, 1].plot(t, x, 'b')
                        axarr[2, 1].plot(ts[i], xs[i], 'r')
                        axarr[2, 1].set(xlabel='t', ylabel='x', title='x over time highlighted in red is displayed above')
                   
                        axarr[2, 2].plot(t, y, 'b')
                        axarr[2, 2].plot(ts[i], ys[i], 'r')
                        axarr[2, 2].set(xlabel='t', ylabel='y', title='y over time')

                        static.find_static_phases(x, y, static_min_len=55)

    plt.show()


