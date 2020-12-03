#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 11:42:55 2020

@author: samarth
"""


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from random import uniform
from networkx.classes.digraph import DiGraph
from networkx.algorithms import dfs_labeled_edges
import math
import pyvisgraph as vg
from collections import OrderedDict
from shapely.geometry import Point, LineString
from uniform_geometry import sample_uniform_geometry
from scipy.stats import truncnorm



num_of_classes=3
nn_output = {'l2': [[2, 'walking_person'], [24.56827828550672, 66.91138914185045], np.array([0.01876828, 0.93232888, 0.04890284])], 
             'l3': [[1, 'person'], [23.502199855640697, 60.14144415717649], np.array([0.87491273, 0.04265166, 0.08243561])]}
sensor_model = [[0.80, 0.18, 0.02],
				[0.23, 0.75, 0.02],
				[0.06, 0.04, 0.9]]  
classes_est = {'l1': [np.array([0.7, 0.25, 0.05])],
            'l2': [np.array([0.35, 0.6, 0.05])],
            'l3': [np.array([0.6, 0.35, 0.05])],
            'l4': [np.array([0.25, 0.7, 0.05])],
            'l5': [np.array([0.15, 0.8, 0.05])],
            'l6': [np.array([0.82, 0.13, 0.05])],
            'l7': [np.array([0.65, 0.3, 0.05])],
            'l8': [np.array([0.22, 0.73, 0.05])],
            'l9': [np.array([0.72, 0.23, 0.05])],
            'l10': [np.array([0.64, 0.31, 0.05])],
            'l11': [np.array([0.12, 0.83, 0.05])],
            'l12': [np.array([0.02, 0.03, 0.95])],
            'l13': [np.array([0.21, 0.7, 0.09])]
            }
def get_nn_prob(class_id):
    result = np.zeros((num_of_classes,))
    prob = np.random.normal(0.75, 0.1, 1)
    while prob>0.99 or prob<0.2:
        prob = np.random.normal(0.75, 0.1, 1)
    result[class_id-1] = prob
    count = 1
    for i in range(num_of_classes):
        if i!= class_id-1:
            count+=1
            remaining_prob = 1 - result.sum()
            prob = np.random.uniform(0.01,remaining_prob,1)
            if count==num_of_classes:
                result[i] = remaining_prob  
            else:
                result[i] = prob
    return result


def update_class_distribution(nn_output):
	global classes_est
	for key in nn_output.keys():
		class_id = nn_output[key][0][0] - 1
		cond_prob = np.empty((num_of_classes,), float)
		cond_prob[class_id] = nn_output[key][2][class_id]
		for i in range(num_of_classes):
			if i!=class_id:
				cond_prob[i] = sensor_model[class_id][i]
		classes_est[key] = classes_est[key]*cond_prob/(classes_est[key]*cond_prob).sum()

# update_class_distribution(nn_output)
# print(classes_est)
print("\n\n\njeyo\n\n")


t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
plt.plot(t, s)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.savefig("test.png")
plt.show()