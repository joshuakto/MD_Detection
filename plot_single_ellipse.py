#!/usr/bin/python3
import json
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits import mplot3d
import helper.extract_feats as feat


if __name__ == '__main__':
    f = input('Process File: ')
    with open(os.path.join('/home/joshuakt/Balance/dec23/',f), 'r') as exp:
        data = json.load(exp)
    
        for tracklet in data['data']:
            x = tracklet['x']
            y = tracklet['y']
            t = tracklet['t']
            tx = feat.trim(x)
            if len(tx) != 0:
                ty = feat.trim(y)
                tt = feat.trim(t)
                (sx, sy) = feat.calibrate_center(tx, ty)
                E = np.zeros((len(sx), 2))
                for i in range(len(sy)):
                    E[i][0] = sx[i]
                    E[i][1] = sy[i]
                cov = np.matmul(E.transpose(), E) 
                w, vec = np.linalg.eig(cov)
                rotated = np.matmul(E, vec)
                x_max = np.amax(abs(rotated[:,0]))
                y_max = np.amax(abs(rotated[:,1]))
                id = tracklet['id']
            
                fig = plt.figure(1)
                ax = fig.add_subplot(1,1,1)
                ax.scatter(sx,sy, c = tt)                
                pri_ax = x_max * vec[:,0]
                sec_ax = y_max * vec[:,1]
                pri_mag = 2 * np.sqrt(np.sum(np.square(pri_ax)))
                sec_mag = 2 * np.sqrt(np.sum(np.square(sec_ax)))
#                tr = vec[0, 0] + vec[1, 1] 
#                tr = cov[0,0] + cov[1,1]
                theta = 180 * math.atan(sec_ax[1]/sec_ax[0]) / math.pi
#                theta = 180 * math.acos((tr - 1)/ 2) / math.pi
#                e = Ellipse((0, 0), sec_mag, pri_mag, angle=math.pi - theta, alpha=.7)
                e = Ellipse((0, 0), sec_mag, pri_mag, angle=theta, alpha=.7)
                ax.plot([0, pri_ax[0]], [0, pri_ax[1]])
                ax.plot([0, sec_ax[0]], [0, sec_ax[1]],'b')
                ax.set_ylim(-.5, .5)
                ax.set_xlim(-.5, .5)
                ax.add_patch(e)
                 
                i = np.ones(2)
                r = np.matmul(i, vec)

#                plt.figure(2)
#                plt.scatter(rotated[:,0], rotated[:,1], c = tt)
#                plt.plot([0, w[0]*vec[0, 0]], [0, w[0] * vec[1, 0]])
#                plt.plot([0, w[1]*vec[0, 1]], [0, w[1] * vec[1, 1]])
#                plt.ylim(-.5, .5)
#                plt.xlim(-.5, .5)

#                plot1 = axarr[r_idx, c_idx].scatter(sx, sy, c = tt)
#                axarr[r_idx, c_idx].plot([0, w[0]*vec[0, 0]], [0, w[0] * vec[1, 0]])
#                axarr[r_idx, c_idx].plot([0, w[1]*vec[0, 1]], [0, w[1] * vec[1, 1]])
                
#                cbar = fig.colorbar(plot1, ax=axarr[r_idx, c_idx])
#                cbar.ax.set_ylabel('time')
            
plt.show()
