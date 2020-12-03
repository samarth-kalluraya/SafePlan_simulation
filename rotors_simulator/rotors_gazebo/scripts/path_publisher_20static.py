#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, Point
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA

path_1 = Path()
path_2 = Path()
path_3 = Path()
path_4 = Path()
path_5 = Path()
# path_6 = Path()
# path_7 = Path()
# path_8 = Path()
# path_9 = Path()
# path_10 = Path()
# path_11 = Path()
# path_12 = Path()
# path_13 = Path()
# path_14 = Path()
# path_15 = Path()
# path_16 = Path()
# path_17 = Path()
# path_18 = Path()
# path_19 = Path()
# path_20 = Path()
# path_21 = Path()
# path_22 = Path()

marker_1 = Marker()
marker_2 = Marker()
marker_3 = Marker()
marker_4 = Marker()
marker_5 = Marker()
# marker_6 = Marker()
# marker_7 = Marker()
# marker_8 = Marker()
# marker_9 = Marker()
# marker_10 = Marker()
# marker_11 = Marker()
# marker_12 = Marker()
# marker_13 = Marker()
# marker_14 = Marker()
# marker_15 = Marker()
# marker_16 = Marker()
# marker_17 = Marker()
# marker_18 = Marker()
# marker_19 = Marker()
# marker_20 = Marker()
# marker_21 = Marker()
# marker_22 = Marker()


#robot1 is blue 
def odom_cb1(data):
	global path_1
	# path_1 = Path()
	# marker1 = Marker()
	path_1.header = data.header
	# path_1.header.stamp = rospy.get_time()
	pose = PoseStamped()
	pose.header = data.header 
	pose.pose = data.pose.pose
	path_1.poses.append(pose)
	path_pub_1.publish(path_1)

	global marker_1 
	marker_1.header = data.header
	# marker_1.header.stamp = rospy.get_time()
	# marker_1.id=0
	marker_1.type = Marker.CUBE
	marker_1.pose.position = data.pose.pose.position
	marker_1.pose.position.z  = 0.3
	# rospy.loginfo(marker_1.pose.position)
	marker_1.scale.x = 24.0
	marker_1.scale.y = 16.0
	marker_1.scale.z = 0.1
	marker_1.color=ColorRGBA(0.573, 0.167, 0.129, 0.8)
	marker_1.lifetime=rospy.Duration()
	marker_pub_1.publish(marker_1)


def odom_cb2(data):
	# rospy.loginfo("x-position of robot2: %s; y_position of robot2: %s",data.pose.pose.position.x,data.pose.pose.position.y)

	global path_2
	path_2.header = data.header
	# path_2.header.stamp = rospy.get_time()
	pose = PoseStamped()
	pose.header = data.header 
	pose.pose = data.pose.pose
	path_2.poses.append(pose)
	path_pub_2.publish(path_2)

	global marker_2 
	marker_2.header = data.header
	# marker_2.header.stamp = rospy.get_time()
	# marker_2.id=1
	marker_2.type = Marker.CUBE
	marker_2.pose.position = data.pose.pose.position
	marker_2.pose.position.z  = 0.3
	marker_2.scale.x = 24.0
	marker_2.scale.y = 16.0
	marker_2.scale.z = 0.1
	marker_2.color=ColorRGBA(0.851, 0.533, 0.502, 0.8)
	marker_2.lifetime=rospy.Duration()
	marker_pub_2.publish(marker_2)

def odom_cb3(data):
	# rospy.loginfo("x-position of robot3: %s; y_position of robot3: %s",data.pose.pose.position.x,data.pose.pose.position.y)
	global path_3
	path_3.header = data.header
	# path_3.header.stamp = rospy.get_time()
	pose = PoseStamped()
	pose.header = data.header 
	pose.pose = data.pose.pose
	path_3.poses.append(pose)
	path_pub_3.publish(path_3)

	global marker_3
	marker_3.header = data.header
	# marker_3.header.stamp = rospy.get_time()
	# marker_3.id=2
	marker_3.type = Marker.CUBE
	marker_3.pose.position = data.pose.pose.position
	marker_3.pose.position.z  = 0.3
	marker_3.scale.x = 24.0
	marker_3.scale.y = 16.0
	marker_3.scale.z = 0.1
	marker_3.color=ColorRGBA(0.0, 1.0, 1.0, 0.8)
	marker_3.lifetime=rospy.Duration()
	marker_pub_3.publish(marker_3)


