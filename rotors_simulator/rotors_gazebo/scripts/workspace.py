# -*- coding: utf-8 -*-

from shapely.geometry import Polygon, Point
import numpy as np
import matplotlib.pyplot as plt

import datetime


def get_label(x, workspace):
    """
    generating the label of position component
    """
    point = Point(x)
    # whether x lies within obstacle
    for (obs, boundary) in iter(workspace.obs.items()):
        if point.within(boundary):
            return obs

    # whether x lies within regions
    # for (region, boundary) in iter(workspace.regions.items()):
    #     if point.within(boundary):
    #         return region
    # x lies within unlabeled region
    return ''




class Workspace(object):
    """
    define the workspace where robots reside
    """
    def __init__(self):
        # dimension of the workspace
        self.length = 150
        self.width = 150
        self.workspace = (self.length, self.width)
        
        # Remember: the list of points in obstacle polygon must be CLOCK-WISE(cw)    
        self.obs = {'o1': Polygon([(40, 120), (40, 150), (70, 150), (70, 120)]),
                       'o2': Polygon([(40, 80), (40, 110), (70, 110), (70, 80)]),
                        'o3': Polygon([(40, 40), (40, 70), (70, 70), (70, 40)])
                    }
        self.padded_obs={}
        self.pad_obstacle(3)
        # original
        # center = [(9.6, 132), (25, 67), (24, 59), (18, 25), (43, 22), (97, 9), (75, 47), 
        #           (100, 91), (104, 136), (128, 10), (100, 55), (135, 95), (129, 48)]
        # all different
        # center = [(9.6, 132), (20, 67), (20, 55), (25, 38), (38, 27), (92, 14), (78, 52), 
        #           (95, 96), (100, 140), (125, 14), (95, 60), (130, 100), (124, 52)]
        # center = [(9.6, 132), (25, 67), (24, 59), (16, 42), (43, 22), (97, 9), (75, 47), 
        #           (100, 91), (100, 140), (125, 14), (95, 60), (135, 95), (129, 48)]
        center = [(9.6, 132), (20, 67), (24, 59), (25, 38), (43, 22), (97, 9), (75, 47), 
                  (106, 87.5), (104, 136), (128, 10), (102, 66), (135, 95), (129, 48)]
        self.landmark= {'l1': [[center[0][0], center[0][1]],  [[3, 0], [0, 3]], []],
                        'l2': [[center[1][0], center[1][1]],  [[3, 0], [0, 4]], []],
                        'l3': [[center[2][0], center[2][1]],  [[3, 0], [0, 3]], []],
                        'l4': [[center[3][0], center[3][1]],  [[1, 0], [0, 5]], []],
                        'l5': [[center[4][0], center[4][1]],  [[5, 0], [0, 4]], []],
                        'l6': [[center[5][0], center[5][1]],  [[4, 0], [0, 2]], []],
                        'l7': [[center[6][0], center[6][1]],  [[3, 0], [0, 4]], []],
                        'l8': [[center[7][0], center[7][1]],  [[2, 0], [0, 2]], []],
                        'l9': [[center[8][0], center[8][1]],  [[1, 0], [0, 1]], []],
                        'l10': [[center[9][0], center[9][1]],  [[2, 0], [0, 2]], []],
                        'l11': [[center[10][0], center[10][1]],  [[2, 0], [0, 2]], []],
                        'l12': [[center[11][0], center[11][1]],  [[2, 0], [0, 2]], []],
                        'l13': [[center[12][0], center[12][1]],  [[2, 0], [0, 2]], []]
                        }
        # self.classes = {1: ['l2','l1'],
        #                 2: ['l6','l3','l5'],
                        # 3: ['l5']}
        self.no_of_classes = 3
        self.classes = np.array([[0.7, 0.25, 0.05],
                                  [0.35, 0.6, 0.05],
                                  [0.6, 0.35, 0.05],
                                  [0.25, 0.7, 0.05],
                                  [0.15, 0.8, 0.05],
                                  [0.82, 0.13, 0.05],
                                  [0.65, 0.3, 0.05],
                                  [0.22, 0.73, 0.05],
                                  [0.72, 0.23, 0.05],
                                  [0.64, 0.31, 0.05],
                                  [0.12, 0.83, 0.05],
                                  [0.02, 0.03, 0.95],
                                  [0.21, 0.7, 0.09]])
        self.num_sample_points = 200
        self.landmark_x = np.empty((len(self.landmark.keys()),self.num_sample_points))
        self.landmark_y = np.empty((len(self.landmark.keys()),self.num_sample_points))
        self.generate_samples()
        
    def generate_samples(self):
        self.landmark_x = np.empty((len(self.landmark.keys()),self.num_sample_points))
        self.landmark_y = np.empty((len(self.landmark.keys()),self.num_sample_points))
        i = 0
        for key in self.landmark.keys():
            mean = self.landmark[key][0]
            cov = self.landmark[key][1]
            self.landmark_x[i,:],self.landmark_y[i,:]=np.random.multivariate_normal(mean, cov, self.num_sample_points).T
            i += 1
               
    def generate_samples_for_lm(self,key):
        i = int(key[1:]) - 1
        mean = self.landmark[key][0]
        cov = self.landmark[key][1]
        self.landmark_x[i,:],self.landmark_y[i,:]=np.random.multivariate_normal(mean, cov, self.num_sample_points).T
 
    def pad_obstacle(self, padding):
        for (obs, boundary) in iter(self.obs.items()):
            obs_x,obs_y = boundary.exterior.coords.xy
            new_poly=[]
            centroid_x = 0
            centroid_y = 0            
            for i in range(len(obs_x)-1):
                centroid_x = centroid_x + obs_x[i]
                centroid_y = centroid_y + obs_y[i]
            centroid_x=centroid_x/(len(obs_x)-1)
            centroid_y=centroid_y/(len(obs_x)-1)
            for i in range(len(obs_x)-1):
                v=np.array([obs_x[i]-centroid_x,obs_y[i]-centroid_y])
                v1=v/np.linalg.norm(v)
                new_poly.append((obs_x[i]+v1[0]*padding,obs_y[i]+v1[1]*padding))
            self.padded_obs[obs]=Polygon(new_poly)

    def update_covariance_shape(self):
        for key in self.landmark.keys():
            lambda_, v = np.linalg.eig(self.landmark[key][1])
            lambda_ = np.sqrt(lambda_)
            x, y= self.landmark[key][0]
            width = lambda_[0]*3*2
            height = lambda_[1]*3*2
            angle= np.arccos(v[0, 0])
            quat_z = np.sin(angle/2)
            quat_w = np.cos(angle/2)
            self.landmark[key][2] = [[width,height],[quat_z,quat_w]]     
                        
    def update_covariance_shape_for_lm(self,key):
        lambda_, v = np.linalg.eig(self.landmark[key][1])
        lambda_ = np.sqrt(lambda_)
        x, y= self.landmark[key][0]
        width = lambda_[0]*3*2
        height = lambda_[1]*3*2
        angle= np.arccos(v[0, 0])
        quat_z = np.sin(angle/2)
        quat_w = np.cos(angle/2)
        self.landmark[key][2] = [[width,height],[quat_z,quat_w]]
                    

