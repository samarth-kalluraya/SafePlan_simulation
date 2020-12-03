#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:13:06 2020

@author: samarth
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def generate_samples(mean, cov):
    n = 1000
    landmark_x = np.empty((1,n))
    landmark_y = np.empty((1,n))
    landmark_x[0,:],landmark_y[0,:]=np.random.multivariate_normal(mean, cov, n).T
    return landmark_x, landmark_y

def scatter_gaussian_plot(lm_x, lm_y, ax):
    ax.set_xlim((-25, 55))
    ax.set_ylim((-25, 55))
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(b=True, which='major', color='k', linestyle='--')
   
    ax.scatter(lm_x[0,:],lm_y[0,:],s=1, marker='.')

np.random.seed(0)

cov = [[10,4],[0, 15]]

mean = [18, 7]

ax = plt.figure(1).gca()

x, y = generate_samples(mean, cov)
# ax.scatter(x, y, s=0.5)
scatter_gaussian_plot(x, y, ax)
# ax.axvline(c='grey', lw=1)
# ax.axhline(c='grey', lw=1)

confidence_ellipse(x, y, ax, edgecolor='red')

# ax.scatter(mu[0], mu[1], c='red', s=3)
# ax.set_title(title)          

plt.show()


cov = np.cov(x, y)
lambda_, v = np.linalg.eig(cov)
lambda_ = np.sqrt(lambda_)
ax = plt.subplot(111, aspect='equal')
ax.set_xlim((-25, 55))
ax.set_ylim((-25, 55))
ell = Ellipse(xy=(np.mean(x), np.mean(y)),
              width=lambda_[0]*3*2, height=lambda_[1]*3*2,
              angle= np.rad2deg(np.arccos(v[0, 0])), edgecolor='red'  )
ell.set_facecolor('none')

ax.add_artist(ell)
plt.scatter(x, y, s=0.5)
plt.show()