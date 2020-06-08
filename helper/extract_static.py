#!/usr/bin/python3
import json
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits import mplot3d
import helper.extract_feats as feat

# def border(x ,y):
#     x0y0 = (min(x), min(y))
#     x1y1 = (max(x), max(y))
#     return (x0y0, x1y1)

def point_distance(xi, yi, cont_x, cont_y):
    distance = []
    for i in range(len(cont_x)): 
        xd = cont_x[i] - xi
        yd = cont_y[i] - yi
        d = np.sqrt(xd ** 2 + yd ** 2)
        distance.append(d)
    return distance

def n_near_pts(x, y, samples=4.0, distance_threshold=.6):   # samples  is  half  the  number  of  samples
    near_points = []                                   # considered around one timepoint -- sampling
    # if samples == None:                                # rate is about 22 samples/second
    #     samples = int(input('Seconds to consider: '))
    # samples = samples[0]
    samples = int(samples*11)
    # if distance_threshold == None:
    #     distance_threshold = float(input('Consider data in range (m):'))
    for i in range(samples, len(x)-samples):  
        cont_x = x[i - samples: i + samples]
        cont_y = y[i - samples: i + samples]
        pt_dist = point_distance(x[i], y[i], cont_x, cont_y)
        near_count = sum([int(d < distance_threshold) for d in pt_dist])
        near_points.append(near_count)
    padding = [0 for i in range(samples)]
    near_points = padding + near_points
    near_points += padding
    return near_points

def find_static_phases(x, y, samples=4.0, distance_threshold=.6, **static_min_len):
    near_points = n_near_pts(x, y, samples, distance_threshold=distance_threshold)
    q_data_pts = [int(i == max(near_points)) for i in near_points]
    q_idx = [i for i, q in enumerate(q_data_pts) if q != 0]
    static_phases = []
    temp = [q_idx[0]]
    for i in range(1, len(q_idx)):
        if q_idx[i] == q_idx[i-1] + 1 and i == len(q_idx):
            temp.append(q_idx[i])
            static_phases.append(temp)
        elif q_idx[i] == q_idx[i-1] + 1: 
            temp.append(q_idx[i])
        else:
            static_phases.append(temp)
            temp = [q_idx[i]]
    static_phases = [phase for phase in static_phases if len(phase) >= static_min_len['static_min_len']]
    return static_phases


def extract_static_data(x, y, t, samples=4.0, distance_threshold=.6, static_min_len=55):
    static_idx = find_static_phases(x, y, samples, distance_threshold, static_min_len=static_min_len)
    xs = []
    ys = []
    ts = []
    index = []
    for idx in static_idx:
        xs.append(list(x[idx[0]:idx[-1]]))
        ys.append(list(y[idx[0]:idx[-1]]))
        ts.append(list(t[idx[0]:idx[-1]]))
        index.append((idx[0],idx[-1]))
    return (xs, ys, ts, index)




