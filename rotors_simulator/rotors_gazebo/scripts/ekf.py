#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 22:52:58 2020

@author: samarth
"""
import matplotlib.pyplot as plt
import numpy as np

def get_H_matrix(x, y, rob_x, rob_y):
    index1 = (x - rob_x)/np.sqrt((x - rob_x)**2 + (y - rob_y)**2)
    index2 = (y - rob_y)/np.sqrt((x - rob_x)**2 + (y - rob_y)**2)
    return np.array([[index1, index2]])

def ekf_update(cov, target, rob_pos, R):
    """
    Parameters
    ----------
    cov : 2x2 covariance of landmark
    target : landmark mean position
    rob_pos : robot position
    R : scalar measurement nose 

    Returns
    -------
    updated covariance matrix

    """
    sigma = np.array(cov)
    
    x = np.array(target).reshape(1,2)
    p_t = np.array(rob_pos).reshape(1,2)

    
    H = get_H_matrix(x[0][0], x[0][1], p_t[0][0], p_t[0][1])
    # print("\n")
    # print(H)
    
    M = H.dot(sigma).dot(np.transpose(H)) + R
    K = sigma.dot(np.transpose(H))/M
    updated_cov = np.dot((np.eye(2) - np.dot(K, H)), sigma)
    return updated_cov

def generate_samples(mean, cov):
    n = 1000
    landmark_x = np.empty((1,n))
    landmark_y = np.empty((1,n))
    landmark_x[0,:],landmark_y[0,:]=np.random.multivariate_normal(mean, cov, n).T
    return landmark_x, landmark_y


def scatter_gaussian_plot(lm_x, lm_y, ax):
    ax.set_xlim((5, 35))
    ax.set_ylim((-5, 25))
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')
   
    ax.scatter(lm_x[0,:],lm_y[0,:],s=1, marker='.')



if __name__ == "__main__":
    ax = plt.figure(22).gca()
        
    cov=[[10,0],[0, 10]]
    target = [18, 7]
    poses = [[68, 57], [48, 47],[28, 37],[38, 17],[28, 0],[18.1, 7.1],[19.1, 7.1],[19.1, 6.1],[16.1, 9.1]]
    # poses = [[68, 57], [58, 47], [48, 37], [38, 27], [28, 17], [18, 8]]
    # poses = [[49, 38]]
    R = 0.5
    lm_x, lm_y = generate_samples(target, cov)
    scatter_gaussian_plot(lm_x, lm_y, ax)
    
    for i in range(len(poses)):
        # print(cov)
        rob_pos = poses[i]
        # print(rob_pos)
        cov = ekf_update(cov, target, rob_pos, R)
        
        ax = plt.figure(i).gca()
        lm_x, lm_y = generate_samples(target, cov)
        scatter_gaussian_plot(lm_x, lm_y, ax)
        
    
    
    # lm_x, lm_y = generate_samples(target, cov)
    # scatter_gaussian_plot(lm_x, lm_y, ax)














