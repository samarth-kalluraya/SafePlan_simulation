#!/usr/bin/env python

import numpy as np
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, Point, Pose2D, Quaternion
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA, Bool, Int32

sensor_noise_cov = [[0.2, 0], [0, 0.2]]

def get_nn_prob(class_id, num_of_classes):
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

def in_FOV(FOV, pos) : 
    if (pos[0] > FOV[0] and pos[0] < FOV[2] and 
        pos[1] > FOV[1] and pos[1] < FOV[3]) : 
        return True
    else : 
        return False

def generate_nn_output(data):
	center = [(9.6, 132), (25, 67), (24, 59), (25, 38), (43, 22), (97, 9), (75, 47), 
                  (103, 87.5), (104, 136), (128, 10), (102, 60), (135, 95), (129, 48)]
	landmark_gt = {'l1': [center[0][0], center[0][1]],
	            'l2': [center[1][0], center[1][1]],
	            'l3': [center[2][0], center[2][1]],
	            'l4': [center[3][0], center[3][1]],
	            'l5': [center[4][0], center[4][1]],
	            'l6': [center[5][0], center[5][1]],
	            'l7': [center[6][0], center[6][1]],
	            'l8': [center[7][0], center[7][1]],
	            'l9': [center[8][0], center[8][1]],
	            'l10': [center[9][0], center[9][1]],
	            'l11': [center[10][0], center[10][1]],
	            'l12': [center[11][0], center[11][1]],
	            'l13': [center[12][0], center[12][1]]
	            }
	landmark_class_gt ={'l1': [1, "person"],
	            'l2': [2, "walking_person"],
	            'l3': [1, "person"],
	            'l4': [2, "walking_person"],
	            'l5': [2, "walking_person"],
	            'l6': [1, "person"],
	            'l7': [1, "person"],
	            'l8': [2, "walking_person"],
	            'l9': [1, "person"],
	            'l10': [1, "person"],
	            'l11': [2, "walking_person"],
	            'l12': [3, "police_station"],
	            'l13': [2, "walking_person"]
	            } 
	drone_x =  data.pose.pose.position.x
	drone_y =  data.pose.pose.position.y 
	drone_z =  data.pose.pose.position.z
	FOV = [drone_x-drone_z*0.75, drone_y-drone_z*0.5, drone_x+drone_z*0.75, drone_y+drone_z*0.5]
	nn_output={}
	lm_with_noise = []
	for key in landmark_gt.keys():
		if in_FOV(FOV, landmark_gt[key]):
			lm_with_noise = np.random.multivariate_normal(landmark_gt[key], sensor_noise_cov, 1).reshape(2,).tolist()
			probabiltiy = get_nn_prob(landmark_class_gt[key][0], 3)
			nn_output[key] = [landmark_class_gt[key],lm_with_noise, probabiltiy]
	# print("\n\n\nthis is what camera sees inside function")
	# print(nn_output)
	return nn_output