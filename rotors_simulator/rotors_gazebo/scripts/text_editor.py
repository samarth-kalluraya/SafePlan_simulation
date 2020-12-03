#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 13:52:07 2020

@author: samarth
"""

import numpy as np

def export_to_txt(path, number_of_robots, height, waypoint_folder_location, launch_folder_location):
    for robot in range(number_of_robots):    
        # with open(waypoint_folder_location+"/uav"+str(robot+1)+"_test.txt", 'w') as f:
        #     f.write("5 "+str(path[0][1][0][0][robot][0])+" "+str(path[0][1][0][0][robot][1])+" "+str(height)+" 0\n")    
        #     for i in range(1,len(path[0][1])):
        #         # f.write("hello\n")
        #         f.write("0.5 "+str(path[0][1][i][0][robot][0])+" "+str(path[0][1][i][0][robot][1])+" "+str(height)+" 0\n") 
        with open(waypoint_folder_location+"/uav"+str(robot+1)+"_test.txt", 'w') as f:
            f.write("5 "+str(path[0][1][0][0][robot][0])+" "+str(path[0][1][0][0][robot][1])
                    +" "+str(height)+" 0 "+path[0][1][0][1]+"\n")    
            for i in range(1,len(path[0][1])):
                # f.write("hello\n")
                f.write("0.5 "+str(path[0][1][i][0][robot][0])+" "+str(path[0][1][i][0][robot][1])
                        +" "+str(height)+" 0 "+path[0][1][i][1]+"\n")                
        
    a_file = open(launch_folder_location + "/ltl_sim.launch", "r")
    list_of_lines = a_file.readlines()
    j1 = 26
    j2 = 27
    add = 25
    for i in range(number_of_robots):
        list_of_lines[j1-1] = "      <arg name=\"x\" value=\""+str(path[0][1][0][0][i][0])+"\"/>\n"
        list_of_lines[j2-1] = "      <arg name=\"y\" value=\""+str(path[0][1][0][0][i][1])+"\"/>\n"
        j1+=add
        j2+=add
    
    a_file = open(launch_folder_location + "/ltl_sim.launch", "w")
    a_file.writelines(list_of_lines)
    a_file.close()

def export_disc_to_txt(path, targets, number_of_robots, height, waypoint_folder_location, launch_folder_location, discretization = 10, edit_launch_file=True):
    # # b_state_list stores all sequential buchi states of the robot.
    # b_state_list = []
    # b_state_list.append(path[0][1][0][1])
    # for i in range (len(path[0][1])):
    #     if path[0][1][i][1]!=b_state_list[-1]:
    #         b_state_list.append(path[0][1][i][1])
    # b_state_count=1
    
    all_rob_waypoints=[]
    all_rob_wp_satsify_AP=[]

    for robot in range(number_of_robots):    
        with open(waypoint_folder_location+"/uav"+str(robot+1)+"_test.txt", 'w') as f:
            rob_waypoint=[]
            rob_wp_satsify_AP=[]
            for i in range(0,len(path[0][1])):
                if i<len(path[0][1])-1:
                    new_wp = True
                    dx = (path[0][1][i+1][0][robot][0]-path[0][1][i][0][robot][0])/discretization
                    dy = (path[0][1][i+1][0][robot][1]-path[0][1][i][0][robot][1])/discretization
                    for di in range(discretization):
                        if i==0 and di==0:
                            f.write("3 "+str(path[0][1][0][0][robot][0])+" "+str(path[0][1][0][0][robot][1])
                                    +" "+str(height)+" 0 "+path[0][1][0][1]+" "+targets[i]+"\n") 
                            rob_waypoint.append([path[0][1][0][0][robot][0], path[0][1][0][0][robot][1], path[0][1][0][1], targets[i]])
                        else:
                            f.write("0.15 "+str(path[0][1][i][0][robot][0]+dx*di)+" "+str(path[0][1][i][0][robot][1]+dy*di)
                                +" "+str(height)+" 0 "+path[0][1][i][1]+" "+targets[i]+"\n")    
                            rob_waypoint.append([path[0][1][i][0][robot][0]+dx*di, path[0][1][i][0][robot][1]+dy*di, path[0][1][i][1], targets[i]])
                            if path[0][1][i][1]!=path[0][1][i-1][1] and new_wp:
                                new_wp = False
                                rob_wp_satsify_AP.append([path[0][1][i][0][robot][0]+dx*di, path[0][1][i][0][robot][1]+dy*di, path[0][1][i][1], targets[i]])
                            
                else:
                    f.write("0.15 "+str(path[0][1][i][0][robot][0])+" "+str(path[0][1][i][0][robot][1])
                                    +" "+str(height)+" 0 "+path[0][1][i][1]+" "+targets[i]+"\n")
                    rob_waypoint.append([path[0][1][i][0][robot][0], path[0][1][i][0][robot][1], path[0][1][i][1], targets[i]])
                    rob_wp_satsify_AP.append([path[0][1][i][0][robot][0], path[0][1][i][0][robot][1], path[0][1][i][1], targets[i]])
        all_rob_waypoints.append(rob_waypoint)
        all_rob_wp_satsify_AP.append(rob_wp_satsify_AP)
                    
        
    # for robot in range(number_of_robots):    
    #     with open(waypoint_folder_location+"/uav"+str(robot+1)+"_test.txt", 'w') as f:
    #         f.write("5 "+str(path[0][1][0][0][robot][0])+" "+str(path[0][1][0][0][robot][1])
    #                 +" "+str(height)+" 0 "+path[0][1][0][1]+"\n")    
    #         for i in range(1,len(path[0][1])):
    #             # f.write("hello\n")
    #             dx = (path[0][1][i][0][robot][0]-path[0][1][i-1][0][robot][0])/10
    #             dy = (path[0][1][i][0][robot][1]-path[0][1][i-1][0][robot][1])/10
    #             for di in range(1,11):
    #                 f.write("0.05 "+str(path[0][1][i-1][0][robot][0]+dx*di)+" "+str(path[0][1][i-1][0][robot][1]+dy*di)
    #                         +" "+str(height)+" 0 "+path[0][1][i][1]+"\n")    
        
    if edit_launch_file:
        a_file = open(launch_folder_location + "/ltl_sim.launch", "r")
        list_of_lines = a_file.readlines()
        j1 = 26
        j2 = 27
        add = 25
        for i in range(number_of_robots):
            list_of_lines[j1-1] = "      <arg name=\"x\" value=\""+str(path[0][1][0][0][i][0])+"\"/>\n"
            list_of_lines[j2-1] = "      <arg name=\"y\" value=\""+str(path[0][1][0][0][i][1])+"\"/>\n"
            j1+=add
            j2+=add
        
        a_file = open(launch_folder_location + "/ltl_sim.launch", "w")
        a_file.writelines(list_of_lines)
        a_file.close()
    return all_rob_waypoints, all_rob_wp_satsify_AP


def export_cov_to_txt(lm_cov, waypoint_folder_location, launch_folder_location):
    
    for lm in range(len(lm_cov[0].landmark)):
        lm_id="l"+str(lm+1)
        with open(waypoint_folder_location+"/lm_cov_"+str(lm+1)+".txt", 'w') as f:
            for i in range(len(lm_cov)):
                lx = lm_cov[i].landmark_x[lm]
                ly = lm_cov[i].landmark_y[lm]
                cov = np.cov(lx, ly)
                lambda_, v = np.linalg.eig(cov)
                lambda_ = np.sqrt(lambda_)
                x, y=np.mean(lx), np.mean(ly)
                width = lambda_[0]*3*2
                height = lambda_[1]*3*2
                angle= np.arccos(v[0, 0])
                quat_z = np.sin(angle/2)
                quat_w = np.cos(angle/2)
                if i==0:
                    f.write(str(x)+" "+str(y)+" "+str(width)+" "+str(height)+" "+str(quat_z)+" "+str(quat_w)+" 5\n")
                else:
                    f.write(str(x)+" "+str(y)+" "+str(width)+" "+str(height)+" "+str(quat_z)+" "+str(quat_w)+" 0.5\n")    
                
    