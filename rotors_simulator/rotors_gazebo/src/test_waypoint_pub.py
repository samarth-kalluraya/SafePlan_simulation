#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import Header
from trajectory_msgs.msg import MultiDOFJointTrajectory, MultiDOFJointTrajectoryPoint
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Transform

firefly_pub = rospy.Publisher('/firefly/command/trajectory',MultiDOFJointTrajectory,queue_size = 5)

traj = MultiDOFJointTrajectory()
traj.header.frame_id = ''
traj.header.stamp = rospy.Time.now()
traj.joint_names = ["base_link"]

desired_pos = Transform()
desired_pos.translation.x = 2
desired_pos.translation.y = 2
desired_pos.translation.z = 4

desired_vel = Twist()

desired_accl = Twist()

point = MultiDOFJointTrajectoryPoint([desired_pos],[desired_vel],[desired_accl],rospy.Duration(1))
traj.points.append(point)
firefly_pub.publish(traj)
