/*
 * Copyright 2015 Fadri Furrer, ASL, ETH Zurich, Switzerland
 * Copyright 2015 Michael Burri, ASL, ETH Zurich, Switzerland
 * Copyright 2015 Mina Kamel, ASL, ETH Zurich, Switzerland
 * Copyright 2015 Janosch Nikolic, ASL, ETH Zurich, Switzerland
 * Copyright 2015 Markus Achtelik, ASL, ETH Zurich, Switzerland
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <fstream>
#include <iostream>
#include <thread>
#include <chrono>
#include <string>

#include <Eigen/Geometry>
#include <mav_msgs/conversions.h>
#include <mav_msgs/default_topics.h>
#include <mav_msgs/eigen_mav_msgs.h>
#include <ros/ros.h>
#include <sensor_msgs/Imu.h>
#include <std_srvs/Empty.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>
#include <trajectory_msgs/MultiDOFJointTrajectory.h>

bool sim_running = false;
bool is_path_ready = false;

static const int64_t kNanoSecondsInSecond = 1000000000;

void callback(const sensor_msgs::ImuPtr& /*msg*/) {
  sim_running = true;
}

void chatterCallback(const std_msgs::Bool::ConstPtr& msg)
{
  is_path_ready = msg->data;
  std::cout<<"\n\n Received path status : ";
  std::cout<<is_path_ready;
  std::cout<<"\n\n";
}

class WaypointWithTime {
 public:
  WaypointWithTime()
      : waiting_time(0),
        position(0, 0, 0),
        yaw(0),
        b_state(""),
        target_b_state("") {
  }

  WaypointWithTime(double t, float x, float y, float z, float _yaw, 
    std::string _b_state, std::string _target_b_state)
      : position(x, y, z), yaw(_yaw), waiting_time(t), b_state(_b_state), target_b_state(_target_b_state) {
  }

  Eigen::Vector3d position;
  double yaw;
  double waiting_time;
  std::string b_state;
  std::string target_b_state;
};

int main(int argc, char** argv) {

  ros::init(argc, argv, "waypoint_publisher");
  ros::NodeHandle nh;
  ROS_INFO("Started waypoint_publisher.");
  
  ros::Subscriber path_sub = nh.subscribe("path_ready", 10, chatterCallback);

  while (!is_path_ready && ros::ok()) {
    std::cout<<"\nwaiting for path. Path status : ";
    std::cout<<is_path_ready;
    ros::spinOnce();
    ros::Duration(0.5).sleep();
  }

  std::cout<<"\n Path ready : ";
  // std::cout<<is_path_ready;


  ros::V_string args;
  ros::removeROSArgs(argc, argv, args);
  if (args.size() != 2 && args.size() != 3) {
    ROS_ERROR("Usage: waypoint_publisher <waypoint_file>"
        "\nThe waypoint file should be structured as: space separated: wait_time [s] x[m] y[m] z[m] yaw[deg])");
    return -1;
  }

  std::vector<WaypointWithTime> waypoints;
  const float DEG_2_RAD = M_PI / 180.0;

  std::ifstream wp_file(args.at(1).c_str());
  if (wp_file.is_open()) {
    double t, x, y, z, yaw;
    std::string b_state, target_b_state;
    // Only read complete waypoints.
    while (wp_file >> t >> x >> y >> z >> yaw >> b_state >> target_b_state) {
      waypoints.push_back(WaypointWithTime(t, x, y, z, yaw * DEG_2_RAD, b_state, target_b_state));
    }
    wp_file.close();
    ROS_INFO("Read %d waypoints.", (int )waypoints.size());
    std::cout<<"\n\n\n\nout of wp reader\n\n\n\n";
  }
  else {
    ROS_ERROR_STREAM("Unable to open poses file: " << args.at(1));
    return -1;
  }

  // The IMU is used, to determine if the simulator is running or not.
  ros::Subscriber sub = nh.subscribe("imu", 10, &callback);

  ros::Publisher wp_pub =
      nh.advertise<trajectory_msgs::MultiDOFJointTrajectory>(
      mav_msgs::default_topics::COMMAND_TRAJECTORY, 10);

  ros::Publisher wp_id_pub =
      nh.advertise<std_msgs::Int32>("current_waypoint_id", 10);
  std_msgs::Int32 wp_count;
  wp_count.data = 0;
  wp_id_pub.publish(wp_count.data);
  
  std_srvs::Empty srv;
  bool unpaused = ros::service::call("/gazebo/unpause_physics", srv);
  unsigned int i = 0;

  ROS_INFO("Wait for simulation to become ready...");

  // while (!sim_running && ros::ok()) {
  //   ros::spinOnce();
  //   // ros::Duration(0.1).sleep();
  // }

  ROS_INFO("...ok");

  // Wait for 3s such that everything can settle and the mav flies to the initial position.
  ros::Duration(3).sleep();

  ROS_INFO("Start publishing waypoints.");

  trajectory_msgs::MultiDOFJointTrajectoryPtr msg(new trajectory_msgs::MultiDOFJointTrajectory);
  msg->header.stamp = ros::Time::now();
  msg->points.resize(waypoints.size());
  msg->joint_names.push_back("base_link");
  int64_t time_from_start_ns = 0;


  bool replanning_done = false;
  for (int i = 0; i < waypoints.size(); ++i) {
        
        while (!is_path_ready && ros::ok()) {
          std::cout<<"\nwaiting for path. Path status : ";
          std::cout<<is_path_ready;
          ros::spinOnce();
          ros::Duration(0.5).sleep();
          i=0;
          wp_count.data = 0;
          replanning_done = true;
        }
        if (replanning_done){
          waypoints.clear();
          std::ifstream wp_file(args.at(1).c_str());
          if (wp_file.is_open()) {
            double t, x, y, z, yaw;
            std::string b_state, target_b_state;
            // Only read complete waypoints.
            while (wp_file >> t >> x >> y >> z >> yaw >> b_state >> target_b_state) {
              waypoints.push_back(WaypointWithTime(t, x, y, z, yaw * DEG_2_RAD, b_state, target_b_state));
            }
            wp_file.close();
            ROS_INFO("Read %d waypoints.", (int )waypoints.size());
          }
          else {
            ROS_ERROR_STREAM("Unable to open poses file: " << args.at(1));
            return -1;
          }
          replanning_done = false;
        }

        trajectory_msgs::MultiDOFJointTrajectory trajectory_msg;
        trajectory_msg.header.stamp = ros::Time::now();
        Eigen::Vector3d desired_position(waypoints[i].position.x(), waypoints[i].position.y(), waypoints[i].position.z());
        double desired_yaw = waypoints[i].yaw;
        mav_msgs::msgMultiDofJointTrajectoryFromPositionYaw(desired_position, desired_yaw, &trajectory_msg);

        double t = waypoints[i].waiting_time;
        std::cout<<"\n waypoint number: "<<i<<"\n";
        wp_pub.publish(trajectory_msg);
        wp_id_pub.publish(wp_count.data);
        wp_count.data = wp_count.data + 1;
        ros::Duration(t).sleep();
        ros::spinOnce();
  }
  ros::spin();
}
