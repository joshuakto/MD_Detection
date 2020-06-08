#!/usr/bin/python3
import json
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import statistics as stat

# def average_deviation(center, x, y):
#     xdev = [abs(xv - center[0]) for xv in x]
#     ydev = [abs(yv - center[0]) for yv in y]
#     dev = [sum(xdev)/len(x), sum(ydev)/len(y)]
#     return dev

def load(data):
    d = []
    for Tracklet in data:
        tmpx = Tracklet['x']
        tmpy = Tracklet['y']
        tmpt = Tracklet['t']
        tmpid = Tracklet['id']
        d.append({'id': tmpid, 'x': tmpx, 'y': tmpy, 't': tmpt})
    return d 

def trim(vec):
    try:
        return vec[38:-38]
    except:
        print('IndexError: data not trimmed')
        return vec

def distance_from_start(x, y):
    distances = [0]
    for i in range(len(x) - 1):
        xdistsq = (x[i] - x[0]) ** 2
        ydistsq = (y[i] - y[0]) ** 2
        distances.append((xdistsq + ydistsq) ** .5)
    return distances

def center(x, y):
    xavg = sum(x)/len(x)
    yavg = sum(y)/len(y)
    return [xavg, yavg] 

def calibrate_center(x, y):
    cen = center(x, y)
    sx = [i - cen[0] for i in x]
    sy = [i - cen[1] for i in y]
    return [sx, sy]

def distance_from_center(x, y):
    distances = []
    center_xy = center(x, y)
    for i in range(len(x) - 1):
        xdistsq = (x[i] - center_xy[0]) ** 2
        ydistsq = (y[i] - center_xy[1]) ** 2
        distances.append((xdistsq + ydistsq) ** .5)
    distances.insert(0, distances[0])
    return distances

def angle_to_center(x, y):
    angles = np.empty(len(x))
    for i in range(len(x)):
        if x[i] == 0 and y[i] == 0:
            angles[i] = np.nan      
        elif x[i] == 0:
            angles[i] = np.sign(y[i]) * np.pi / 2
        elif y[i] == 0:
            if x[i] > 0:
                angles[i] = 0
            else:
                angle[i] = np.pi
        # else if np.sign(x[i] * y[i]) == 1:
        else:
            ang = np.arctan(y[i]/x[i])
            if x[i] < 0:
                angles[i] = -np.pi + ang
            else:
                angles[i] = ang
    for i in range(len(angles)):
        if angles[i] < 0:
            angles[i] += 2 * np.pi
    return angles
                
def extract_angles_categories(x, y, intervals):
    angles = angle_to_center(x, y)
    categorical = [0 for i in range(intervals)]
    cat_w = 2*np.pi / intervals
    for ang in angles:
        cat_idx = int(ang // cat_w)
        categorical[cat_idx] += 1
    return categorical

def rms_center_distance(x, y):
    sqd = [ i ** 2 for i in distance_from_center(x, y)]
    return (sum(sqd)/len(sqd))**.5

def avg_dev(x, y):
    dist_from_center = distance_from_center(x, y)
    return sum(dist_from_center)/len(dist_from_center) 

def avg_dev_s(x, y):
    dist_from_start = distance_from_start(x, y)
    return sum(dist_from_start)/len(dist_from_start) 

if __name__ == '__main__':
    file = input('input file: ')
    with open(os.path.join('/home/joshuakt/Balance/dec23/', file), 'r') as f:
        data = json.load(f)['data']

    for tracklet in data:

        x = tracklet['x']
        y = tracklet['y']
        z = tracklet['z']
        t = tracklet['t']
        id = tracklet['id']

        tx = trim(x)
        ty = trim(y)
        tt = trim(t)
        
        dc = distance_from_center(tx, ty)
        ds = distance_from_start(x, y)

        fig ,axarr = plt.subplots(2, 3)
        plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
        axarr[0, 0].plot(x, y)
        axarr[0, 0].set(xlabel='x', ylabel='y', title='x-y positon over time')
 
        # t = np.arange(len(x))
        plot1 = axarr[0, 1].scatter(x, y, c = t)
        axarr[0, 1].set(xlabel='x', ylabel='y', title='Scatter plot of x-y data over time (color chage proportional to time)')
        cbar = fig.colorbar(plot1, ax=axarr[0, 1])
        cbar.ax.set_ylabel('time')
 
        axarr[1, 0].plot(tt, dc)
        axarr[1, 0].set(xlabel='t', ylabel='v', title='dc')

        axarr[1, 1].plot(t, ds)
        axarr[1, 1].set(xlabel='t', ylabel='y', title='ds')
 
        axarr[1, 2].plot(t, x)
        axarr[1, 2].set(xlabel='t', ylabel='x', title='y over time')
 
        print(avg_dev(tx, ty)) 
       
plt.show()
