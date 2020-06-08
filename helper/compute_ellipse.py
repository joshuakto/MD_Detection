#!/usr/bin/python3
import json
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits import mplot3d
import helper.extract_feats as feat

def load_array(x, y):
    E = np.zeros((len(x), 2))
    for i in range(len(y)):
        E[i][0] = x[i]
        E[i][1] = y[i]
    return E

def compute_cov(x, y):
    E = load_array(x, y)
    return np.matmul(E.transpose(), E)

def extract_eig(x, y):
    cov = compute_cov(x, y)
    w, vec = np.linalg.eig(cov)
    return (w, vec)

def extract_axes(x, y):
    E = load_array(x, y)
    eig_val, eig_vec = extract_eig(x, y)
    rotated = np.matmul(E, eig_vec)
    x_max = np.amax(abs(rotated[:,0]))
    y_max = np.amax(abs(rotated[:,1]))
    pri_ax = x_max * eig_vec[:,0]
    sec_ax = y_max * eig_vec[:,1] 
    return pri_ax, sec_ax

# def extract_axes(x, y):
#     E = load_array(x, y)
#     eig_val, eig_vec = extract_eig(x, y)
#     rotated = np.matmul(E, eig_vec)
#     x_max = np.amax(abs(rotated[:,0]))
#     y_max = np.amax(abs(rotated[:,1]))
#     axes = np.matmul(np.array([[x_max, 0],[0, y_max]]), eig_vec.transpose())
#     return axes

def best_fit_ellipse(x, y):
    pri_ax, sec_ax = extract_axes(x, y)
    pri_mag = 2 * np.sqrt(np.sum(np.square(pri_ax)))
    sec_mag = 2 * np.sqrt(np.sum(np.square(sec_ax)))
    theta = 180 * math.atan(sec_ax[1]/sec_ax[0]) / math.pi
    e = Ellipse((0, 0), sec_mag, pri_mag, angle=theta, alpha=.7)
    return e

def area(x, y):
    pri_ax, sec_ax = extract_axes(x, y)
    pri_mag = 2 * np.sqrt(np.sum(np.square(pri_ax)))
    sec_mag = 2 * np.sqrt(np.sum(np.square(sec_ax)))
    area = math.pi * pri_mag * sec_mag
    return area 
    

