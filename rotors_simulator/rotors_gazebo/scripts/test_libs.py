#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pip install Shapely
Created on Thu Oct  1 11:42:55 2020

@author: samarth
"""

from __future__ import print_function 


import subprocess
import os.path
import re
import networkx as nx
import numpy as np
from networkx.classes.digraph import DiGraph
from sympy import satisfiable
from sympy.parsing.sympy_parser import parse_expr    #samarth change

from itertools import combinations


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from random import uniform
from networkx.classes.digraph import DiGraph
from networkx.algorithms import dfs_labeled_edges
import math
import numpy as np
from collections import OrderedDict
import pyvisgraph as vg
from shapely.geometry import Point, LineString
from uniform_geometry import sample_uniform_geometry
from scipy.stats import truncnorm
import datetime


import matplotlib.pylab as p
from workspace import Workspace
# import visilibity as vis

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from workspace import get_label
from termcolor import colored
import scipy.stats as st

from shapely.geometry import Polygon, Point

import pyvisgraph as vg
from workspace import Workspace, get_label
from random import uniform
import numpy as np
from sympy import Symbol

from task import Task
from buchi_parse import Buchi
from workspace import Workspace
import datetime
from collections import OrderedDict
import numpy as np
from biased_tree import BiasedTree
from construct_biased_tree import construction_biased_tree, path_via_visibility
from draw_picture import path_plot, path_print
from text_editor import export_to_txt, export_cov_to_txt, export_disc_to_txt
import matplotlib.pyplot as plt
import pyvisgraph as vg
from termcolor import colored
import networkx as nx









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

update_class_distribution(nn_output)
print(classes_est)
print("\n\n\njeyo")



t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
plt.plot(t, s)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.savefig("test.png")
plt.show()