#robot4 is yellow 
def odom_cb4(data):
	# rospy.loginfo("x-position of robot4: %s; y_position of robot4: %s",data.pose.pose.position.x,data.pose.pose.position.y)
	global path_4
	path_4.header = data.header
	# path_4.header.stamp = rospy.get_time()
	pose = PoseStamped()
	pose.header = data.header 
	pose.pose = data.pose.pose
	path_4.poses.append(pose)
	path_pub_4.publish(path_4)

	global marker_4 
	marker_4.header = data.header
	# marker_4.header.stamp = rospy.get_time()
	# marker_4.id=3
	marker_4.type = Marker.CUBE
	marker_4.pose.position = data.pose.pose.position
	marker_4.pose.position.z  = 0.3
	marker_4.scale.x = 24.0
	marker_4.scale.y = 16.0
	marker_4.scale.z = 0.1
	marker_4.color=ColorRGBA(1.0, 0.435, 0.298, 0.8)
	marker_4.lifetime=rospy.Duration()
	marker_pub_4.publish(marker_4)
#robot 5 is pink 
def odom_cb5(data):
	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
	global path_5
	path_5.header = data.header
	# path_5.header.stamp = rospy.get_time()
	pose = PoseStamped()
	pose.header = data.header 
	pose.pose = data.pose.pose
	path_5.poses.append(pose)
	path_pub_5.publish(path_5)

	global marker_5 
	marker_5.header = data.header
	# marker_5.header.stamp = rospy.get_time()
	# marker_5.id=4
	marker_5.type = Marker.CUBE
	marker_5.pose.position = data.pose.pose.position
	marker_5.pose.position.z  = 0.3
	marker_5.scale.x = 24.0
	marker_5.scale.y = 16.0
	marker_5.scale.z = 0.1
	marker_5.color=ColorRGBA(1.0, 0.921, 0.216, 0.8)
	marker_5.lifetime=rospy.Duration()
	marker_pub_5.publish(marker_5)

# def odom_cb6(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_6
# 	path_6.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_6.poses.append(pose)
# 	path_pub_6.publish(path_6)

# 	global marker_6 
# 	marker_6.header = data.header
# 	marker_6.type = Marker.CUBE
# 	marker_6.pose.position = data.pose.pose.position
# 	marker_6.pose.position.z  = 0.3
# 	marker_6.scale.x = 24.0
# 	marker_6.scale.y = 16.0
# 	marker_6.scale.z = 0.1
# 	marker_6.color=ColorRGBA(0.8, 0.623, 0.149, 0.8)
# 	# marker_6.color=ColorRGBA(1.0, 0.0, 0.0, 0.8)

# 	marker_6.lifetime=rospy.Duration()
# 	marker_pub_6.publish(marker_6)

# def odom_cb7(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_7
# 	path_7.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_7.poses.append(pose)
# 	path_pub_7.publish(path_7)

# 	global marker_7 
# 	marker_7.header = data.header
# 	marker_7.type = Marker.CUBE
# 	marker_7.pose.position = data.pose.pose.position
# 	marker_7.pose.position.z  = 0.3
# 	marker_7.scale.x = 24.0
# 	marker_7.scale.y = 16.0
# 	marker_7.scale.z = 0.1
# 	marker_7.color=ColorRGBA(0.82, 0.259, 0.553, 0.8)
# 	marker_7.lifetime=rospy.Duration()
# 	marker_pub_7.publish(marker_7)

# def odom_cb8(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_8
# 	path_8.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_8.poses.append(pose)
# 	path_pub_8.publish(path_8)

# 	global marker_8 
# 	marker_8.header = data.header
# 	marker_8.type = Marker.CUBE
# 	marker_8.pose.position = data.pose.pose.position
# 	marker_8.pose.position.z  = 0.3
# 	marker_8.scale.x = 24.0
# 	marker_8.scale.y = 16.0
# 	marker_8.scale.z = 0.1
# 	marker_8.color=ColorRGBA(0.0784, 0.353, 0.196, 0.8)
# 	marker_8.lifetime=rospy.Duration()
# 	marker_pub_8.publish(marker_8)

# def odom_cb9(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_9
# 	path_9.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_9.poses.append(pose)
# 	path_pub_9.publish(path_9)

