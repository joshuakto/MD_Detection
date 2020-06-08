#!/usr/bin/python3

import json

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


if __name__ == '__main__':

    with open('test_reported/116ab1fd-1295-47d4-8d23-1248d32ed2d5.ustracklets.1545344288993.json', 'r') as f:

        data = json.load(f)['data']

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    for tracklet in data:

        x = tracklet['x']

        y = tracklet['y']

        z = tracklet['z']

        t = tracklet['t']

        id = tracklet['id']

        print(t[0])


        ax.plot3D(x, y, z, 'gray')
        ax.scatter3D(x[0], y[0], z[0], c = 'b', marker='^')
        plt.xlabel('x')
        plt.ylabel('y')
        # plt.plot(x, y, z)

    plt.show()
