#!/usr/bin/env python
import rospy
import numpy as np
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, Point, Pose2D, Quaternion
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA, Bool, Int32


from kf import kf_update
from workspace import Workspace
from task import Task
from biased_TLRRT_star import generate_NBA, generate_path
from neural_net import generate_nn_output
# from display_landmark import show_landmark1#, show_landmark2

channel_open = True

got_image_1 = False
got_image_2 = False
got_image_3 = False
got_image_4 = False
got_image_5 = False

marker_1 = Marker()
marker_2 = Marker()
marker_3 = Marker()
marker_4 = Marker()
marker_5 = Marker()
marker_6 = Marker()
marker_7 = Marker()
marker_8 = Marker()
marker_9 = Marker()
marker_10 = Marker()
marker_11 = Marker()
marker_12 = Marker()
marker_13 = Marker()
lm_marker_1 = Marker()
lm_marker_2 = Marker()
lm_marker_3 = Marker()
lm_marker_4 = Marker()
lm_marker_5 = Marker()
lm_marker_6 = Marker()
lm_marker_7 = Marker()
lm_marker_8 = Marker()
lm_marker_9 = Marker()
lm_marker_10 = Marker()
lm_marker_11 = Marker()
lm_marker_12 = Marker()
lm_marker_13 = Marker()

rob1_wp_id = 0
rob2_wp_id = 0
rob3_wp_id = 0
rob4_wp_id = 0
rob5_wp_id = 0

print("testing workflow 1")
workspace = Workspace()
workspace.update_covariance_shape()
task=Task()
all_robot_waypoints = []
robot_wp_satsify_AP = []
num_of_classes = workspace.no_of_classes                  

display_target_landmarks = True
sensor_noise_cov = [[0.2, 0], [0, 0.2]]
"""
example of defining the sensor model:
sensor_model = [[P(person|person), 	P(person|car), 	P(person|bike)],
				[P(car|person), 	P(car|car), 	P(car|bike)],
				[P(bike|person),	P(bike|car), 	P(bike|bike)]]
"""
sensor_model = [[0.80, 0.18, 0.02],
				[0.23, 0.75, 0.02],
				[0.06, 0.04, 0.9]]  

buchi, buchi_graph = generate_NBA()

print("testing workflow 2")

def update_landmark_estimates(nn_output):
	global workspace
	for key in nn_output.keys():
		x_estimate = workspace.landmark[key][0]
		cov = workspace.landmark[key][1]
		obs = nn_output[key][1]
		x_estimate, cov = kf_update(cov, x_estimate, obs, sensor_noise_cov)
		workspace.landmark[key][0] = x_estimate
		workspace.landmark[key][1]= cov
		workspace.generate_samples_for_lm(key)
		workspace.update_covariance_shape_for_lm(key)
		

def update_class_distribution(nn_output):
	global workspace
	for key in nn_output.keys():
		pair = key.split('_')  # region-robot pair
		robot_index = int(pair[0][1:]) - 1
		class_id = nn_output[key][0][0] - 1
		cond_prob = np.empty((num_of_classes,), float)
		cond_prob[class_id] = nn_output[key][2][class_id]
		for i in range(num_of_classes):
			if i!=class_id:
				cond_prob[i] = sensor_model[class_id][i]
		workspace.classes[robot_index] = workspace.classes[robot_index]*cond_prob/(workspace.classes[robot_index]*cond_prob).sum()


def get_lm_color(nba_truth, num_of_lm):
    """
    1: neutral
    2: landmark
    3: avoid
    """
    lm_color=np.ones(num_of_lm)
    if nba_truth['truth']!='1':
	    for key in nba_truth['truth'].keys():
	        if nba_truth['truth'][key]==True:
	            pair = key.split('_')
	            lm_color[int(pair[0][1:])-1] = 2
    for key in nba_truth['avoid'].keys():
        for j in range(len(nba_truth['avoid'][key])):
                lm_color[int(nba_truth['avoid'][key][j][0][1:])-1]=3
    for key in nba_truth['avoid_self_loop'].keys():
        for j in range(len(nba_truth['avoid_self_loop'][key])):
                lm_color[int(nba_truth['avoid_self_loop'][key][j][0][1:])-1]=3
    return lm_color


