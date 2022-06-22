import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict
import time
from joblib import Parallel, delayed
import itertools
from deepwalk import getCropu
from deepwalk import savePath
from deepwalk import learningEmbedding as learn
from deepwalk import SimCount
from node2vec.node2vec import Node2Vec

from target2vec import getCropu as tar_getCropu
from target2vec import savePath as tar_savePath
from target2vec import learningEmbedding as tar_learn
from target2vec import SimCount as tar_SimCount




def degree(edges, n):
    degree = {}
    seeds = []

    for edge in edges: 
        if edge[0] in degree:
            degree[edge[0]] += 1
        else:
            degree[edge[0]] = 1
        if edge[1] in degree:
            degree[edge[1]] += 1
        else:
            degree[edge[1]] = 1

    seeds = list({k: v for k, v in sorted(degree.items(), key=lambda item: item[1], reverse=True)}.keys())[:n]
    return seeds

def pagerank(nodes, edges, n):
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    pr = nx.pagerank(g)

    seeds = list({k: v for k, v in sorted(pr.items(), key=lambda item: item[1], reverse=True)}.keys())[:n]
    return seeds

def random(nodes, n):
    np.random.shuffle(nodes)

    return nodes[:n]



def deepwalk(nodes, edges, seeds_number, target_nodes,id):

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    #print("输出全部节点：{}".format(g.nodes()))
    #print("输出全部边：{}".format(g.edges()))

    #nx.draw(g)
    #plt.show()

    path_length = 12
    alpha = 0.2
    # 生成路径
    walks = []
    nodes_number = 0
    target_number = 0
    for node in g.nodes:
        #for i in range(5):
        path = getCropu.getPath(node, g, path_length, alpha)
        walks.append(path)
        nodes_number = nodes_number + len(path)
        for i in path:
            if int(i) in target_nodes:
                target_number += 1

        # j+=1
        # print('生成{}次路径'.format(j))
    #print('游走节点总数量', nodes_number)
    #print('游走序列中所含目标节点数量', target_number)
    #print('游走序列中目标节点占比', target_number / nodes_number)
    # 保存路径
    savePath.save_path(walks, id)
    # 学习嵌入
    pathtolearn = 'deepwalk_test' + str(id) + '.txt'
    model = tar_learn.learn(pathtolearn)
    # 选择种子节点
    resu = SimCount.getSimilaryByMostKSimilary(model, g, seeds_number)
    return [int(i) for i in list(resu.keys())]


def node2vec(nodes, edges, seeds_number, id):

    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    model = Node2Vec(g, id, walk_length=12, num_walks=len(g.nodes),
                     p=0.25, q=4, workers=1, use_rejection_sampling=0)
    model_embedding = model.train(id)
    # 选择种子节点
    resu = SimCount.getSimilaryByMostKSimilary(model_embedding, g, seeds_number)
    return [int(i) for i in list(resu.keys())]





def get_neigbors(g, node, depth=1):
    output = {}
    layers = dict(nx.bfs_successors(g, source=node, depth_limit=depth))
    nodes = [node]
    for i in range(1,depth+1):
        output[i] = []
        for x in nodes:
            output[i].extend(layers.get(x,[]))
        nodes = output[i]
    return output


def target2vec3(nodes, edges, seeds_number, target_nodes, all_path, id):

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    #print("输出全部节点：{}".format(g.nodes()))
    #print("输出全部边：{}".format(g.edges()))

    #nx.draw(g)
    #plt.show()
    #path_length = nx.diameter(g)
    #print('path_length = ', path_length)
    path_length = 15
    p = 0.1
    q = 10
    #nwpd = 2
    #j = 0
    # 生成路径
    walks = []
    nodes_number = 0
    target_number = 0
    for node in g.nodes:
        #NW = nwpd * g.degree(int(node))
        #for i in range(0, 3):
    #results = Parallel(n_jobs=8, verbose=0)(delayed(tar_getCropu.getPath3)(node, target_nodes, p, q, g, path_length) for node in g.nodes)
    #path = list(itertools.chain(*results))
        path = tar_getCropu.getPath4(node, target_nodes, p, q, g, path_length, all_path)
        walks.append(path)
        nodes_number = nodes_number + len(path)
        for i in path:
            if int(i) in target_nodes:
                target_number += 1

            #j+=1
            #print('生成{}次路径'.format(j))
    #print('游走节点总数量', nodes_number)
    #print('游走序列中所含目标节点数量', target_number)
    #print('游走序列中目标节点占比', target_number/nodes_number)
    # 保存路径
    tar_savePath.save_path(walks, id)
    # 学习嵌入
    pathtolearn = 'target2vec_test' + str(id) + '.txt'
    model = tar_learn.learn(pathtolearn)
    # 选择种子节点
    resu = tar_SimCount.getSimilaryByMostKSimilary(model, g, seeds_number)
    return [int(i) for i in list(resu.keys())]
