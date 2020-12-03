# -*- coding: utf-8 -*-

from workspace import Workspace, get_label
from random import uniform
import numpy as np
from sympy import Symbol
    

class Task(object):
    """
    define the task specified in LTL
    """
    def __init__(self):
        """
        +----------------------------+
        |   Propositonal Symbols:    |
        |       true, false         |
        |	    any lowercase string |
        |                            |
        |   Boolean operators:       |
        |       !   (negation)       |
        |       ->  (implication)    |
        |       &&  (and)            |
        |       ||  (or)             |
        |                            |
        |   Temporal operators:      |
        |       []  (always)         |
        |       <>  (eventually)     |
        |       U   (until)          |
        +----------------------------+
        """
        workspace = Workspace()
        
        manual_initiation = True
        robot_initial_pos = ((25,80),(10,8),(15,8),(20,8),(25,8))
        robot_initial_angle = [np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708])]
        
        # For subformula it is necessary to have a space between landmark and logical operator 
        # task specification, e_i are subformulas, li_j means the j-th robot is at regions l_i
        '''
        subformula={ AP_id: [a,b,c,d,e]}
        a: condition for AP_id to be True
        b: if 0=> "AND". If "1"=> OR
        c: desired probability
        d: distance from landmark
        e: if 0=> landmark . If "1"=> class
        '''
        
        # --------------------------------- Task 0 -------------------------------------
        # self.formula = '<>e1 && <> ( e2 && <> (e3 && <> e4)) && (!e2 U e5) && []!e6 && []!e7'
        # self.formula = '<>e1 && <> ( e2 && <> e5) && []!e6'
        # self.subformula = {1: ['(l1_1 && l3_2 && l4_3 && l7_4 && l10_5)',0,    0.7,    1.5, 0],
        #                     2: ['(l9_1 && l11_2 && l8_3 && l6_4)',  0,    0.7,    1.5,  0],
        #                     # 3: ['(l8_1 && l7_2 && l6_3)', 0,    0.8,    0.8,  0],
        #                     # 4: ['(l3_1 && l3_2 && l5_3 && l2_5)', 0,    0.7,    0.8,  0],
        #                     5: ['(l8_1 && l7_2 && l2_3 && l12_4 && l12_5)', 0,    0.7,   1.5,  0],
        #                     6: ['(l13_5)', 0,    0.6,    6,  0],                            
        #                     # 7: ['(l7_1 && l4_2  && l7_4)', 0,    0.7,    1,  0]
        #                     }
        # self.number_of_robots = 5
        # --------------------------------- Task 1 -------------------------------------
        # self.formula = '<> ( e1 && <> (e2 && <> (e3 && <> e4))) && []!e5'#&& []!e6'
        # # self.formula = '<> e1 && []!e6'
        # self.subformula = {1: ['(l1_1 && l10_2 && l4_4  && l6_5)',0,0.8,1, 0], # e1 is true if robot in l1
        #                     2: ['(l3_3)',0,0.8,1, 0],
        #                     3: ['(l6_1 && l2_2)',0,0.8,1, 0],
        #                     4: ['(l3_1 && l7_3 && l6_4 && l4_5)',0,0.8,1, 0],
        #                     5: ['(l8_1 || l8_2 || l8_3 || l8_4 || l8_5)',0,0.85,1, 0],
        #                     6: ['(l5_1 || l5_2 || l5_3 || l5_4 || l5_5)',0,0.85,1, 0],
        #                     }
        # self.number_of_robots = 5
        # self.formula = '<>  e1  && []!e5'
        # self.formula = '<> e1 && <>(e2 && <> (e3 && <> e4))'# && []!e5'
       # self.formula = '<>e1 &&  <> ( e2 && <> e3) && []!e5'
       # self.formula = '<> e1 && <> e2 && !e1 U e2 && []!e5'
        # self.subformula = {1: ['(l1_1 && l4_2 && l2_3 && l3_4  && l8_5)',0,0.8,1.5, 0], # e1 is true if robot in l1
        #                     2: ['(l11_1 && l1_2 && l5_3 && l8_4  && l6_5)',0,0.8,1.5, 0],
        #                     3: ['(l9_2 && l8_3 && l6_4  && l10_5)',0,0.8,3, 0],
        #                     4: ['(l12_1 && l12_2 && l12_3 && l12_4  && l12_5)',0,0.8,8, 0],
        #                     5: ['(l13_1 || l13_2 || l13_3 || l13_4 || l13_5)',0,0.85,7, 0],
        #                     6: ['(l4_1 || l4_2 || l4_3 || l4_4 || l4_5)',0,0.85,6, 0],
        #                     }
       # self.subformula = {1: ['(l4_1 && l2_2 && l5_3 && l7_4  && l6_5)',0,0.8,1.5, 0], # e1 is true if robot in l1
       #                      2: ['(l3_1 && l5_2 && l6_3 && l11_4  && l10_5)',0,0.8,1.5, 0],
       #                      # 3: ['(l5_5)',0,0.8,1.5, 0],
       #                      # 4: ['(l4_5)',0,0.8,9, 0],
       #                      5: ['(l13_1 || l13_2 || l13_3 || l13_4 || l13_5)',0,0.85,5, 0]
       #                      # 6: ['(l4_1 || l4_2 || l4_3 || l4_4 || l4_5)',0,0.85,4, 0],
       #                      }
        # self.subformula = {1: ['(l4_1 && l2_2 && l3_3)',0,0.8,1.5, 0], # e1 is true if robot in l1
        #                     2: ['(l5_4  && l6_5)',0,0.8,1.5, 0],
        #                     3: ['(l2_1 && l3_2 && l5_3 && l6_4  && l10_5)',0,0.8,1.5, 0],
        #                     4: ['(l11_5)',0,0.8,9, 0],
        #                     5: ['(l13_1 || l13_2 || l13_3 || l13_4 || l13_5)',0,0.85,7, 0]
        #                     # 6: ['(l4_1 || l4_2 || l4_3 || l4_4 || l4_5)',0,0.85,4, 0],
        #                     }
        # self.number_of_robots = 5
        # self.formula = '<> ( e1 && <> e2)'
        # # self.formula = '<> e1 && []!e6'
        # self.subformula = {1: ['(l1_1 && l5_2)',0,0.8,0.8, 0], # e1 is true if robot in l1
        #                     2: ['(l5_1 && l1_2)',0,0.8,0.8, 0],
        #                     # 3: ['(l5_1 && l6_2)',0,0.5,1, 0],
        #                     # 4: ['(l3_1)',0,0.5,1, 0],
        #                     # 5: ['(l9_1)',0,0.5,1, 0],
        #                     }
        # self.number_of_robots = 2
        # --------------------------------- Task 2 -------------------------------------
        # self.formula = '[] <> e1 && [] <> e3 && !e1 U e2' 
        # self.subformula = {1: ['(l1_1)',0,0.8,1, 0],
        #                     # 2: ['(l6_1)',0,0.8,1, 0], 
        #                     2: ['(c2_1 )',0,0.85,1, 1], 
        #                     # 2: ['((l6_1 || l3_1)&& (l2_2 || l1_2))',0,0.8,1, 0], 
        #                     3: ['(l5_2)',0,0.8,1, 0]
        #                     }
        # self.number_of_robots = 2
        self.formula = '<> e1 && <> e2 && !e3 U e1' 
        self.subformula = {1: ['(l13_1)',0,0.8,1.5, 0],
                            # 2: ['(l6_1)',0,0.8,1, 0], 
                            2: ['(l11_1)',0,0.8,1.5, 0], 
                            # 2: ['((l6_1 || l3_1)&& (l2_2 || l1_2))',0,0.8,1, 0], 
                            3: ['(l11_1)',0,0.8,6, 0]
                            }
        self.number_of_robots = 5
