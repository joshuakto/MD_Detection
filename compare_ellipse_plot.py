#!/usr/bin/python3
import math
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import helper.extract_feats as feat
import helper.compute_ellipse as cell

if __name__ == '__main__':

    nrow = 2
    ncol = 3
    fig ,axarr = plt.subplots(nrow, ncol)
    count = 0
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)

    # exps = [i for _,_,i in os.walk('/home/joshuakt/Balance/dec23')]
    exps = [i for _,_,i in os.walk('/home/joshuakt/Balance/jan2')]
    exps = exps[0]
    # num = 0
    # num2 = 0
    for f in exps:
        if count < nrow * ncol:
            # with open(os.path.join('/home/joshuakt/Balance/dec23/',f), 'r') as exp:
            with open(os.path.join('/home/joshuakt/Balance/jan2/',f), 'r') as exp:
                data = json.load(exp)
                desc = data['metadata']['description']
                # description_rec = open('/home/joshuakt/Balance/descs.txt','a')
                # description_rec.write(desc+'\n')
                # if 'facing device' in desc:
                #     for tracklet in data['data']:
                #         t = tracklet['t']
                #         if len(t) > 0:
                #             print('True')
                #             print(len(t))
                #             num2 += 1
                #         else:
                #             print('False')
                #     print(desc)
                #     num += 1
                #     print(num)
                #     print(num2)
                # print(len(exps))
                if ('eyes closed' in desc and 'tandem' in desc and 'facing left' in desc):
                
                    r_idx = count // ncol
                    c_idx = count - ncol * r_idx

                    for tracklet in data['data']:
                        x = tracklet['x']
                        y = tracklet['y']
                        t = tracklet['t']
                        id = tracklet['id']
                        tx = feat.trim(x)
                        if len(tx) != 0:
                            count += 1
                            ty = feat.trim(y)
                            tt = feat.trim(t)
                            (sx, sy) = feat.calibrate_center(tx, ty)

                            # plot scatter plot of data
                            plot1 = axarr[r_idx, c_idx].scatter(sx, sy, c = tt)
                            
                            # extract coordinates of axes tip and plot from 0, 0 to tip for each axis
                            # axes = cell.extract_axes(sx, sy)
                            # axarr[r_idx, c_idx].plot([0, axes[0, 0]], [0, axes[1, 0]], 'b')
                            # axarr[r_idx, c_idx].plot([0, axes[0, 1]], [0, axes[1, 1]], 'r') 
                            pri_ax, sec_ax = cell.extract_axes(sx, sy)
                            axarr[r_idx, c_idx].plot([0, pri_ax[0]], [0, pri_ax[1]], 'r')
                            axarr[r_idx, c_idx].plot([0, sec_ax[0]], [0, sec_ax[1]], 'b') 
                            
                            
                            # extract ellipse patch and add patch to plot
                            e = cell.best_fit_ellipse(sx, sy)
                            axarr[r_idx, c_idx].add_patch(e)
            
                            # setting for each plot
                            axarr[r_idx, c_idx].set_ylim(-.6, .6)
                            axarr[r_idx, c_idx].set_xlim(-.6, .6)
                            # area of ellipse as xlabel 
                            e_area = cell.area(sx, sy)
                            # axarr[r_idx, c_idx].set(xlabel='x', ylabel='y', title=f'area of ellipse: {e_area}')
                            axarr[r_idx, c_idx].set(xlabel=f'area of ellipse: {e_area}', ylabel='y')
                            
                            fig.suptitle(desc)
                
plt.show()
