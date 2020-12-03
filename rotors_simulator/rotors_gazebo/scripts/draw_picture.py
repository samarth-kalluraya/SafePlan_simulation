# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from workspace import get_label
from termcolor import colored
import scipy.stats as st

def workspace_plot(workspace, landmark, r_or_o, id_r_or_o, ax):
    """
    plot the workspace
    :param workspace: workspace
    :param r_or_o: regions or obstacles
    :param id_r_or_o: indicators for regions of obstacles
    :param ax: figure axis
    :return: figure
    """
    ax.set_xlim((0, workspace[0]))
    ax.set_ylim((0, workspace[1]))
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle=':',linewidth=0.2)
    for key in r_or_o.keys():
        color = '0.75' if id_r_or_o != 'region' else 'c'
        x = []
        y = []
        patches = []
        for point in list(r_or_o[key].exterior.coords)[:-1]:
            x.append(point[0])
            y.append(point[1])
        polygon = Polygon(np.column_stack((x, y)), True)
        patches.append(polygon)
        p = PatchCollection(patches, facecolors=color, edgecolors=color)
        ax.add_collection(p)
        ax.text(np.mean(x), np.mean(y), r'${}_{{{}}}$'.format(key[0], key[1:]), fontsize=16)
    for key in landmark.keys():
        color = '0.75' if id_r_or_o != 'region' else 'c'
        ax.text(landmark[key][0][0]+0.2, landmark[key][0][1]+0.2, r'${}_{{{}}}$'.format(key[0], key[1:]), fontsize=16)

def landmark_plot(workspace, landmark, ax):
    ax.set_xlim((0, workspace[0]))
    ax.set_ylim((0, workspace[1]))
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')
    for key in landmark.keys():
        color = 'k'
        x_l=landmark[key][0][0]
        y_l=landmark[key][0][1]
        x = []
        y = []
        patches = []
        x.append(x_l + 0.02)
        y.append(y_l + 0.02)
        
        x.append(x_l + 0.02)
        y.append(y_l - 0.02)
        
        x.append(x_l - 0.02)
        y.append(y_l - 0.02)
        
        x.append(x_l - 0.02)
        y.append(y_l + 0.02)
        
        polygon = Polygon(np.column_stack((x, y)), True)
        patches.append(polygon)
        p = PatchCollection(patches, facecolors=color, edgecolors=color)
        ax.add_collection(p)
        # ax.text(np.mean(x), np.mean(y), r'${}_{{{}}}$'.format(key[0], key[1:]), fontsize=16)
    
def scatter_gaussian_plot(workspace, landmark, lm_x, lm_y, ax):
    ax.set_xlim((0, workspace[0]))
    ax.set_ylim((0, workspace[1]))
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')
    
    """
    For scatter points of gaussian points uncomment part A
    For gaussian plot around landmarks uncomment part B 
    """
    """
    Part A
    """
    for i in range(len(landmark)):
        ax.scatter(lm_x[i,:],lm_y[i,:],s=1, marker='.')
    
    """
    End of Part A
    """
    """
    Part B
    """
    # x=lm_x.ravel()
    # y=lm_y.ravel()
    # deltaX = (max(x) - min(x))/10
    # deltaY = (max(y) - min(y))/10
    # xmin = 0
    # xmax = workspace[0]
    # ymin = 0
    # ymax = workspace[1]
    # xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    # positions = np.vstack([xx.ravel(), yy.ravel()])
    # values = np.vstack([x, y])
    # kernel = st.gaussian_kde(values)
    # f = np.reshape(kernel(positions).T, xx.shape)
    # cfset = ax.contourf(xx, yy, f, cmap='coolwarm')
    """
    End of Part B
    """
    
    
    
def path_plot(path, workspace, lm, number_of_robots, round_num, identity):
    """
    plot the path
    :param path: found path
    :param workspace: workspace
    :param number_of_robots:
    :return: figure
    """

    for n in range(number_of_robots):
        ax = plt.figure(n).gca()
        # workspace_plot(workspace.workspace, workspace.regions, 'region', ax)
        scatter_gaussian_plot(workspace.workspace, lm.landmark, lm.landmark_x, lm.landmark_y, ax)
        workspace_plot(workspace.workspace, workspace.landmark, workspace.obs, 'obs', ax)
        landmark_plot(workspace.workspace, workspace.landmark, ax)
        

        # prefix path
        x_pre = np.asarray([point[0][n][0] for point in path[0]])
        y_pre = np.asarray([point[0][n][1] for point in path[0]])
        pre = plt.quiver(x_pre[:-1], y_pre[:-1], x_pre[1:] - x_pre[:-1], y_pre[1:] - y_pre[:-1],
                         headlength=0, headaxislength=0, width=0.003, color='r',
                         scale_units='xy', angles='xy', scale=1, label='prefix path')

        # suffix path
        x_suf = np.asarray([point[0][n][0] for point in path[1]])
        y_suf = np.asarray([point[0][n][1] for point in path[1]])
        suf = plt.quiver(x_suf[:-1], y_suf[:-1], x_suf[1:] - x_suf[:-1], y_suf[1:] - y_suf[:-1], color='g',
                         scale_units='xy', angles='xy', scale=1, label='suffix path')
        ax.scatter(path[0][0][0][n][0],path[0][0][0][n][1], s=3, c='k', marker='x')
        
        plt.savefig('/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/scripts/img/{}_{}_path{}.png'.format(identity, round_num+1, n+1), bbox_inches='tight', dpi=600)
        # plt.savefig('img/pat0.png', dpi=600)


def path_print(path, workspace, number_of_robots):
    """
    print the path
    :param path: found path
    :param workspace: workspace
    :param number_of_robots:
    :return: printed path of traversed regions. points with empty label are depicted as dots
    """
    for n in range(number_of_robots):
        print('robot {0:<2}: '.format(n+1), end='')
        # prefix path, a path of x's or y's of a robot
        x_pre = [point[0][n][0] for point in path[0]]
        y_pre = [point[0][n][1] for point in path[0]]
        path_print_helper(x_pre, y_pre, workspace)
        # suffix path
        x_suf = [point[0][n][0] for point in path[1]]
        y_suf = [point[0][n][1] for point in path[1]]
        path_print_helper(x_suf, y_suf, workspace)
        print('')


def path_print_helper(x, y, workspace):
    """
    help to print the path
    :param x: a path of x's of a robot throughout the run
    :param y: a path of y's of a robot throughout the run
    :param workspace: workspace
    :return: printed path of traversed regions. points with empty label are depicted as dots
    """
    for i in range(len(x)):
        label = get_label((x[i], y[i]), workspace)
        label = ' .' if not label else label
        print(label + ' --> ', end='')
    print(colored('|| ', 'yellow'), end='')