#((l6_1 || l3_1 || l4_1) && (l2_2 || l1_2))
        # --------------------------------- Task 3 -------------------------------------
        # randomly generate tasks
        # num_of_robot_in_one_group = 3
        # group = np.array(range(1, self.number_of_robots + 1))
        # np.random.shuffle(group)
        # group = group.reshape(8, num_of_robot_in_one_group)
        
        # formula = []
        # for i in range(8):
        #     subformula = []
        #     for j in range(num_of_robot_in_one_group):
        #         subformula.append('l' + str(np.random.randint(1, 7)) + '_' + str(group[i][j]))
        #     for j in range(num_of_robot_in_one_group//2):
        #         while True:
        #             g = np.random.randint(7)
        #             robot = group[g][np.random.randint(num_of_robot_in_one_group)]
        #             if robot not in group[i]:
        #                 break
        #         subformula.append('l' + str(np.random.randint(1, 7)) + '_' + str(robot))
        
        #     formula.append('(' + ' && '.join(subformula) + ')')

        # self.subformula = {i: formula[i-1] for i in range(1, 9)}
        # --------------------------------- Task 4 -------------------------------------
        # self.formula = '<> e1 && <> e2 && <> e3 && <>(e4 && <>(e5 && <> e6))'
        # self.subformula = {
        #     1: ['(l1_1 && l1_2)',0,0.6,1, 0],
        #     2: ['(l2_2 && l2_3)',0,0.6,1, 0],
        #     3: ['(l3_3 && l3_4)',0,0.6,1, 0],
        #     4: ['(l4_1)',0,0.6,1, 0],
        #     5: ['(l5_4)',0,0.6,1, 0],
        #     6: ['(l6_3)',0,0.6,1, 0]}
        # self.number_of_robots = 4

        # randomly generate initial locations of robots with empty atomic propositions
        # self.number_of_robots = num_of_robot_in_one_group * 8  # for task 3
        # self.number_of_robots = 1
        if not manual_initiation:
            self.init = []  # initial locations
            self.init_label = []  # labels of initial locations
            self.init_angle = []
            for i in range(self.number_of_robots):
                while True:
                    ini = [round(uniform(0, workspace.workspace[k]), 3) for k in range(len(workspace.workspace))]
                    ap = get_label(ini, workspace)
                    if 'o' not in ap:
                        break
                self.init.append(tuple(ini))
                self.init_angle.append(np.arctan2(workspace.workspace[1]/2-ini[1],workspace.workspace[1]/2-ini[0]))
                # ap = ap + '_' + str(i + 1) if 'l' in ap else ''
                # self.init_label.append(ap)
            self.init = tuple(self.init)          # in the form of ((x, y), (x, y), ...)
            self.init_label = self.get_label_landmark(self.init, workspace)
        else:
            self.init = robot_initial_pos
            self.init_angle = robot_initial_angle
            self.init_label = self.get_label_landmark(self.init, workspace)
            
        self.threshold = 1                # minimum distance between any pair of robots
        
        
    
    def get_label_landmark(self, x, workspace):
        '''
        inputParameters
        ----------
        x : state of all robots
        workspace: object or Workspace class or Landmark class
        
        get labels of robot position satisfied in each AP
        returns {2:['','l6_2']
                 3:[''}]}   --> 
        '''
        AP_labels = {}
        
        for key in self.subformula.keys():
            AP = self.subformula[key][0]
            logic = self.subformula[key][1]     #not needed
            desired_prob = self.subformula[key][2]
            distance = self.subformula[key][3]
            if self.subformula[key][4] == 0:
                # dict storing robot as key and its respective landmark
                robot_index = self.parse_AP(AP)     
                label=[]
                AP_satisfied = False
                count = 0
                for robot_id in range(1, self.number_of_robots+1):
                    if robot_id in robot_index.keys():
                        #check probability and set flag (x[robot_id]), probability, distance workspace, robot_id, landmark)
                        landmark_id = robot_index[robot_id]
                        if self.robot_proximity_check(x[robot_id - 1], desired_prob, distance, workspace, robot_id, landmark_id):
                            label.append('l'+ str(landmark_id) + '_' + str(robot_id))
                            count+=1
                            if logic == 1:
                                AP_satisfied = True
                        else:
                            label.append('')
                    else:
                        label.append('')
                if logic == 0 and count != 0: #If AP is partially satisfied count wont be equal to length of AP
                    AP_satisfied = True
                if AP_satisfied:
                    AP_labels[key]=label
            else:
                robot_index = self.parse_AP(AP) 
                label=[]
                AP_satisfied = False
                count = 0
                for robot_id in range(1, self.number_of_robots+1):
                    if robot_id in robot_index.keys():
                        #check probability and set flag (x[robot_id]), probability, distance workspace, robot_id, landmark)
                        class_id = robot_index[robot_id] 
                        landmark_id = np.argmax(workspace.classes[:,(class_id-1)]) + 1
                        if self.robot_proximity_check(x[robot_id - 1], desired_prob, distance, workspace, robot_id, landmark_id):
                            label.append('c'+ str(class_id) + '_' + str(robot_id))
                            count+=1
                            if logic == 1:
                                AP_satisfied = True
                        else:
                            label.append('')
                    else:
                        label.append('')
                if logic == 0 and count != 0: #If AP is partially satisfied count wont be equal to length of AP
                    AP_satisfied = True
                if AP_satisfied:
                    AP_labels[key]=label
                
        return AP_labels
                
            
                
    def robot_proximity_check(self, x, desired_prob, distance, workspace, robot_id, landmark_id):
        lm_id = landmark_id - 1
        xx1 = workspace.landmark_x[lm_id,:]-x[0]
        yy1 = workspace.landmark_y[lm_id,:]-x[1]
        dist_array = np.sqrt(xx1**2+yy1**2)
        count = (dist_array < distance).sum()
        prob = count / workspace.num_sample_points
        if prob > desired_prob:
            return True
        else:
            return False
        
            
    def parse_AP(self, AP):
        # returns list of landmarks and respective robot indices for a given AP (subformula)
        robot_index={}
        i=0
        while i < len(AP):
            if AP[i]=='l' or AP[i]=='c':
                j=i+1
                while AP[j]!='_':
                    j=j+1
                k=j+1
                while AP[k]!=' ' and AP[k]!=')':
                    k=k+1
                robot_index[int(AP[j+1:k])] = int(AP[i+1:j])
                i=k
            else:
                i+=1
        return robot_index

    def Replanning_check(self, rob_waypoint, next_rob_waypoint, workspace, robot_wp_satsify_AP, robot_id, buchi_graph):
        rob_x = rob_waypoint[0]
        rob_y = rob_waypoint[1]
        rob_state = rob_waypoint[2]
        rob_target_state = rob_waypoint[3]

        needs_replanning = False
        # case 1 ... check if end point of robot_id (referrred from robot_wp_satsify_AP) still satisfy AP for that robot_id
        # find the truth value to reach the next buchi state
        truth = buchi_graph.edges[(rob_state, rob_target_state)]['truth']
        if truth != '1': 
            #find the target for robot_id
            target_lm=""
            for key in truth.keys():
                pair = key.split('_')
                if int(pair[1])==robot_id and truth[key]:
                    target_lm=key
            if target_lm!="":
                pair = target_lm.split('_')
                
                # if target_lm covariance is large then dont replan
                if workspace.landmark[pair[0]][1][0][0] <=0.3 and workspace.landmark[pair[0]][1][1][1] <= 0.3:
                    b_state_count=0
                    for i in range(len(robot_wp_satsify_AP[robot_id-1])):
                        if robot_wp_satsify_AP[robot_id-1][i][2] == rob_state:
                            b_state_count=i+1                
                    satisfying_x = []
                    for i in range(self.number_of_robots):
                        satisfying_x.append(robot_wp_satsify_AP[i][b_state_count][:2])        
                    label = self.get_label_landmark(satisfying_x, workspace)
                    mod_truth={target_lm:True}
                    needs_replanning = not(self.check_transition_b(label, mod_truth))
        if needs_replanning:
            return needs_replanning

        # case 2 ... check if next waypoints of robot_id enter avoid region     
        avoid = buchi_graph.edges[(rob_state, rob_target_state)]['avoid_self_loop']   
        avoid_truth = {}
        if truth != '1':
            for key in truth.keys():
                if truth[key]==False:
                    avoid_truth[key]=False
        for key in avoid.keys():
            for i in range(len(avoid[key])):
                lmid=avoid[key][i][0]+'_'+str(key+1)
                avoid_truth[lmid]=False
        for j in range(len(next_rob_waypoint[0])):           
            next_state=[]
            for i in range(self.number_of_robots):
                next_state.append(next_rob_waypoint[i][j][:2])
            needs_replanning = not(self.check_transition_b(self.get_label_landmark(next_state, workspace), avoid_truth))
            if needs_replanning:
                return needs_replanning
        return needs_replanning     

    def check_transition_b(self, x_label, truth):
        """
        check whether transition enabled with current generated label
        :param x_label: label of the current position
        :param truth: symbol enabling the transition
        :return: true or false
        """
        if truth == '1':
            return True
        # all true propositions should be satisdied
        true_label = [true_label for true_label in truth.keys() if truth[true_label]]
        for label in true_label:
            found = False
            for key in x_label.keys():
                if label in x_label[key]:
                    found =True
            if found==False:
                return False

        #  all fasle propositions should not be satisfied
        false_label = [false_label for false_label in truth.keys() if not truth[false_label]]
        for label in false_label:
            found = False
            for key in x_label.keys():
                if label in x_label[key]:
                    found =True
            if found==True:
                return False
        return True
        
        
        
        
        
        
        
        
        
        
        
        