# 	global marker_9 
# 	marker_9.header = data.header
# 	marker_9.type = Marker.CUBE
# 	marker_9.pose.position = data.pose.pose.position
# 	marker_9.pose.position.z  = 0.3
# 	marker_9.scale.x = 24.0
# 	marker_9.scale.y = 16.0
# 	marker_9.scale.z = 0.1
# 	marker_9.color=ColorRGBA(0.18, 0.8, 0.443, 0.8)
# 	marker_9.lifetime=rospy.Duration()
# 	marker_pub_9.publish(marker_9)

# def odom_cb10(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_10
# 	path_10.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_10.poses.append(pose)
# 	path_pub_10.publish(path_10)

# 	global marker_10 
# 	marker_10.header = data.header
# 	marker_10.type = Marker.CUBE
# 	marker_10.pose.position = data.pose.pose.position
# 	marker_10.pose.position.z  = 0.3
# 	marker_10.scale.x = 24.0
# 	marker_10.scale.y = 16.0
# 	marker_10.scale.z = 0.1
# 	marker_10.color=ColorRGBA(0.51, 0.878, 0.667, 0.8)
# 	marker_10.lifetime=rospy.Duration()
# 	marker_pub_10.publish(marker_10)

# def odom_cb11(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_11
# 	path_11.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_11.poses.append(pose)
# 	path_pub_11.publish(path_11)

# 	global marker_11 
# 	marker_11.header = data.header
# 	marker_11.type = Marker.CUBE
# 	marker_11.pose.position = data.pose.pose.position
# 	marker_11.pose.position.z  = 0.3
# 	marker_11.scale.x = 24.0
# 	marker_11.scale.y = 16.0
# 	marker_11.scale.z = 0.1
# 	marker_11.color=ColorRGBA(0.0, 1.0, 0.0, 0.5)
# 	marker_11.lifetime=rospy.Duration()
# 	marker_pub_11.publish(marker_11)

# def odom_cb12(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_12
# 	path_12.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_12.poses.append(pose)
# 	path_pub_12.publish(path_12)

# 	global marker_12 
# 	marker_12.header = data.header
# 	marker_12.type = Marker.CUBE
# 	marker_12.pose.position = data.pose.pose.position
# 	marker_12.pose.position.z  = 0.3
# 	marker_12.scale.x = 24.0
# 	marker_12.scale.y = 16.0
# 	marker_12.scale.z = 0.1
# 	marker_12.color=ColorRGBA(0.969, 0.863, 0.435, 0.8)
# 	marker_12.lifetime=rospy.Duration()
# 	marker_pub_12.publish(marker_12)

# def odom_cb13(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_13
# 	path_13.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_13.poses.append(pose)
# 	path_pub_13.publish(path_13)

# 	global marker_13 
# 	marker_13.header = data.header
# 	marker_13.type = Marker.CUBE
# 	marker_13.pose.position = data.pose.pose.position
# 	marker_13.pose.position.z  = 0.3
# 	marker_13.scale.x = 24.0
# 	marker_13.scale.y = 16.0
# 	marker_13.scale.z = 0.1
# 	marker_13.color=ColorRGBA(0.0, 0.0, 1.0, 0.8)
# 	marker_13.lifetime=rospy.Duration()
# 	marker_pub_13.publish(marker_13)

# def odom_cb14(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_14
# 	path_14.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_14.poses.append(pose)
# 	path_pub_14.publish(path_14)

# 	global marker_14 
# 	marker_14.header = data.header
# 	marker_14.type = Marker.CUBE
# 	marker_14.pose.position = data.pose.pose.position
# 	marker_14.pose.position.z  = 0.3
# 	marker_14.scale.x = 24.0
# 	marker_14.scale.y = 16.0
# 	marker_14.scale.z = 0.1
# 	marker_14.color=ColorRGBA(0.102, 0.3216, 0.46275, 0.8)
# 	marker_14.lifetime=rospy.Duration()
# 	marker_pub_14.publish(marker_14)

# def odom_cb15(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_15
# 	path_15.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_15.poses.append(pose)
# 	path_pub_15.publish(path_15)

