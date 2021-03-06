import numpy as np

def influence_count(nodes, edges, seeds, threshold):
    in_degree = {}
    inactive_nodes = []
    active_nodes = []
    nodes_status = {}

    for edge in edges:   #依次判断每条边首尾的节点是否在种子节点中
        if edge[0] in seeds:
            active_nodes.append(edge[0])
        else:
            inactive_nodes.append(edge[0])
        
        if edge[1] in seeds:
            active_nodes.append(edge[1])
        else:
            inactive_nodes.append(edge[1])
        
        if edge[1] in in_degree:
            in_degree[edge[1]] += 1
        else:
            in_degree[edge[1]] = 1

    active_nodes = list(set(active_nodes))
    inactive_nodes = list(set(inactive_nodes))

    for node in nodes:
        nodes_status[node] = 0
    for node in active_nodes:
        nodes_status[node] = 1  #结束选定种子节点后的初始赋值
            
    while(active_nodes): #从种子节点开始，到没有激活种子节点时结束
        new_actived_nodes = []
        for edge in edges:
            if nodes_status[edge[0]] == 1:
                if nodes_status[edge[1]] == 0:
                    p = np.array([1 - threshold / in_degree[edge[1]], threshold / in_degree[edge[1]]])
                    flag = np.random.choice([0, 1], p=p.ravel()) #确定每条边的激活概率

                    if flag:
                        new_actived_nodes.append(edge[1])
        
        for node in active_nodes:
            nodes_status[node] = 2  #已被激活且尝试过激活其他节点的节点
        for node in new_actived_nodes:
            nodes_status[node] = 1
        active_nodes = new_actived_nodes

    final_actived_node = 0
    for node in nodes:
        if nodes_status[node] == 2:
            final_actived_node += 1

    return final_actived_node  
