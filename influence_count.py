import numpy as np

def influence_count(nodes, edges, seeds, target_nodes, threshold):
    in_degree = {}
    inactive_nodes = []
    active_nodes = []
    nodes_status = {}
    time_step = 0
    cur_activated_node = {}
    cur_activated_target = {}

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
        time_step += 1
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

        actived_node = 0
        target_actived_node = 0

        for node in nodes:
            if nodes_status[node] == 2:
                actived_node += 1
                if node in target_nodes:
                    target_actived_node += 1

        cur_activated_node[time_step] = actived_node
        cur_activated_target[time_step] = target_actived_node





    final_actived_node = 0
    final_target_actived_node = 0

    for node in nodes:
        if nodes_status[node] == 2:
            final_actived_node += 1
            if node in target_nodes:
                final_target_actived_node += 1

    #filename1 = "difussion_activated_node.txt" #激活节点数量随时间变化趋势
    #with open(filename1, encoding="utf-8", mode="w") as f:
        #for j in cur_activated_node.keys():
            #f.write(str(j) + ' '+str(cur_activated_node[j]))
            #f.write("\n")

    #filename2 = "difussion_activated_target.txt" #激活目标节点数量随时间变化趋势
    #with open(filename2, encoding="utf-8", mode="w") as f:
        #for k in cur_activated_target.keys():
            #f.write(str(k) + ' ' + str(cur_activated_target[k]))
            #f.write("\n")

    #filename1 = "difussion_progess_activated.txt"
    #with open(filename1, encoding="utf-8", mode="w") as f:
        #for node in nodes:
            #if nodes_status[node] == 2:
                #f.write(str(node) + " ")
                #f.write("\n")

    #filename2 = "difussion_progess_target.txt"
    #with open(filename2, encoding="utf-8", mode="w") as f:
        #for node in nodes:
            #if nodes_status[node] == 2:
                #if node in target_nodes:
                    #f.write(str(node) + " ")
                    #f.write("\n")

    return final_actived_node, final_target_actived_node