def show_landmark1(data,key_id,position,shape,marker):
	chord1 = shape[0][0]
	chord2 = shape[0][1]
	if chord1>chord2:
		long_chord = chord1
	else:
		long_chord = chord2
	if chord1<0.5:
		chord1=0.5
	if chord2<0.5:
		chord2=0.5
	height = 2/long_chord
	if height>4:
		height = 4

	marker.header = data.header
	marker.type = Marker.CYLINDER
	marker.pose.position.x = position[0]
	marker.pose.position.y = position[1]
	marker.pose.position.z  = height/2
	marker.pose.orientation = Quaternion(0,0,shape[1][0],shape[1][1])

	marker.scale.x = chord1
	marker.scale.y = chord2

	marker.scale.z = height
	marker.color=ColorRGBA(0.013, 0.01, 0.9, 0.8)
	marker.lifetime=rospy.Duration()

def show_landmark_color(data,key_id,marker,lm_color):
	marker.header = data.header
	marker.type = Marker.CYLINDER
	marker.pose.position.x = workspace.landmark[key_id][0][0]
	marker.pose.position.y = workspace.landmark[key_id][0][1]
	marker.pose.position.z  = 0.15
	marker.pose.orientation = Quaternion(0,0,workspace.landmark['l1'][2][1][0],workspace.landmark['l1'][2][1][1])
	if lm_color==1:
		marker.scale.x = 0.01
		marker.scale.y = 0.01
		marker.scale.z = 0.2
		marker.color=ColorRGBA(0.013, 0.01, 0.9, 0.8)
	elif lm_color==2:
		marker.scale.x = 2
		marker.scale.y = 2
		marker.scale.z = 0.2
		marker.color=ColorRGBA(0.013, 0.9, 0.01, 0.8)
	else:
		marker.scale.x = 2
		marker.scale.y = 2
		marker.scale.z = 0.2
		marker.color=ColorRGBA(0.9, 0.01, 0.01, 0.8)
	marker.lifetime=rospy.Duration()

