#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 12:18:54 2020

@author: samarth

"""
import matplotlib.pyplot as plt
import numpy as np

def get_H_matrix(x, y, rob_x, rob_y):
    index1 = (x - rob_x)/np.sqrt((x - rob_x)**2 + (y - rob_y)**2)
    index2 = (y - rob_y)/np.sqrt((x - rob_x)**2 + (y - rob_y)**2)
    return np.array([[index1, index2]])

def kf_update(cov, x_estimate, obs, R):
    """
    Parameters
    ----------
    cov : 2x2 covariance of landmark
    x_estimate : landmark mean position
    obs : robot position
    R : scalar measurement nose 

    Returns
    -------
    updated covariance matrix

    """
    sigma = np.array(cov)
    
    x = np.array(x_estimate).reshape(2,1)
    z = np.array(obs).reshape(2,1)

    H = np.array([[1,0],[0,1]])
    M = H.dot(sigma).dot(np.transpose(H)) + R
    K = sigma.dot(np.transpose(H)).dot(np.linalg.inv(M))
    updated_cov = np.dot((np.eye(2) - np.dot(K, H)), sigma)
    updated_x = x + np.dot(K, (z-x))
    return [updated_x[0][0],updated_x[1][0]], updated_cov

def generate_samples(mean, cov):
    n = 1000
    landmark_x = np.empty((1,n))
    landmark_y = np.empty((1,n))
    landmark_x[0,:],landmark_y[0,:]=np.random.multivariate_normal(mean, cov, n).T
    return landmark_x, landmark_y


def scatter_gaussian_plot(lm_x, lm_y, x, ax):
    ax.set_xlim((15, 25))
    ax.set_ylim((5, 15))
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')
    ax.scatter(lm_x[0,:],lm_y[0,:],s=1, marker='.')
    ax.scatter(x[0],x[1],s=2, marker='x')
    



if __name__ == "__main__":
    ax = plt.figure(22).gca()
        
    cov=[[10,0],[0, 10]]
    x_estimate = [20, 12]
    observation = [[19.05, 9.1], [17.95, 6.87],[18.11, 7],[17.94, 6.95],[18.01, 7.06],[18.05, 7.1],[18.1, 7.2],[18.1, 6.8],[17.8, 6.9]]
    # poses = [[68, 57], [58, 47], [48, 37], [38, 27], [28, 17], [18, 8]]
    # poses = [[49, 38]]
    R = [[0.5,0],[0,0.5]]
    lm_x, lm_y = generate_samples(x_estimate, cov)
    scatter_gaussian_plot(lm_x, lm_y, x_estimate, ax)
    
    for i in range(len(observation)):
        # print(cov)
        obs = observation[i]
        # print(rob_pos)
        x_estimate, cov = kf_update(cov, x_estimate, obs, R)
        
        ax = plt.figure(i).gca()
        lm_x, lm_y = generate_samples(x_estimate, cov)
        scatter_gaussian_plot(lm_x, lm_y, x_estimate, ax)
        
    
    
    # lm_x, lm_y = generate_samples(target, cov)
    # scatter_gaussian_plot(lm_x, lm_y, ax)














