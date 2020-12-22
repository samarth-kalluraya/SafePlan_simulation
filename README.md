# SafePlan simulation
The solution of the TL-RRT* program [biased_TLRRT_star.py](/biased_TLRRT_star.py) can be visualized in the simulation environment. This simulation 
uses the RotorS ROS package [RotorS](https://github.com/ethz-asl/rotors_simulator) which is a MAV gazebo simulator and the BebopS ROS package 
[BebopS](https://github.com/gsilano/BebopS), which is an extension of the ROS package RotorS.

Installation Instructions - Ubuntu 18.04 with ROS Melodic and Gazebo 9
---------------------------------------------------------
To use the code developed and stored in this repository some preliminary actions are needed. They are listed below.

1. Install and initialize ROS Melodic desktop full, additional ROS packages, catkin-tools, and wstool:

```console
$ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
$ sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
$ sudo apt update
$ sudo apt install ros-melodic-desktop-full ros-melodic-joy ros-melodic-octomap-ros ros-melodic-mavlink
$ sudo apt install python-wstool python-catkin-tools protobuf-compiler libgoogle-glog-dev ros-melodic-control-toolbox
$ sudo rosdep init
$ rosdep update
$ echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
$ sudo apt install python-rosinstall python-rosinstall-generator build-essential
```

2. If you don't have ROS workspace yet you can do so by

```console
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/src
$ catkin_init_workspace  # initialize your catkin workspace
$ cd ~/catkin_ws/
$ catkin init
$ cd ~/catkin_ws/src
$ git clone my repo													
$ cd ~/catkin_ws
```

3. Build your workspace with `python_catkin_tools` (therefore you need `python_catkin_tools`)

```console
$ rosdep install --from-paths src -i
$ catkin build
```

4. Add sourcing to your `.bashrc` file

```console
$ echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
```

5. Update the pre-installed Gazebo version. This fix the issue with the `error in REST request for accessing api.ignition.org`

```console
$ sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
$ wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
$ sudo apt update
$ sudo apt install gazebo9 gazebo9-* ros-melodic-gazebo-*
$ sudo apt upgrade
```

> In the event that the simulation does not start, the problem may be related to Gazebo and missing packages. Therefore, run the following commands. 
```console
$ sudo apt-get remove ros-melodic-gazebo* gazebo*
$ sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
$ wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install gazebo9 gazebo9-* ros-melodic-gazebo-*
$ sudo apt upgrade
```

## Additional requirements
* [gazebo2rviz](https://github.com/andreasBihlmaier/gazebo2rviz)
* [pysdf](https://github.com/andreasBihlmaier/pysdf.git)

# Usage
## Structures
* Class [Task](task.py) defines the task specified in LTL
* Class [Workspace](workspace.py) define the workspace where robots reside
* Class [Landmark](workspace.py) define the landmarks in the workspace
* Class [Buchi](buchi_parse.py) constructs the graph of NBA from LTL formula
* Class [Geodesic](geodesic_path.py) constructs geodesic path for given environment
* Class [BiasedTree](biased_tree.py) involves the initialization of the tree and relevant operations
* Function [construction_biased_tree](construct_biased_tree.py) incrementally grow the tree
* Script [biased_TLRRT_star.py](biased_TLRRT_star.py) contains the main function
* Functions [path_plot](draw_picture.py) and [path_print](draw_picture.py) draw and print the paths, respectively
* Functions [export_disc_to_txt](draw_picture.py) and [export_cov_to_txt](draw_picture.py) export discretized waypoints and covariance at waypoints, respectively
* Functions [kf_update](kf.py) and [ekf_update](ekf.py) update position and cavariance using kalman filter and extended kalman filter respectively

## Basic procedure
* First, in the class [Workspace](/workspace.py) specify the size of the workspace, the layout of landmarks and obstacles, and the covariance associated with each landmark. Also specify the number of classes and the class distribution.
* Then, specify the LTL task in the class [Task](task.py), which mainly involves the assigned task, the number of robots, the initial locations of robots and the minimum distance between any pair of robots, and workspace in the class [Workspace](/workspace.py) that contains the information about the size of the workspace, the layout of regions and obstacles. If manual initiation is set to False, then the robots will be initated at random locations. 
* Set the parameters used in the TL-RRT* in the script [biased_tree.py](/biased_tree.py), such as the maximum number of iterations, the step size, sensor range, sensor noise. 
* Specify location of folder where the waypoints should be saved (resources folder in the rotors_gazebo package).


Basic Usage of simulation
---------------------------------------------------------

Running the simulation is quite simple, so as customizing it: it is enough to run in a terminal the command

```console
$ roslaunch rotors_gazebo ltl_sim.launch 
```
> **Note** For the first run you will need to update the starting positions of the robots in the launch file. This position should be the same starting positions as mentioned in the LTL task in the class [Task](scripts/task.py). Alternatively if you run the program [biased_TLRRT_star.py](scripts/biased_TLRRT_star.py) from the terminal before launching the simulation, the launch file will be automatically updated.

The ltl_sim.launch file  launches a gazebo environment and an RViz environment. Once the Gazebo environment is unpaused, run the following line in the terminal.
```console
$ rosrun rotors_gazebo online_planner.py 
```
The [online_planner.py](scripts/online_planner.py) file is used to calculate the path of the robots. It uses the feedback of the cameras mounted on each of the drones to update the estimates of the landmarks. It then determines if replanning is necessary to satisfy the LTL condition.

### User-defined
* User can replace the [generate_nn_output](scripts/neural_net.py) function with their neural network. The output of this network is used to update the landmark estimates and class distributions. User can also change the [update_landmark_estimates](scripts/online_planner.py) and the [update_class_distribution](scripts/online_planner.py) functions as per requirement. The current fucntions use a kalman filter and a bayes filter respectively to update the probability distributions. 
* User can use any Gazebo world as per requirement. If a new world is used update the landmark estimates and class distributions in the class [Workspace](scripts/workspace.py)