def show_all_landmarks(data):
	show_landmark1(data,'l1', workspace.landmark['l1'][0], workspace.landmark['l1'][2],marker_1)
	marker_pub_1.publish(marker_1)
	show_landmark1(data,'l2', workspace.landmark['l2'][0], workspace.landmark['l2'][2],marker_2)
	marker_pub_2.publish(marker_2)
	show_landmark1(data,'l3', workspace.landmark['l3'][0], workspace.landmark['l3'][2],marker_3)
	marker_pub_3.publish(marker_3)
	show_landmark1(data,'l4', workspace.landmark['l4'][0], workspace.landmark['l4'][2],marker_4)
	marker_pub_4.publish(marker_4)
	show_landmark1(data,'l5', workspace.landmark['l5'][0], workspace.landmark['l5'][2],marker_5)
	marker_pub_5.publish(marker_5)
	show_landmark1(data,'l6', workspace.landmark['l6'][0], workspace.landmark['l6'][2],marker_6)
	marker_pub_6.publish(marker_6)
	show_landmark1(data,'l7', workspace.landmark['l7'][0], workspace.landmark['l7'][2],marker_7)
	marker_pub_7.publish(marker_7)
	show_landmark1(data,'l8', workspace.landmark['l8'][0], workspace.landmark['l8'][2],marker_8)
	marker_pub_8.publish(marker_8)
	show_landmark1(data,'l9', workspace.landmark['l9'][0], workspace.landmark['l9'][2],marker_9)
	marker_pub_9.publish(marker_9)
	show_landmark1(data,'l10', workspace.landmark['l10'][0], workspace.landmark['l10'][2],marker_10)
	marker_pub_10.publish(marker_10)
	show_landmark1(data,'l11', workspace.landmark['l11'][0], workspace.landmark['l11'][2],marker_11)
	marker_pub_11.publish(marker_11)
	show_landmark1(data,'l12', workspace.landmark['l12'][0], workspace.landmark['l12'][2],marker_12)
	marker_pub_12.publish(marker_12)
	show_landmark1(data,'l13', workspace.landmark['l13'][0], workspace.landmark['l13'][2],marker_13)
	marker_pub_13.publish(marker_13)
	number_of_landmarks = 13

	if not isinstance(rob1_wp_id, int) and display_target_landmarks:
		if rob1_wp_id.data < len(all_robot_waypoints[0]):
			lm_color = get_lm_color(buchi_graph.edges[(all_robot_waypoints[0][rob1_wp_id.data][2:])], number_of_landmarks)
			show_landmark_color(data,'l1',lm_marker_1,lm_color[0])
			lm_marker_pub_1.publish(lm_marker_1)
			show_landmark_color(data,'l2',lm_marker_2,lm_color[1])
			lm_marker_pub_2.publish(lm_marker_2)
			show_landmark_color(data,'l3',lm_marker_3,lm_color[2])
			lm_marker_pub_3.publish(lm_marker_3)
			show_landmark_color(data,'l4',lm_marker_4,lm_color[3])
			lm_marker_pub_4.publish(lm_marker_4)
			show_landmark_color(data,'l5',lm_marker_5,lm_color[4])
			lm_marker_pub_5.publish(lm_marker_5)
			show_landmark_color(data,'l6',lm_marker_6,lm_color[5])
			lm_marker_pub_6.publish(lm_marker_6)
			show_landmark_color(data,'l7',lm_marker_7,lm_color[6])
			lm_marker_pub_7.publish(lm_marker_7)
			show_landmark_color(data,'l8',lm_marker_8,lm_color[7])
			lm_marker_pub_8.publish(lm_marker_8)
			show_landmark_color(data,'l9',lm_marker_9,lm_color[8])
			lm_marker_pub_9.publish(lm_marker_9)
			show_landmark_color(data,'l10',lm_marker_10,lm_color[9])
			lm_marker_pub_10.publish(lm_marker_10)
			show_landmark_color(data,'l11',lm_marker_11,lm_color[10])
			lm_marker_pub_11.publish(lm_marker_11)
			show_landmark_color(data,'l12',lm_marker_12,lm_color[11])
			lm_marker_pub_12.publish(lm_marker_12)
			show_landmark_color(data,'l13',lm_marker_13,lm_color[12])
			lm_marker_pub_13.publish(lm_marker_13)

# def show_landmark2(data,key_id,shape):
# 	global marker_2 
# 	marker_2.header = data.header
# 	marker_2.type = Marker.CYLINDER
# 	marker_2.pose.position.x = workspace.landmark[key_id][0][0]
# 	marker_2.pose.position.y = workspace.landmark[key_id][0][1]
# 	marker_2.pose.position.z  = 1
# 	marker_2.scale.x = 0.50
# 	marker_2.scale.y = 0.50
# 	marker_2.scale.z = 4
# 	marker_2.color=ColorRGBA(0.013, 0.01, 0.9, 0.8)
# 	marker_2.lifetime=rospy.Duration()
# 	marker_pub_2.publish(marker_2)

def publish_path_status(is_path_ready):
	path_ready_pub1.publish(is_path_ready)
	path_ready_pub2.publish(is_path_ready)
	path_ready_pub3.publish(is_path_ready)
	path_ready_pub4.publish(is_path_ready)
	path_ready_pub5.publish(is_path_ready)


def get_curr_rob_states(wp_id):
    init=[]
    pos=[]
    for i in range(buchi.number_of_robots):
        pos.append(tuple(all_robot_waypoints[i][wp_id][:2]))
    init.append(tuple(pos))
    init.append(all_robot_waypoints[0][wp_id][2])
    return tuple(init)