"""
    def Replanning_check(self, rob_waypoint, workspace, robot_wp_satsify_AP, robot_id, buchi_graph):
        rob_x = rob_waypoint[0]
        rob_y = rob_waypoint[1]
        rob_state = rob_waypoint[2]
        rob_target_state = rob_waypoint[3]

        truth = buchi_graph.edges[(rob_state, rob_target_state)]['truth']
        if truth == '1':
            return False
        
        target_lm=""
        for key in truth.keys():
            pair = key.split('_')
            if int(pair[1])==robot_id and truth[key]:
                target_lm=key
        if target_lm=="":
            return False
        pair = target_lm.split('_')
        if workspace.landmark[pair[0]][1][0][0] >=0.3 and workspace.landmark[pair[0]][1][1][1] >= 0.3:
            return False
        
        #truth
        #{'l5_3': True, 'l6_4': True, 'l10_5': True, 'l2_1': True, 'l3_2': True}
        #now i just need to check if l6_4 is present in label. If it is then I dont need to replan for robot 4. 
        #If it is not there and the covariance of l6 is less than some value, then replan
        
        
        #case 1 ... check if end points still satisfy AP
        b_state_count=0
        for i in range(len(robot_wp_satsify_AP[robot_id-1])):
            if robot_wp_satsify_AP[4][i][2] == rob_state:
                b_state_count=i+1
                
        satisfying_x = []
        for i in range(self.number_of_robots):
            satisfying_x.append(robot_wp_satsify_AP[i][b_state_count][:2])
        
        label = self.get_label_landmark(satisfying_x, workspace)
        
        #this label should be satisfied in         rob_state -->robot_wp_satsify_AP[robot_id][b_state_count][2] for robot_id
        
        #now i just need to 
        mod_truth={target_lm:True}
        needs_replanning = not(self.check_transition_b(label, mod_truth))
        return needs_replanning 
"""        
        
        
        
        
        
        
        
        