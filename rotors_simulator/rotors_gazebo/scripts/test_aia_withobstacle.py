#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import Header
from trajectory_msgs.msg import MultiDOFJointTrajectory, MultiDOFJointTrajectoryPoint
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Transform



import numpy as np
import dense_search
import minimum_jerk
import random
from collections import defaultdict
import math
import collision_check
from matplotlib import pyplot as plt
from samplingStrategy_v2 import SampleNodeToExtend, SampleControlAction
from RobotDynamics_v2 import RobotDynamics
from Functions_v3 import node, traceback, ekf, computeCovOfChildrenNode, ComputeUnc, UpdateBias
from PathGenerator import path_generator
from result_visual import plot_target,plot_path
from traj_generator import traj_generator
from utilities import traj2rosmsg



# for testing purpose 

def odom_cb1(data):

	rospy.loginfo("current position of the robot is : {}".format(data.pose.pose.position))




#########################################----------INITIALIZATION---------##############################################

# initialization for environment
xMin = 0
yMin = 0
xMax = 10
yMax = 10

# initialization for 

# maximum number of iterations for planning
n_max = 2000  # 85000 works


# position of targets with corresponding covariance matrix
prior_mean_1 = np.array([6, 6])
prior_cov_1 = np.array([[0.5, 0], [0, 0.5]])
prior_mean_2 = np.array([8, 9])
prior_cov_2 = np.array([[0.5, 0], [0, 0.5]])
prior_mean_3 = np.array([5, 2])
prior_cov_3 = np.array([[0.5, 0], [0, 0.5]])
prior_mean_4 = np.array([3, 7])
prior_cov_4 = np.array([[0.5, 0], [0, 0.5]])
unc_threshold = 0.01
localizedTargets = []


# initialization for ground truth targets
target_1 = prior_mean_1 + np.random.uniform(low=-0.25,high=0.25,size=2)
target_2 = prior_mean_2 + np.random.uniform(low=-0.25,high=0.25,size=2)
target_3 = prior_mean_3 + np.random.uniform(low=-0.25,high=0.25,size=2)
target_4 = prior_mean_4 + np.random.uniform(low=-0.25,high=0.25,size=2)
true_targets= [target_1,target_2,target_3,target_4]

# define the position of obstacles, the points need to be in clock-wise order
obstacle_1 = np.array([[3, 3], [3, 5], [5, 5], [5, 3]])
obstacle_2 = np.array([[4, 6], [4, 7], [5, 7], [5, 6]])
obstacle_space = [obstacle_1, obstacle_2]
tol = 0.2
robustness_mat = np.array([[-tol,-tol],[-tol,tol],[tol,tol],[tol,-tol]])
# inflate the obstacles
inflated_obstacle_space = []
for obstacle in obstacle_space:
    inflated_obstacle = obstacle + robustness_mat
    inflated_obstacle_space.append(inflated_obstacle)



listOfMean = [prior_mean_1, prior_mean_2, prior_mean_3,
              prior_mean_4]  # initial estimated pos of targets, list of numpy arrays
listOfCov = [prior_cov_1, prior_cov_2, prior_cov_3, prior_cov_4] # initial estimated cov of targets, list of numpy arrays
numOfTargets = len(listOfMean)

#visualizing targets in plot
# for target in true_targets:
#     plt.scatter(target[0],target[1],marker='s')
# for target in listOfMean:
#     plt.scatter(target[0], target[1], marker='s',color='black')

# Binary check of task completion 
task_completed = False

# initialization for robots//
# d = 2 # size of state per robot
p_init = [np.array([0.0, 0.0]), np.array([0.0, 1.0])]  # initial pos of robots, list of numpy arrays
theta_init = [np.array([np.deg2rad(0)]), np.array([np.deg2rad(0)])]  # initial heading of robots
num_of_robots = len(p_init)
sensing_range = 1 # in radius 


W = [0]
W = W + [np.deg2rad(angle) for angle in range(-180, 180, 5)]  # heading/angular velocity
# print('actions:', len(W))

stepSize = 0.5  # velocity
tau = 0.1  # discrertization
U = [0]
U = U + [stepSize] * (len(W) - 1)
# print('vel:', len(U))

control_in = []
for i in range(len(U)):
    control_in.append([W[i], U[i]])

control_in = np.asarray(
    control_in)  # convention: the first control action should correspond to "null" action (stay idle)

# obstacle_space = [[2, 8], [35, 15], [5, 65], [95, 2]]  # points occupied by obstacles


############################################------ Main Algorithm------- #############################

count = 0
replan_step = 10 # how often to replan the trajectory
robot_pose = p_init
robot_ori  = theta_init
actual_path = []
future_step = 20


# initiate the ros node for publishing trajectory msg
rospy.init_node('python_waypoint_pub_node', anonymous=True)
firefly_1_pub = rospy.Publisher('/firefly1/command/trajectory',MultiDOFJointTrajectory,queue_size = 3)
firefly_2_pub = rospy.Publisher('/firefly2/command/trajectory',MultiDOFJointTrajectory,queue_size = 3)
publishers = [firefly_1_pub,firefly_2_pub]

while not task_completed:
    if count % replan_step ==0:
        rospy.loginfo('Planner is planning a new path')

        # used for debugging, print the current ground truth state of robot 
        odom_sub_1 = rospy.Subscriber("/firefly/odometry_sensor1/odometry", Odometry, odom_cb1)

        # use initial position as the planning start point when planning the offline trajectory, use k+10 th position when performing online replanning
        if count == 0 or len(pose_list) < future_step:
            planning_start = robot_pose
        else:
            planning_start = pose_list[-future_step]

        V = path_generator(planning_start, robot_ori, control_in, listOfMean, listOfCov, sensing_range, unc_threshold, tau,
                           n_max,true_targets,inflated_obstacle_space)
        pose_list, ori_list, _ = traceback(V[-1],V)
        
        if len(pose_list) > 180:
        	future_step = 35
        else:
        	future_step = 15 
        # rospy.loginfo('The origin of this path is {}'.format(planning_start))

        #array with shape K x (number of robots x 2)
        waypoints_reversed = np.asarray(pose_list).reshape(len(pose_list), -1)
        waypoints = np.flip(waypoints_reversed,0)

        # list that stores trajectory of each robot 
        traj_list = traj_generator(waypoints)

        for i in range(len(traj_list)):
        	traj = traj_list[i]
        	traj_msg = traj2rosmsg(traj)
        	rospy.sleep(0.5)
        	publishers[i].publish(traj_msg)
        	if i==1 :
        		rospy.loginfo("Algorithm is publishing trajectory for robot 2 !!!!!!!!!!!!!!!!!!")

        #check if sleep is necessary
        
        

        # rospy.loginfo("Published new trajectory")
        # rospy.loginfo(traj.points)
        # rospy.loginfo(traj_array)

    ind = -2-(count%replan_step)  
    if abs(ind)>len(pose_list):
        rospy.loginfo('missiong completed')
        break
    # elif len(pose_list) == 1 :
    #     rospy.loginfo('mission completed')
    #     break

    # move the robot to k+1th state     
    robot_pose = pose_list[ind]
    robot_ori = ori_list[ind]

    # Update Covariance using actual measurements
    listOfCov, listOfMean = computeCovOfChildrenNode(listOfCov,robot_pose,sensing_range,listOfMean,num_of_robots,true_targets,True)
    ChildrenNodeCost = ComputeUnc(listOfCov)
    
    count += 1 

# rospy.spin()