# 	global marker_15 
# 	marker_15.header = data.header
# 	marker_15.type = Marker.CUBE
# 	marker_15.pose.position = data.pose.pose.position
# 	marker_15.pose.position.z  = 0.3
# 	marker_15.scale.x = 24.0
# 	marker_15.scale.y = 16.0
# 	marker_15.scale.z = 0.1
# 	marker_15.color=ColorRGBA(0.18, 0.525, 0.757, 0.8)
# 	marker_15.lifetime=rospy.Duration()
# 	marker_pub_15.publish(marker_15)

# def odom_cb16(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_16
# 	path_16.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_16.poses.append(pose)
# 	path_pub_16.publish(path_16)

# 	global marker_16 
# 	marker_16.header = data.header
# 	marker_16.type = Marker.CUBE
# 	marker_16.pose.position = data.pose.pose.position
# 	marker_16.pose.position.z  = 0.3
# 	marker_16.scale.x = 24.0
# 	marker_16.scale.y = 16.0
# 	marker_16.scale.z = 0.1
# 	marker_16.color=ColorRGBA(0.522, 0.757, 0.914, 0.8)
# 	marker_16.lifetime=rospy.Duration()
# 	marker_pub_16.publish(marker_16)

# def odom_cb17(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_17
# 	path_17.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_17.poses.append(pose)
# 	path_pub_17.publish(path_17)

# 	global marker_17 
# 	marker_17.header = data.header
# 	marker_17.type = Marker.CUBE
# 	marker_17.pose.position = data.pose.pose.position
# 	marker_17.pose.position.z  = 0.3
# 	marker_17.scale.x = 24.0
# 	marker_17.scale.y = 16.0
# 	marker_17.scale.z = 0.1
# 	marker_17.color=ColorRGBA(0.561, 0.796, 0.141, 0.8)
# 	marker_17.lifetime=rospy.Duration()
# 	marker_pub_17.publish(marker_17)

# def odom_cb18(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_18
# 	path_18.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_18.poses.append(pose)
# 	path_pub_18.publish(path_18)

# 	global marker_18 
# 	marker_18.header = data.header
# 	marker_18.type = Marker.CUBE
# 	marker_18.pose.position = data.pose.pose.position
# 	marker_18.pose.position.z  = 0.3
# 	marker_18.scale.x = 24.0
# 	marker_18.scale.y = 16.0
# 	marker_18.scale.z = 0.1
# 	marker_18.color=ColorRGBA(0.29,0.1370, 0.353, 0.8)
# 	marker_18.lifetime=rospy.Duration()
# 	marker_pub_18.publish(marker_18)

# def odom_cb19(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_19
# 	path_19.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_19.poses.append(pose)
# 	path_pub_19.publish(path_19)

# 	global marker_19 
# 	marker_19.header = data.header
# 	marker_19.type = Marker.CUBE
# 	marker_19.pose.position = data.pose.pose.position
# 	marker_19.pose.position.z  = 0.3
# 	marker_19.scale.x = 24.0
# 	marker_19.scale.y = 16.0
# 	marker_19.scale.z = 0.1
# 	marker_19.color=ColorRGBA(0.557, 0.267, 0.678, 0.8)
# 	marker_19.lifetime=rospy.Duration()
# 	marker_pub_19.publish(marker_19)

# def odom_cb20(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_20
# 	path_20.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_20.poses.append(pose)
# 	path_pub_20.publish(path_20)

# 	global marker_20 
# 	marker_20.header = data.header
# 	marker_20.type = Marker.CUBE
# 	marker_20.pose.position = data.pose.pose.position
# 	marker_20.pose.position.z  = 0.3
# 	marker_20.scale.x = 24.0
# 	marker_20.scale.y = 16.0
# 	marker_20.scale.z = 0.1
# 	marker_20.color=ColorRGBA(0.765, 0.608, 0.827, 0.8)
# 	marker_20.lifetime=rospy.Duration()
# 	marker_pub_20.publish(marker_20)

# def odom_cb21(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_21
# 	path_21.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_21.poses.append(pose)
# 	path_pub_21.publish(path_21)

# 	global marker_21 
# 	marker_21.header = data.header
# 	marker_21.type = Marker.SPHERE
# 	marker_21.pose.position = data.pose.pose.position
# 	marker_21.scale.x = 1.0
# 	marker_21.scale.y = 1.0
# 	marker_21.scale.z = 1.0
# 	marker_21.color=ColorRGBA(0.0, 1.0, 0.0, 0.5)
# 	marker_21.lifetime=rospy.Duration()
# 	marker_pub_21.publish(marker_21)

