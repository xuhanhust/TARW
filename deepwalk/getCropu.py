"""
@Time: 2020/11/13 15:34
@version: ,
@author: ,
@description: 
"""


import random as rand

def getPath(start, nx_G, path_length, alpha):
    if start:
        path = [start]
    else:
        # Sampling is uniform w.r.t V, and not w.r.t E
        path = [rand.choice(list(nx_G.neighbors(start)))]

    while len(path) < path_length:
        cur = path[-1]  # 取最近的一个节点
        if len(list(nx_G.neighbors(cur))) > 0:  # 如果存在邻居节点
            if rand.random() >= alpha:  # 随机生成一个概率，是否重新开始
                # 继续random_walk
                path.append(rand.choice(list(nx_G.neighbors(cur))))  # 从邻居中随机选择一个节点
            else:
                # 重新开始新的random_walk
                path.append(path[0])
        else:
            break
    return [str(node) for node in path]


