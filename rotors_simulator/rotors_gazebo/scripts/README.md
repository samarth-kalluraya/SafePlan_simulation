# SafePlan
SafePlan is an implementation of optimal temporal logic planning for multi-robot systems in uncertain semantic maps [1].
The goal of this planner is to complete collaborative high-level tasks captured by global temporal logic specifications in the presence of uncertainty in the workspace. The workspace is modeled as a semantic map determined by Gaussian distributions over landmark positions and arbitrary  discrete distributions over landmark classes. We extend Linear Temporal Logic by including information-based predicates allowing us to incorporate uncertainty and probabilistic satisfaction requirements directly into the task specification. We propose a new highly scalable sampling-based approach that simultaneously searches the semantic map along with an automaton corresponding to the task and synthesizes paths that satisfy the assigned task specification.

[1] Y. Kantaros and G. J. Pappas, "Optimal Temporal Logic Planning for Multi-Robot Systems in Uncertain Semantic Maps," 2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), Macau, China, 2019, pp. 4127-4132, doi: 10.1109/IROS40897.2019.8968547.

# Requirements
* [Python >=3.6](https://www.python.org/downloads/)
* [sympy](https://www.sympy.org/en/index.html)
* [re]()
* [Pyvisgraph](https://github.com/TaipanRex/pyvisgraph)
* [NetworkX](https://networkx.github.io)
* [Shapely](https://github.com/Toblerity/Shapely)
* [scipy](https://www.scipy.org)
* [matplotlib](https://matplotlib.org)
* [termcolor](https://pypi.org/project/termcolor/)
* [visilibity](https://github.com/tsaoyu/PyVisiLibity)

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
* If the output will be used by the simulation, the specify location of folder where the waypoints should be saved.
* Run [biased_TLRRT_star.py](/biased_TLRRT_star.py) to generate the solution.
* Finally, after the TL-RRT* terminates, the runtime and the cost of the solution are presented. What's more, the path composed of prefix and suffix parts for each robot is drawn with workspace layout when the number of robots is relatively small, otherwise, the path for each robot is printed onto the screen when the number of robots is large. 

# Example

## Workspace
The workspace of size `150 x 150` is shown below, with `l_1`-`l_13` being regions and `o_1`-`o_3` being obstacles
<p align="center">
<img src="img/workspace.png"  width="600" height="600">
</p>

## Test Cases
For all the following test cases, the same set of parameters are used.
```python
# parameters
# maximum number of iterations
n_max = 100000
para = dict()
# lite version, excluding extending and rewiring
para['is_lite'] = True
# step_size used in function near
para['step_size'] = 0.25 * buchi.number_of_robots
# probability used when choosing node q_p_closest
para['p_closest'] = 0.9
# probability used when deciding the target point 
para['y_rand'] = 0.99
# minimum distance between any pair of robots  
para['threshold'] = 1
# Updates landmark covariance when inside sensor range
para['update_covariance'] = True
# sensor range in meters
para['sensor_range'] = 10
# sensor measurement noise
para['sensor_R'] = 0.5
```
Furthermore, the construction of the tree terminates once an accepting node is detected, which is controlled in [construct_biased_tree.py](construct_biased_tree.py) by line
```python
if len(tree.goals): break
```
### Case 1
The task involving one robot is specified by 
```python
self.formula = '<> e1  && <> ( e2 && <> e3) && !e4 U e1' 
self.subformula = {2: ['(l11_1)',0,0.8,1.5, 0],
                    3: ['(l9_1)',0,0.8,1.5, 0], 
                    1: ['(l13_1)',0,0.8,3, 0], 
                    4: ['(l11_1)',0,0.8,5, 0]
                   }
robot_initial_pos = ((25,80),)  # in the form of ((x,y), (x,y), ...)    
```
The output results during execution are
```
Time for the prefix path: 0.0066 min
Cost of path: 228.00000000000003
```
<p align="center">
<img src="img/Case1_Output1.png"  width="250" height="250" title="Robot 1 path">
</p>


### Case 2
The task involving two robots is specified by 
```python
self.formula = '<> e1  && <> e2 && <> e3 && !e3 U e1' 
self.subformula = {1: ['(l9_1)',0,0.8,1.5, 0],
                    2: ['(l12_2)',0,0.8,1.5, 0], 
                    3: ['(l2_1 && l10_2)',0,0.8,3, 0]
                  }
robot_initial_pos = ((25,80),(10,8)  # in the form of ((x,y), (x,y), ...)    
```
The output results during execution are
```
Time for the prefix path: 0.0995 min
Cost of path: 229.45128947213922
```
<p align="center">
<img src="img/Case2_Output1.png"  width="250" height="250" title="Robot 1 path">
<img src="img/Case2_Output2.png"  width="250" height="250" title="Robot 2 path">
</p>


### Case 3
The task involving five robots is specified by 
```python
self.formula = '<>e1 && <> ( e2 && <> e3) && []!e4'
self.subformula = {1: ['(l1_1 && l3_2 && l7_4 && l10_5)',0,    0.7,    1.5, 0],
                    2: ['(l9_1 && l11_2 && l8_3)',  0,    0.7,    1.5,  0],
                    3: ['(l8_1 && l7_2 && l2_3 && l6_4 && l12_5)', 0,    0.7,   1.5,  0],
                    4: ['(l13_1 || l13_2 || l13_3 || l13_4 || l13_5)', 0,    0.7,    5,  0]
                   }
robot_initial_pos = ((25,80),(10,8),(15,8),(20,8),(25,8))
```
The output results during execution are
```
Time for the prefix path: 0.2149 min
Cost of path: 535.7794199619735
```
<p align="center">
<img src="img/Case5_Output1.png"  width="250" height="250" title="Robot 1 path">
<img src="img/Case5_Output2.png"  width="250" height="250" title="Robot 2 path">
<img src="img/Case5_Output3.png"  width="250" height="250" title="Robot 3 path">
</p>
<p align="center">
<img src="img/Case5_Output4.png"  width="250" height="250" title="Robot 4 path">
<img src="img/Case5_Output5.png"  width="250" height="250" title="Robot 5 path">
</p>

