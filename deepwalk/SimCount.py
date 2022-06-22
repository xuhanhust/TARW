"""
@Time: 2020/11/16 14:11
@version: ,
@author: ,
@description: 
"""

import numpy as np
import networkx as nx
import random

# -----------------从最终的结构表示中找对所有节点进行相似度计算并排序，找最优的排序---------------

# 计算余弦相似度
def clacSimilaryScore(model, v, len):
    li = model.wv.similar_by_vector(np.array(model.wv[v]), topn=len) # topn=None为计算所有
    return li

# 字典按照value排序
def getTopK(dict_, k = 20):
    keys = list(dict_.keys())
    # 冒泡排序
    for key_i in range(len(keys)):
        for key_j in range(key_i+1, len(keys)):
            if dict_[keys[key_i]] < dict_[keys[key_j]]:
                temp = keys[key_i]
                keys[key_i] = keys[key_j]
                keys[key_j] = temp
    # 保留前K个
    resu_ = dict()
    for i in range(k):
        if len(keys) > i:
            resu_[keys[i]] = dict_[keys[i]]
    return resu_

# 遍历所有，返回TOPＫ
def getSimilaryByMostKSimilary(model, g, k=6):
    result_dict = dict()
    for i in g.nodes:
        result_dict[str(i)] = 0

    for rand_ in range(3):
        random_node = random.choice(list(g.nodes))
        # 随机三个节点，作为计算的初始节点，然后就开始统计
        theta = clacSimilaryScore(model, str(random_node), len(g))[k][1] #clacsimilaryscore返回一个列表，元素是节点编号与相似度，提取其中第11个元素的相似度作为theta
        for i in g.nodes:
            li = clacSimilaryScore(model, str(i), len(g))
            for ele in li:
                if ele[1] >= theta:
                    result_dict[str(ele[0])] += 1
    # 取平均值
    for key in result_dict.keys():
        result_dict[key] //= 3
    return getTopK(result_dict, k)