def detect_in_vid1(data):
	global got_image_1
	got_image_1 = True

def detect_in_vid2(data):
	global got_image_2
	got_image_2 = True

def detect_in_vid3(data):
	global got_image_3
	got_image_3 = True
	
def detect_in_vid4(data):
	global got_image_4
	got_image_4 = True
	
def detect_in_vid5(data):
	global got_image_5
	got_image_5 = True

  
def odom_cb1(data):
	global got_image_1
	global workspace
	# print(rob1_wp_id)
	global channel_open
	# print("channel status in 1:", channel_open)
	if channel_open:
		channel_open = False
		if got_image_1:
			nn_output = generate_nn_output(data)
			got_image_1 = False
			update_landmark_estimates(nn_output)
			update_class_distribution(nn_output)
			show_all_landmarks(data)
			if nn_output:
				global all_robot_waypoints
				global robot_wp_satsify_AP
				
				if rob1_wp_id.data < len(all_robot_waypoints[0]):
					rob_waypoint = all_robot_waypoints[0][rob1_wp_id.data]
					next_rob_waypoint = []
					for i in range(buchi.number_of_robots):
						next_rob_waypoint.append(all_robot_waypoints[i][rob1_wp_id.data+1:rob1_wp_id.data+10])

					replanning_bool = task.Replanning_check(rob_waypoint, next_rob_waypoint, workspace, robot_wp_satsify_AP, 1, buchi_graph)
					if replanning_bool:
						is_path_ready = False
						publish_path_status(is_path_ready)
					
						print("\n*\n*\nCalculating path\n*\n*\n")
						init_state = get_curr_rob_states(rob1_wp_id.data)
						all_robot_waypoints,robot_wp_satsify_AP = generate_path(buchi, buchi_graph, workspace, init_state, save_waypoints = True, edit_launch_file=False, save_covariances = False)
						print("\n Calculated path from cb 1\n")

						print("\n set path ready true\n")
						
						is_path_ready = True
						publish_path_status(is_path_ready)
		channel_open = True
		# print("exit channel operation 1")




# 2
def odom_cb2(data):
	global got_image_2
	global channel_open
	# print("channel status in 2:", channel_open)
	if channel_open:
		channel_open = False
		if got_image_2:	
			nn_output = generate_nn_output(data)
			got_image_2 = False
			update_landmark_estimates(nn_output)
			update_class_distribution(nn_output)
			show_all_landmarks(data)
			if nn_output:
				global all_robot_waypoints
				global robot_wp_satsify_AP
				
				if rob2_wp_id.data < len(all_robot_waypoints[0]):
					rob_waypoint = all_robot_waypoints[0][rob2_wp_id.data]
					next_rob_waypoint = []
					for i in range(buchi.number_of_robots):
						next_rob_waypoint.append(all_robot_waypoints[i][rob2_wp_id.data+1:rob2_wp_id.data+10])
					replanning_bool = task.Replanning_check(rob_waypoint, next_rob_waypoint, workspace, robot_wp_satsify_AP, 2, buchi_graph)
					if replanning_bool:
						is_path_ready = False
						publish_path_status(is_path_ready)
					
						print("\n*\n*\nCalculating path\n*\n*\n")
						init_state = get_curr_rob_states(rob2_wp_id.data)
						all_robot_waypoints,robot_wp_satsify_AP = generate_path(buchi, buchi_graph, workspace, init_state, save_waypoints = True, edit_launch_file=False, save_covariances = False)
						print("\n Calculated path from cb 2\n")

						print("\n set path ready true\n")
						
						is_path_ready = True
						publish_path_status(is_path_ready)
		channel_open = True
		# print("exit channel operation 2")