# def odom_cb22(data):
# 	# rospy.loginfo("x-position of robot5: %s; y_position of robot5: %s",data.pose.pose.position.x,data.pose.pose.position.y)
# 	global path_22
# 	path_22.header = data.header
# 	pose = PoseStamped()
# 	pose.header = data.header 
# 	pose.pose = data.pose.pose
# 	path_22.poses.append(pose)
# 	path_pub_22.publish(path_22)

# 	global marker_22 
# 	marker_22.header = data.header
# 	marker_22.type = Marker.SPHERE
# 	marker_22.pose.position = data.pose.pose.position
# 	marker_22.scale.x = 1.0
# 	marker_22.scale.y = 1.0
# 	marker_22.scale.z = 1.0
# 	marker_22.color=ColorRGBA(0.0, 1.0, 0.0, 0.5)
# 	marker_22.lifetime=rospy.Duration()
# 	marker_pub_22.publish(marker_22)

rospy.init_node('path_node', anonymous=True)


path_pub_1 = rospy.Publisher('/firefly1/path',Path,queue_size = 100)
path_pub_2 = rospy.Publisher('/firefly2/path',Path,queue_size = 100)
path_pub_3 = rospy.Publisher('/firefly3/path',Path,queue_size = 100)
path_pub_4 = rospy.Publisher('/firefly4/path',Path,queue_size = 100)
path_pub_5 = rospy.Publisher('/firefly5/path',Path,queue_size = 100)
# path_pub_6 = rospy.Publisher('/firefly6/path',Path,queue_size = 100)
# path_pub_7 = rospy.Publisher('/firefly7/path',Path,queue_size = 100)
# path_pub_8 = rospy.Publisher('/firefly8/path',Path,queue_size = 100)
# path_pub_9 = rospy.Publisher('/firefly9/path',Path,queue_size = 100)
# path_pub_10 = rospy.Publisher('/firefly10/path',Path,queue_size = 100)
# path_pub_11 = rospy.Publisher('/firefly11/path',Path,queue_size = 100)
# path_pub_12 = rospy.Publisher('/firefly12/path',Path,queue_size = 100)
# path_pub_13 = rospy.Publisher('/firefly13/path',Path,queue_size = 100)
# path_pub_14 = rospy.Publisher('/firefly14/path',Path,queue_size = 100)
# path_pub_15 = rospy.Publisher('/firefly15/path',Path,queue_size = 100)
# path_pub_16 = rospy.Publisher('/firefly16/path',Path,queue_size = 100)
# path_pub_17 = rospy.Publisher('/firefly17/path',Path,queue_size = 100)
# path_pub_18 = rospy.Publisher('/firefly18/path',Path,queue_size = 100)
# path_pub_19 = rospy.Publisher('/firefly19/path',Path,queue_size = 100)
# path_pub_20 = rospy.Publisher('/firefly20/path',Path,queue_size = 100)
# path_pub_21 = rospy.Publisher('/firefly21/path',Path,queue_size = 100)
# path_pub_22 = rospy.Publisher('/firefly22/path',Path,queue_size = 100)




marker_pub_1 = rospy.Publisher('/firefly1/visualization_marker', Marker, queue_size = 10)
marker_pub_2 = rospy.Publisher('/firefly2/visualization_marker', Marker, queue_size = 10)
marker_pub_3 = rospy.Publisher('/firefly3/visualization_marker', Marker, queue_size = 10)
marker_pub_4 = rospy.Publisher('/firefly4/visualization_marker', Marker, queue_size = 10)
marker_pub_5 = rospy.Publisher('/firefly5/visualization_marker', Marker, queue_size = 10)
# marker_pub_6 = rospy.Publisher('/firefly6/visualization_marker', Marker, queue_size = 100)
# marker_pub_7 = rospy.Publisher('/firefly7/visualization_marker', Marker, queue_size = 100)
# marker_pub_8 = rospy.Publisher('/firefly8/visualization_marker', Marker, queue_size = 100)
# marker_pub_9 = rospy.Publisher('/firefly9/visualization_marker', Marker, queue_size = 100)
# marker_pub_10 = rospy.Publisher('/firefly10/visualization_marker', Marker, queue_size = 100)
# marker_pub_11 = rospy.Publisher('/firefly11/visualization_marker', Marker, queue_size = 100)
# marker_pub_12 = rospy.Publisher('/firefly12/visualization_marker', Marker, queue_size = 100)
# marker_pub_13 = rospy.Publisher('/firefly13/visualization_marker', Marker, queue_size = 100)
# marker_pub_14 = rospy.Publisher('/firefly14/visualization_marker', Marker, queue_size = 100)
# marker_pub_15 = rospy.Publisher('/firefly15/visualization_marker', Marker, queue_size = 100)
# marker_pub_16 = rospy.Publisher('/firefly16/visualization_marker', Marker, queue_size = 100)
# marker_pub_17 = rospy.Publisher('/firefly17/visualization_marker', Marker, queue_size = 100)
# marker_pub_18 = rospy.Publisher('/firefly18/visualization_marker', Marker, queue_size = 100)
# marker_pub_19 = rospy.Publisher('/firefly19/visualization_marker', Marker, queue_size = 100)
# marker_pub_20 = rospy.Publisher('/firefly20/visualization_marker', Marker, queue_size = 100)
# marker_pub_21 = rospy.Publisher('/firefly21/visualization_marker', Marker, queue_size = 100)
# marker_pub_22 = rospy.Publisher('/firefly22/visualization_marker', Marker, queue_size = 100)




