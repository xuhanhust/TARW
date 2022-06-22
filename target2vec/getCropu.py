"""
@Time: 2020/11/13 15:34
@version: ,
@author: ,
@description: 
"""


import random as rand

import numpy as np


def getPath2(start, target_nodes, p, q, nx_G, path_length):  #修改了跳转概率，加入了归一化的目标节点含量
    # 计算每个节点的入度，作为游走下一节点选择概率的基础
    path = '.\data\WS_1_all.txt' #all
    bi_edges = []
    file = open(path)
    for line in file:
        source, target = line.split('   ')
        bi_edges.append((int(source), int(target)))

    in_degree = {}
    for edge in bi_edges:
        if edge[1] in in_degree:
            in_degree[edge[1]] += 1
        else:
            in_degree[edge[1]] = 1
    for node in list(nx_G.nodes):
        if node not in in_degree.keys():
            in_degree[node] = 0

    #初始化随机游走的前两个节点
    if start:
        path = [start]
    else:
        # Sampling is uniform w.r.t V, and not w.r.t E
        path = [rand.choice(list(nx_G.neighbors(start)))]

    while len(path) == 1 :
        cur = path[-1]  # 取最近的一个节点
        if len(list(nx_G.neighbors(cur))) > 0:  # 如果存在邻居节点
            #if rand.random() >= alpha:  # 随机生成一个概率，是否重新开始
                # 继续random_walk
                path.append(rand.choice(list(nx_G.neighbors(cur))))  # 从邻居中随机选择一个节点
            #else:
                # 重新开始新的random_walk
            #    path.append(path[0])
        else:
            break


    
    #根据t-v-x的不同类型，重新计算下一节点选择概率
    while len(path) < path_length:
        t = path[-2]
        v = path[-1]

        beta = []
        unnormalized_probs = []
        if len(list(nx_G.neighbors(v))) == 0: break
        for x in list(nx_G.neighbors(v)):
            temp = 0
            for u in list(nx_G.neighbors(x)):
                if u in target_nodes:
                    temp +=1
            beta.append(temp / len(list(nx_G.neighbors(x))))
            weight = in_degree[int(x)]  # w_vx

            if ((t in target_nodes) & (v not in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight/p )
            elif ((t not in target_nodes) & (v in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight/p)
            elif ((t not in target_nodes) & (v not in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight/p)
            elif ((t in target_nodes) & (v in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight)
            elif ((t not in target_nodes) & (v not in target_nodes) & (x not in target_nodes)):
                unnormalized_probs.append(weight)
            else:
                unnormalized_probs.append(weight/q)
        norm_const = sum(unnormalized_probs)
        norm_beta = sum(beta)
        if norm_const == 0: break
        normalized_probs = [float(u_prob)/norm_const for u_prob in unnormalized_probs]
        if norm_beta != 0:
            normalized_beta = [float(u_beta) / norm_beta for u_beta in beta]
            normalized_probs2 = np.array(normalized_probs) + np.array(normalized_beta)
            if len(normalized_probs)==1: break
            next_node = random_pick(list(nx_G.neighbors(v)), normalized_probs2)
            path.append(next_node)
        else:
            next_node = random_pick(list(nx_G.neighbors(v)), normalized_probs)
            path.append(next_node)

    return [str(node) for node in path]


def random_pick(some_list,probabilities):

    x = rand.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item



def getPath4(nodes, target_nodes, p, q, nx_G, path_length, all_path):  # 修改了跳转概率，重新写了公式
    # 计算每个节点的入度，作为游走下一节点选择概率的基础
    #filename = path + 'all\\' + str(id) + '.txt' #all
    bi_edges = []
    file = open(all_path)
    for line in file:
        source, target = line.split(' ')
        bi_edges.append((int(source), int(target)))

    in_degree = {}
    for edge in bi_edges:
        if edge[1] in in_degree:
            in_degree[edge[1]] += 1
        else:
            in_degree[edge[1]] = 1
    for node in list(nx_G.nodes):
        if node not in in_degree.keys():
            in_degree[node] = 0

    # 初始化随机游走的前两个节点

    if nodes:
        path = [nodes]
    else:
        # Sampling is uniform w.r.t V, and not w.r.t E
        path = [rand.choice(list(nx_G.neighbors(nodes)))]

    while len(path) == 1:
        cur = path[-1]  # 取最近的一个节点
        if len(list(nx_G.neighbors(cur))) > 0:  # 如果存在邻居节点
            # if rand.random() >= alpha:  # 随机生成一个概率，是否重新开始
            # 继续random_walk
            path.append(rand.choice(list(nx_G.neighbors(cur))))  # 从邻居中随机选择一个节点
        # else:
        # 重新开始新的random_walk
        #    path.append(path[0])
        else:
            break

    # 根据t-v-x的不同类型，重新计算下一节点选择概率
    while len(path) < path_length:
        t = path[-2]
        v = path[-1]


        unnormalized_probs = []
        if len(list(nx_G.neighbors(v))) == 0: break
        for x in list(nx_G.neighbors(v)):
            temp = 0
            for u in list(nx_G.neighbors(x)):
                if u in target_nodes:
                    temp += 1
            beta = temp / len(list(nx_G.neighbors(x)))
            if in_degree[int(x)] == 0:
                weight = 0
            else:
                weight = (1 + beta) / (in_degree[int(x)] + beta)  # w_vx

            if ((t in target_nodes) & (v not in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight / p)
            elif ((t not in target_nodes) & (v in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight / p)
            elif ((t not in target_nodes) & (v not in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight / p)
            elif ((t in target_nodes) & (v in target_nodes) & (x in target_nodes)):
                unnormalized_probs.append(weight)
            elif ((t not in target_nodes) & (v not in target_nodes) & (x not in target_nodes)):
                unnormalized_probs.append(weight)
            else:
                unnormalized_probs.append(weight / q)
        norm_const = sum(unnormalized_probs)

        if norm_const == 0: break
        normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]
        if len(normalized_probs) == 1: break
        next_node = random_pick(list(nx_G.neighbors(v)), normalized_probs)
        #若节点返回，则重新选择
        #if next_node == t: continue  #none-backtracking
        if len(path) > 3:
            if next_node == path[-3]: continue
        path.append(next_node)
        #if len(path) - len(set(path)) > 4: #重复过多后进行重启动
            #path.append(path[0])
            #path.append(rand.choice(list(nx_G.neighbors((path[0])))))


    return [str(node) for node in path]