# 3
def odom_cb3(data):
	global got_image_3
	global channel_open
	# print("channel status in 3:", channel_open)
	if channel_open:
		channel_open = False
		if got_image_3:
			nn_output = generate_nn_output(data)
			got_image_3 = False
			update_landmark_estimates(nn_output)
			update_class_distribution(nn_output)
			show_all_landmarks(data)
			if nn_output:
				global all_robot_waypoints
				global robot_wp_satsify_AP
				
				if rob3_wp_id.data < len(all_robot_waypoints[0]):
					rob_waypoint = all_robot_waypoints[0][rob3_wp_id.data]
					next_rob_waypoint = []
					for i in range(buchi.number_of_robots):
						next_rob_waypoint.append(all_robot_waypoints[i][rob3_wp_id.data+1:rob3_wp_id.data+10])
				
					replanning_bool = task.Replanning_check(rob_waypoint, next_rob_waypoint, workspace, robot_wp_satsify_AP, 3, buchi_graph)
					if replanning_bool:
						is_path_ready = False
						publish_path_status(is_path_ready)
					
						print("\n*\n*\nCalculating path\n*\n*\n")
						init_state = get_curr_rob_states(rob3_wp_id.data)
						all_robot_waypoints,robot_wp_satsify_AP = generate_path(buchi, buchi_graph, workspace, init_state, save_waypoints = True, edit_launch_file=False, save_covariances = False)
						print("\n Calculated path from cb 3\n")

						print("\n set path ready true\n")
						
						is_path_ready = True
						publish_path_status(is_path_ready)
		channel_open = True
		# print("exit channel operation 3")

# 4
def odom_cb4(data):
	global got_image_4
	global channel_open
	# print("channel status in 4:", channel_open)
	if channel_open:
		channel_open = False
		if got_image_4:
			nn_output = generate_nn_output(data)
			got_image_4 = False
			update_landmark_estimates(nn_output)
			update_class_distribution(nn_output)
			show_all_landmarks(data)
			if nn_output:
				global all_robot_waypoints
				global robot_wp_satsify_AP
				
				if rob4_wp_id.data < len(all_robot_waypoints[0]):
					rob_waypoint = all_robot_waypoints[0][rob4_wp_id.data]
					next_rob_waypoint = []
					for i in range(buchi.number_of_robots):
						next_rob_waypoint.append(all_robot_waypoints[i][rob4_wp_id.data+1:rob4_wp_id.data+10])
					
					replanning_bool = task.Replanning_check(rob_waypoint, next_rob_waypoint, workspace, robot_wp_satsify_AP, 4, buchi_graph)
					if replanning_bool:
						is_path_ready = False
						publish_path_status(is_path_ready)
					
						print("\n*\n*\nCalculating path\n*\n*\n")
						init_state = get_curr_rob_states(rob4_wp_id.data)
						all_robot_waypoints,robot_wp_satsify_AP = generate_path(buchi, buchi_graph, workspace, init_state, save_waypoints = True, edit_launch_file=False, save_covariances = False)
						print("\n Calculated path from cb 4\n")

						print("\n set path ready true\n")
						
						is_path_ready = True
						publish_path_status(is_path_ready)
		channel_open = True
		# print("exit channel operation 4")

# 5
def odom_cb5(data):
	global got_image_5
	global channel_open
	# print("channel status in 5:", channel_open)
	if channel_open:
		channel_open = False
		if got_image_5:	
			nn_output = generate_nn_output(data)
			got_image_5 = False
			update_landmark_estimates(nn_output)
			update_class_distribution(nn_output)
			show_all_landmarks(data)
			if nn_output:
				global all_robot_waypoints
				global robot_wp_satsify_AP
				
				if rob5_wp_id.data < len(all_robot_waypoints[0]):
					rob_waypoint = all_robot_waypoints[0][rob5_wp_id.data]
					next_rob_waypoint = []
					for i in range(buchi.number_of_robots):
						next_rob_waypoint.append(all_robot_waypoints[i][rob5_wp_id.data+1:rob5_wp_id.data+10])
					
					replanning_bool = task.Replanning_check(rob_waypoint, next_rob_waypoint, workspace, robot_wp_satsify_AP, 5, buchi_graph)
					if replanning_bool:
						is_path_ready = False
						publish_path_status(is_path_ready)
					
						print("\n*\n*\nCalculating path\n*\n*\n")
						init_state = get_curr_rob_states(rob5_wp_id.data)
						all_robot_waypoints,robot_wp_satsify_AP = generate_path(buchi, buchi_graph, workspace, init_state, save_waypoints = True, edit_launch_file=False, save_covariances = False)
						print("\n Calculated path from cb 5\n")

						print("\n set path ready true\n")
						
						is_path_ready = True
						publish_path_status(is_path_ready)
		channel_open = True
		# print("exit channel operation 5")



