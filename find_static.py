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
    # f = '1904186b-a659-4f77-841f-b781dd910396.ustracklets.1546553953416.json'
    # f = 'f617a98a-195a-48bf-9e00-16050501709d.ustracklets.1546553952626.json'
    # walking experiment:
    # f = '518df718-06fb-4512-8cc3-c14066fd73a8.ustracklets.1546553952258.json'
    f = 'cb1895f4-0ef7-4b74-b6f3-14f97414fe18.ustracklets.1546553951350.json'
    with open(os.path.join('/home/joshuakt/Balance/jan2/',f), 'r') as exp:
        data = json.load(exp)
        desc = data['metadata']['description']
        
    for tracklet in data['data']:
        x = tracklet['x']
        y = tracklet['y']
        z = tracklet['z']
        t = tracklet['t']
        id = tracklet['id']

        sample = 4.0
        d = .6
        near_point_count = static.n_near_pts(x, y, sample, distance_threshold=d)

        fig ,axarr = plt.subplots(2, 1)

        axarr[0].plot(t, y)
        axarr[0].set(xlabel='t', ylabel='y', title='y over time')

        axarr[1].plot(t, near_point_count)
        axarr[1].set(xlabel='t', ylabel='# near points', title='# points near xt over time'+str(sample)+str(d))
       
        static.find_static_phases(x, y, static_min_len=55)

        # samples_sec = [i*0.5 for i in range(2,9)]
        # dist_thres = [i*0.1 for i in range(2,9)]

        # for sample in samples_sec:
        #     for d in dist_thres:
        #         near_point_count = static.n_near_pts(x, y, sample, distance_threshold=d)
    
        #         fig ,axarr = plt.subplots(2, 1)
    
        #         axarr[0].plot(t, y)
        #         axarr[0].set(xlabel='t', ylabel='y', title='y over time')
    
        #         axarr[1].plot(t, near_point_count)
        #         axarr[1].set(xlabel='t', ylabel='# near points', title='# points near xt over time'+str(sample)+str(d))

    plt.show()


