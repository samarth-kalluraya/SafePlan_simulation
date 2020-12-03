# -*- coding: utf-8 -*-

import numpy as np
import pyvisgraph as vg


def construction_biased_tree(tree, n_max):
    """
    construction of the biased tree
    :param tree: biased tree
    :param n_max: maximum number of iterations
    :return: found path
    """

    for n in range(n_max):
        if n%200 == 0:
            print("---------------------------------------------%d" %(n))
            # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n                                              ---------------------------------------------%d" %(n))
        # biased sample
        x_new, x_angle, q_p_closest, label, target_b_state = tree.biased_sample()
        # couldn't find x_new
        if not x_new: continue
        # label of x_new
        # label = tree.task.get_label_landmark(x_new, tree.workspace_instance)
        # near state
        if tree.lite:
            # avoid near
            near_nodes = [q_p_closest]
        else:
            near_nodes = tree.near(tree.mulp2single(x_new))
            near_nodes = near_nodes + [q_p_closest] if q_p_closest not in near_nodes else near_nodes

        # check the line is obstacle-free: returns True if path is possible
        obs_check = tree.obstacle_check(near_nodes, x_new, label)
        # not obstacle-free
        if tree.lite and not list(obs_check.items())[0][1]: continue

        # iterate over each buchi state
        for b_state in tree.buchi.buchi_graph.nodes:
            # new product state
            q_new = (x_new, b_state)
            # extend
            added = tree.extend(q_new, x_angle, near_nodes, label, obs_check, target_b_state)
            # rewire
            if not tree.lite and added:
                tree.rewire(q_new, near_nodes, obs_check)

        # detect the first accepting state
        if len(tree.goals): break

    return tree.find_path(tree.goals)


def path_via_visibility(tree, path):
    """
    using the visibility graph to find the shortest path
    :param tree: biased tree
    :param path: path found by the first step of the suffix part
    :return: a path in the free workspace (after treating all regions as obstacles) and its distance cost
    """
    paths = []
    max_len = 0
    # find a path for each robot using visibility graph method
    for i in range(tree.robot):
        init = path[-1][0][i]
        goal = path[0][0][i]
        shortest = tree.g.shortest_path(vg.Point(init[0], init[1]), vg.Point(goal[0], goal[1]))
        max_len = len(shortest) if len(shortest) > max_len else max_len
        paths.append([(point.x, point.y) for point in shortest])
    # append to the same length
    for i in range(tree.robot):
        paths[i] = paths[i] + [paths[i][-1]]*(max_len-len(paths[i]))
    # combine to one path of product state
    path_free = [(tuple([p[i] for p in paths]), '') for i in range(max_len)]  # second component serves as buchi state
    # calculate cost
    cost = 0
    for i in range(1, max_len):
        cost = cost + np.linalg.norm(np.subtract(tree.mulp2single(path_free[i][0]), tree.mulp2single(path_free[i-1][0])))

    return cost, path_free