odom_sub_1 = rospy.Subscriber("/firefly1/odometry_sensor1/odometry", Odometry, odom_cb1, queue_size = 1)
odom_sub_2 = rospy.Subscriber("/firefly2/odometry_sensor1/odometry", Odometry, odom_cb2, queue_size = 1)
odom_sub_3 = rospy.Subscriber("/firefly3/odometry_sensor1/odometry", Odometry, odom_cb3, queue_size = 1)
odom_sub_4 = rospy.Subscriber("/firefly4/odometry_sensor1/odometry", Odometry, odom_cb4, queue_size = 1)
odom_sub_5 = rospy.Subscriber("/firefly5/odometry_sensor1/odometry", Odometry, odom_cb5, queue_size = 1)
# odom_sub_6 = rospy.Subscriber("/firefly6/odometry_sensor1/odometry", Odometry, odom_cb6)
# odom_sub_7 = rospy.Subscriber("/firefly7/odometry_sensor1/odometry", Odometry, odom_cb7)
# odom_sub_8 = rospy.Subscriber("/firefly8/odometry_sensor1/odometry", Odometry, odom_cb8)
# odom_sub_9 = rospy.Subscriber("/firefly9/odometry_sensor1/odometry", Odometry, odom_cb9)
# odom_sub_10 = rospy.Subscriber("/firefly10/odometry_sensor1/odometry", Odometry, odom_cb10)
# odom_sub_11 = rospy.Subscriber("/firefly11/odometry_sensor1/odometry", Odometry, odom_cb11)
# odom_sub_12 = rospy.Subscriber("/firefly12/odometry_sensor1/odometry", Odometry, odom_cb12)
# odom_sub_13 = rospy.Subscriber("/firefly13/odometry_sensor1/odometry", Odometry, odom_cb13)
# odom_sub_14 = rospy.Subscriber("/firefly14/odometry_sensor1/odometry", Odometry, odom_cb14)
# odom_sub_15 = rospy.Subscriber("/firefly15/odometry_sensor1/odometry", Odometry, odom_cb15)
# odom_sub_16 = rospy.Subscriber("/firefly16/odometry_sensor1/odometry", Odometry, odom_cb16)
# odom_sub_17 = rospy.Subscriber("/firefly17/odometry_sensor1/odometry", Odometry, odom_cb17)
# odom_sub_18 = rospy.Subscriber("/firefly18/odometry_sensor1/odometry", Odometry, odom_cb18)
# odom_sub_19 = rospy.Subscriber("/firefly19/odometry_sensor1/odometry", Odometry, odom_cb19)
# odom_sub_20 = rospy.Subscriber("/firefly20/odometry_sensor1/odometry", Odometry, odom_cb20)
# odom_sub_21 = rospy.Subscriber("/firefly21/odometry_sensor1/odometry", Odometry, odom_cb21)
# odom_sub_22 = rospy.Subscriber("/firefly22/odometry_sensor1/odometry", Odometry, odom_cb22)


print("x\nx\nx\nx\nx\nx\nx\nIn markers \nx\nx\nx\nx\nx\nx\nx\n")









if __name__=="__main__":
	
	rospy.spin()
