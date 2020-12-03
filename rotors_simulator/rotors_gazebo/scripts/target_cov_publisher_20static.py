#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, Point, Pose2D, Quaternion
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA
import numpy as np 
import scipy
from scipy.spatial.transform import Rotation as R
import sys


def cov_pub_1(x, y, width, height, quat):

	# global marker_1
	marker_1 = Marker()
	marker_1.header=Header(frame_id='world')
	marker_1.type = Marker.CYLINDER
	marker_1.pose.position.x  =  x
	marker_1.pose.position.y = y
	marker_1.pose.position.z  = 0.2
	
	marker_1.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_1.scale.x = width
	marker_1.scale.y = height
	marker_1.scale.z = 0.2

	# rospy.loginfo("x-position of robot5: %f; y_position of robot5: %f",width,height)
	marker_1.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_1.lifetime=rospy.Duration()
	cov_publisher_1.publish(marker_1)

def cov_pub_2(x, y, width, height, quat):

	# global marker_2
	marker_2 = Marker()
	marker_2.header=Header(frame_id='world')
	marker_2.type = Marker.CYLINDER
	marker_2.pose.position.x  = x
	marker_2.pose.position.y = y
	marker_2.pose.position.z  = 0.2
	marker_2.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_2.scale.x = width
	marker_2.scale.y = height
	marker_2.scale.z = 0.2
	marker_2.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_2.lifetime=rospy.Duration()

	cov_publisher_2.publish(marker_2)


def cov_pub_3(x, y, width, height, quat):
	# global marker_3
	marker_3 = Marker()
	marker_3.header=Header(frame_id='world')
	marker_3.type = Marker.CYLINDER
	marker_3.pose.position.x  = x
	marker_3.pose.position.y = y
	marker_3.pose.position.z  = 0.2
	marker_3.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_3.scale.x = width
	marker_3.scale.y = height
	marker_3.scale.z = 0.01
	marker_3.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_3.lifetime=rospy.Duration()
	cov_publisher_3.publish(marker_3)

def cov_pub_4(x, y, width, height, quat):

	global position_msg
	marker_4 = Marker()
	marker_4.header=Header(frame_id='world')
	marker_4.type = Marker.CYLINDER
	marker_4.pose.position.x  = x
	marker_4.pose.position.y = y
	marker_4.pose.position.z  = 0.2
	# marker_4.pose.position = position_msg
	# marker_4.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_4.scale.x = width
	marker_4.scale.y = height
	marker_4.scale.z = 0.05
	marker_4.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_4.lifetime=rospy.Duration()
	cov_publisher_4.publish(marker_4)


def cov_pub_5(x, y, width, height, quat):
	# global marker_5
	marker_5 = Marker()
	marker_5.header=Header(frame_id='world')
	marker_5.type = Marker.CYLINDER
	marker_5.pose.position.x  =  x
	marker_5.pose.position.y = y
	marker_5.pose.position.z  = 0.2
	marker_5.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_5.scale.x = width
	marker_5.scale.y = height
	marker_5.scale.z = 0.2
	marker_5.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_5.lifetime=rospy.Duration()
	cov_publisher_5.publish(marker_5)

def cov_pub_6(x, y, width, height, quat):
	# global marker_6
	marker_6 = Marker()
	marker_6.header=Header(frame_id='world')
	marker_6.type = Marker.CYLINDER
	marker_6.pose.position.x  = x
	marker_6.pose.position.y = y
	marker_6.pose.position.z  = 0.2
	marker_6.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_6.scale.x = width
	marker_6.scale.y = height
	marker_6.scale.z = 0.2
	marker_6.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_6.lifetime=rospy.Duration()
	cov_publisher_6.publish(marker_6)

def cov_pub_7(x, y, width, height, quat):
	# global marker_7
	marker_7 = Marker()
	marker_7.header=Header(frame_id='world')
	marker_7.type = Marker.CYLINDER
	marker_7.pose.position.x  = x
	marker_7.pose.position.y = y
	marker_7.pose.position.z  = 0.2
	marker_7.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_7.scale.x = width
	marker_7.scale.y = height
	marker_7.scale.z = 0.2
	marker_7.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_7.lifetime=rospy.Duration()
	cov_publisher_7.publish(marker_7)