def wp_id_cb1(data):
	global rob1_wp_id
	rob1_wp_id = data
	# print("firefly 1: ",rob1_wp_id.data)

def wp_id_cb2(data):
	global rob2_wp_id
	rob2_wp_id = data
	# print("firefly 2: ",rob2_wp_id.data)

def wp_id_cb3(data):
	global rob3_wp_id
	rob3_wp_id = data
	# print("firefly 3: ",rob3_wp_id.data)	

def wp_id_cb4(data):
	global rob4_wp_id
	rob4_wp_id = data
	# print("firefly 4: ",rob4_wp_id.data)

def wp_id_cb5(data):
	global rob5_wp_id
	rob5_wp_id = data
	# print("firefly 5: ",rob5_wp_id.data)






if __name__=="__main__":
	print("testing workflow 3")


	rospy.init_node('neural_network', anonymous=True)

	path_ready_pub1 = rospy.Publisher('/firefly1/path_ready', Bool, queue_size=10)
	path_ready_pub2 = rospy.Publisher('/firefly2/path_ready', Bool, queue_size=10)
	path_ready_pub3 = rospy.Publisher('/firefly3/path_ready', Bool, queue_size=10)
	path_ready_pub4 = rospy.Publisher('/firefly4/path_ready', Bool, queue_size=10)
	path_ready_pub5 = rospy.Publisher('/firefly5/path_ready', Bool, queue_size=10)
	is_path_ready = False
	# path_ready_pub1.publish(is_path_ready)
	# path_ready_pub2.publish(is_path_ready)
	# path_ready_pub3.publish(is_path_ready)
	# path_ready_pub4.publish(is_path_ready)
	# path_ready_pub5.publish(is_path_ready)
	publish_path_status(is_path_ready)


	init_state = (task.init, buchi_graph.graph['init'][0])
	all_robot_waypoints,robot_wp_satsify_AP = generate_path(buchi, buchi_graph, workspace, init_state, save_waypoints = True, edit_launch_file=True, save_covariances = False)

	# marker_pub_1 = rospy.Publisher('/target1/cov/visualization_marker', Marker, queue_size = 10)
	# marker_pub_2 = rospy.Publisher('/target1/cov/visualization_marker', Marker, queue_size = 10)
	# marker_pub_3 = rospy.Publisher('/firefly3/camera/visualization_marker', Marker, queue_size = 10)
	# marker_pub_4 = rospy.Publisher('/firefly4/camera/visualization_marker', Marker, queue_size = 10)
	# marker_pub_5 = rospy.Publisher('/firefly5/camera/visualization_marker', Marker, queue_size = 10)
	marker_pub_1 = rospy.Publisher('/target1/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_2 = rospy.Publisher('/target2/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_3 = rospy.Publisher('/target3/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_4 = rospy.Publisher('/target4/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_5 = rospy.Publisher('/target5/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_6 = rospy.Publisher('/target6/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_7 = rospy.Publisher('/target7/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_8 = rospy.Publisher('/target8/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_9 = rospy.Publisher('/target9/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_10 = rospy.Publisher('/target10/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_11 = rospy.Publisher('/target11/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_12 = rospy.Publisher('/target12/cov/visualization_marker', Marker, queue_size = 10)
	marker_pub_13 = rospy.Publisher('/target13/cov/visualization_marker', Marker, queue_size = 10)

	lm_marker_pub_1 = rospy.Publisher('/target1/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_2 = rospy.Publisher('/target2/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_3 = rospy.Publisher('/target3/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_4 = rospy.Publisher('/target4/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_5 = rospy.Publisher('/target5/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_6 = rospy.Publisher('/target6/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_7 = rospy.Publisher('/target7/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_8 = rospy.Publisher('/target8/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_9 = rospy.Publisher('/target9/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_10 = rospy.Publisher('/target10/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_11 = rospy.Publisher('/target11/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_12 = rospy.Publisher('/target12/state/visualization_marker', Marker, queue_size = 10)
	lm_marker_pub_13 = rospy.Publisher('/target13/state/visualization_marker', Marker, queue_size = 10)	


	vid_sub_1 = rospy.Subscriber("/firefly1/vi_sensor/left/image_raw", Image, detect_in_vid1, queue_size = 1)
	vid_sub_2 = rospy.Subscriber("/firefly2/vi_sensor/left/image_raw", Image, detect_in_vid2, queue_size = 1)
	vid_sub_3 = rospy.Subscriber("/firefly3/vi_sensor/left/image_raw", Image, detect_in_vid3, queue_size = 1)
	vid_sub_4 = rospy.Subscriber("/firefly4/vi_sensor/left/image_raw", Image, detect_in_vid4, queue_size = 1)
	vid_sub_5 = rospy.Subscriber("/firefly5/vi_sensor/left/image_raw", Image, detect_in_vid5, queue_size = 1)

	odom_sub_1 = rospy.Subscriber("/firefly1/odometry_sensor1/odometry", Odometry, odom_cb1, queue_size = 1)
	odom_sub_2 = rospy.Subscriber("/firefly2/odometry_sensor1/odometry", Odometry, odom_cb2, queue_size = 1)
	odom_sub_3 = rospy.Subscriber("/firefly3/odometry_sensor1/odometry", Odometry, odom_cb3, queue_size = 1)
	odom_sub_4 = rospy.Subscriber("/firefly4/odometry_sensor1/odometry", Odometry, odom_cb4, queue_size = 1)
	odom_sub_5 = rospy.Subscriber("/firefly5/odometry_sensor1/odometry", Odometry, odom_cb5, queue_size = 1)

	wp_id_sub_1 = rospy.Subscriber("/firefly1/current_waypoint_id", Int32, wp_id_cb1, queue_size = 1)
	wp_id_sub_2 = rospy.Subscriber("/firefly2/current_waypoint_id", Int32, wp_id_cb2, queue_size = 1)
	wp_id_sub_3 = rospy.Subscriber("/firefly3/current_waypoint_id", Int32, wp_id_cb3, queue_size = 1)
	wp_id_sub_4 = rospy.Subscriber("/firefly4/current_waypoint_id", Int32, wp_id_cb4, queue_size = 1)
	wp_id_sub_5 = rospy.Subscriber("/firefly5/current_waypoint_id", Int32, wp_id_cb5, queue_size = 1)


	print("x\nx\nx\nx\nx\nx\nx\nIn nn sim \nx\nx\nx\nx\nx\nx\nx\n")
	# d = rospy.Duration(3, 0)
	# rospy.sleep(d)
	print("x\nx\nx\nx\nx 30 sec sleep done \nx\nx\nx\n")
	

	is_path_ready = True
	# path_ready_pub1.publish(is_path_ready)
	# path_ready_pub2.publish(is_path_ready)
	# path_ready_pub3.publish(is_path_ready)
	# path_ready_pub4.publish(is_path_ready)
	# path_ready_pub5.publish(is_path_ready)
	publish_path_status(is_path_ready)







	rospy.spin()