class Landmark(object):
    """
    define the workspace where robots reside
    """
    def __init__(self):
        # dimension of the workspace
        
        self.landmark= {}
        # self.classes = {1: ['l2','l1'],
        #                 2: ['l6','l3','l5'],
                        # 3: ['l5']}
        self.no_of_classes = 3
        self.num_sample_points = 200
        self.landmark_x = np.empty((len(self.landmark.keys()),self.num_sample_points))
        self.landmark_y = np.empty((len(self.landmark.keys()),self.num_sample_points))
        
    def generate_samples(self):
        self.landmark_x = np.empty((len(self.landmark.keys()),self.num_sample_points))
        self.landmark_y = np.empty((len(self.landmark.keys()),self.num_sample_points))
        i = 0
        for key in self.landmark.keys():
            mean = self.landmark[key][0]
            cov = self.landmark[key][1]
            self.landmark_x[i,:],self.landmark_y[i,:]=np.random.multivariate_normal(mean, cov, self.num_sample_points).T
            i += 1
            
    def generate_samples_for_lm(self,key):
        i = int(key[1:]) - 1
        mean = self.landmark[key][0]
        cov = self.landmark[key][1]
        self.landmark_x[i,:],self.landmark_y[i,:]=np.random.multivariate_normal(mean, cov, self.num_sample_points).T

            
    def update_from_landmark(self,landmark_obj):
        self.landmark = landmark_obj.landmark.copy()
        start = datetime.datetime.now()   
        self.landmark_x = landmark_obj.landmark_x.copy()
        self.landmark_y = landmark_obj.landmark_y.copy()
        # self.generate_samples()
        NBA_time = (datetime.datetime.now() - start).total_seconds()
        print('Time for constructing the NBA: {0:.4f} s'.format(NBA_time))
        
        
    def update_from_workspace(self,workspace_obj):
        self.landmark = workspace_obj.landmark.copy()
        self.landmark_x = workspace_obj.landmark_x.copy()
        self.landmark_y = workspace_obj.landmark_y.copy()

            

# w=Workspace()  
# lm=Landmark()
# lm.update_from_workspace(w)