def cov_pub_8(x, y, width, height, quat):
	# global marker_8
	marker_8 = Marker()
	marker_8.header=Header(frame_id='world')
	marker_8.type = Marker.CYLINDER
	marker_8.pose.position.x  = x
	marker_8.pose.position.y = y
	marker_8.pose.position.z  = 0.2
	marker_8.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_8.scale.x = width
	marker_8.scale.y = height
	marker_8.scale.z = 0.2
	marker_8.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_8.lifetime=rospy.Duration()
	cov_publisher_8.publish(marker_8)

def cov_pub_9(x, y, width, height, quat):
	# global marker_9
	marker_9 = Marker()
	marker_9.header=Header(frame_id='world')
	marker_9.type = Marker.CYLINDER
	marker_9.pose.position.x  = x
	marker_9.pose.position.y = y
	marker_9.pose.position.z  = 0.2
	marker_9.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_9.scale.x = width
	marker_9.scale.y = height
	marker_9.scale.z = 0.2
	marker_9.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_9.lifetime=rospy.Duration()
	cov_publisher_9.publish(marker_9)

def cov_pub_10(x, y, width, height, quat):
	# global marker_10
	marker_10 = Marker()
	marker_10.header=Header(frame_id='world')
	marker_10.type = Marker.CYLINDER
	marker_10.pose.position.x  = x
	marker_10.pose.position.y = y
	marker_10.pose.position.z  = 0.2
	marker_10.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_10.scale.x = width
	marker_10.scale.y = height
	marker_10.scale.z = 0.2
	marker_10.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_10.lifetime=rospy.Duration()
	cov_publisher_10.publish(marker_10)


def cov_pub_11(x, y, width, height, quat):
	# global marker_11
	marker_11 = Marker()
	marker_11.header=Header(frame_id='world')
	marker_11.type = Marker.CYLINDER
	marker_11.pose.position.x  = x
	marker_11.pose.position.y = y
	marker_11.pose.position.z  = 0.2
	marker_11.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_11.scale.x = width
	marker_11.scale.y = height
	marker_11.scale.z = 0.2
	marker_11.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_11.lifetime=rospy.Duration()
	cov_publisher_11.publish(marker_11)

def cov_pub_12(x, y, width, height, quat):
	# global marker_12
	marker_12 = Marker()
	marker_12.header=Header(frame_id='world')
	marker_12.type = Marker.CYLINDER
	marker_12.pose.position.x  = x
	marker_12.pose.position.y = y
	marker_12.pose.position.z  = 0.2
	marker_12.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_12.scale.x = width
	marker_12.scale.y = height
	marker_12.scale.z = 0.2
	marker_12.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_12.lifetime=rospy.Duration()
	cov_publisher_12.publish(marker_12)

def cov_pub_13(x, y, width, height, quat):
	# global marker_13
	marker_13 = Marker()
	marker_13.header=Header(frame_id='world')
	marker_13.type = Marker.CYLINDER
	marker_13.pose.position.x  = x
	marker_13.pose.position.y = y
	marker_13.pose.position.z  = 0.2
	marker_13.pose.orientation = Quaternion(0,0,quat[0],quat[1])

	marker_13.scale.x = width
	marker_13.scale.y = height
	marker_13.scale.z = 0.2
	marker_13.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)
	marker_13.lifetime=rospy.Duration()
	cov_publisher_13.publish(marker_13)

rospy.init_node('target_cov_plot', anonymous=True)

cov_publisher_1 = rospy.Publisher('/target1/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_2 = rospy.Publisher('/target2/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_3 = rospy.Publisher('/target3/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_4 = rospy.Publisher('/target4/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_5 = rospy.Publisher('/target5/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_6 = rospy.Publisher('/target6/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_7 = rospy.Publisher('/target7/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_8 = rospy.Publisher('/target8/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_9 = rospy.Publisher('/target9/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_10 = rospy.Publisher('/target10/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_11 = rospy.Publisher('/target11/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_12 = rospy.Publisher('/target12/cov/visualization_marker', Marker, queue_size = 10)
cov_publisher_13 = rospy.Publisher('/target13/cov/visualization_marker', Marker, queue_size = 10)	

cov_data_1 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_1.txt')
cov_data_2 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_2.txt')
cov_data_3 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_3.txt')
cov_data_4 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_4.txt')
cov_data_5 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_5.txt')
cov_data_6 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_6.txt')
cov_data_7 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_7.txt')
cov_data_8 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_8.txt')
cov_data_9 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_9.txt')
cov_data_10 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_10.txt')
cov_data_11 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_11.txt')
cov_data_12 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_12.txt')
cov_data_13 = np.loadtxt(fname = '/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource/lm_cov_13.txt')



n_waypoints = len(cov_data_1)
n_targets  = 13
rospy.sleep(3.00)
for i in range(n_waypoints):

    # rospy.loginfo("covariance at iteration: ")
    # rospy.loginfo(i)
    target_1 = cov_data_1[i]
    target_2 = cov_data_2[i]
    target_3 = cov_data_3[i]
    target_4 = cov_data_4[i]
    target_5 = cov_data_5[i]
    target_6 = cov_data_6[i]
    target_7 = cov_data_7[i]
    target_8 = cov_data_8[i]
    target_9 = cov_data_9[i]
    target_10 = cov_data_10[i]
    target_11 = cov_data_11[i]
    target_12 = cov_data_12[i]
    target_13 = cov_data_13[i]

    x_1, y_1 = target_1[0:2]
    x_2, y_2 = target_2[0:2]
    x_3, y_3 = target_3[0:2]
    x_4, y_4 = target_4[0:2]
    x_5, y_5 = target_5[0:2]
    x_6, y_6 = target_6[0:2]
    x_7, y_7 = target_7[0:2]
    x_8, y_8 = target_8[0:2]
    x_9, y_9 = target_9[0:2]
    x_10, y_10 = target_10[0:2]
    x_11, y_11 = target_11[0:2]
    x_12, y_12 = target_12[0:2]
    x_13, y_13 = target_13[0:2]    

    width_1, height_1 = target_1[2:4]
    width_2, height_2 = target_2[2:4]
    width_3, height_3 = target_3[2:4]
    width_4, height_4 = target_4[2:4]
    width_5,height_5 = target_5[2:4]
    width_6, height_6 = target_6[2:4]
    width_7, height_7 = target_7[2:4]
    width_8, height_8 = target_8[2:4]
    width_9, height_9 = target_9[2:4]
    width_10, height_10 = target_10[2:4]
    width_11, height_11 = target_11[2:4]
    width_12, height_12 = target_12[2:4]
    width_13, height_13 = target_13[2:4]
    
    quat_1 = target_1[4:6]
    quat_2 = target_2[4:6]
    quat_3 = target_3[4:6]
    quat_4 = target_4[4:6]
    quat_5 = target_5[4:6]
    quat_6 = target_6[4:6]
    quat_7 = target_7[4:6]
    quat_8 = target_8[4:6]
    quat_9 = target_9[4:6]
    quat_10 = target_10[4:6]
    quat_11 = target_11[4:6]
    quat_12 = target_12[4:6]
    quat_13 = target_13[4:6]    
    
    t = target_1[6]
    # rospy.loginfo('covariance start sleeping for: %s',str(t))
    rospy.sleep(t)
    # rospy.loginfo('command sleep time: %s', str(t))
    # rospy.loginfo('covariance waypoint: %s', str(i))
    # rospy.loginfo('publishing waypoint covariance !!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    
    cov_pub_1(x_1, y_1, width_1, height_1, quat_1)
    cov_pub_2(x_2, y_2, width_2, height_2, quat_2)
    cov_pub_3(x_3, y_3, width_3, height_3, quat_3)
    cov_pub_4(x_4, y_4, width_4, height_4, quat_4)
    cov_pub_5(x_5, y_5, width_5, height_5, quat_5)
    cov_pub_6(x_6, y_6, width_6, height_6, quat_6)
    cov_pub_7(x_7, y_7, width_7, height_7, quat_7)
    cov_pub_8(x_8, y_8, width_8, height_8, quat_8)
    cov_pub_9(x_9, y_9, width_9, height_9, quat_9)
    cov_pub_10(x_10, y_10, width_10, height_10, quat_10)
    cov_pub_11(x_11, y_11, width_11, height_11, quat_11)
    cov_pub_12(x_12, y_12, width_12, height_12, quat_12)
    cov_pub_13(x_13, y_13, width_13, height_13, quat_13)


if __name__=="__main__":
	rospy.spin()


