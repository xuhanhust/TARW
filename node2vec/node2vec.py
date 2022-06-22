# -*- coding:utf-8 -*-

"""



Author:

    Weichen Shen,wcshen1994@163.com



Reference:

    [1] Grover A, Leskovec J. node2vec: Scalable feature learning for networks[C]//Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2016: 855-864.(https://www.kdd.org/kdd2016/papers/files/rfp0218-groverA.pdf)



"""

from gensim.models import word2vec
import pandas as pd

from node2vec import walker


class Node2Vec:

    def __init__(self, graph, id, walk_length, num_walks, p=1.0, q=1.0, workers=1, use_rejection_sampling=0):

        self.graph = graph
        self.id = id
        self._embeddings = {}
        self.walker = walker.RandomWalker(
            graph, p=p, q=q, use_rejection_sampling=use_rejection_sampling)

        print("Preprocess transition probs...")
        self.walker.preprocess_transition_probs()

        self.sentences = self.walker.simulate_walks(
            id, num_walks=num_walks, walk_length=walk_length, workers=workers, verbose=1)



    def train(self, id):

        filename = 'node2vec_test' + str(id) + '.txt'
        sentences = word2vec.LineSentence(filename)
        model = word2vec.Word2Vec(sentences, vector_size=128, window=10, min_count=0, sg=1, workers=8, epochs=2)
        # model.save('text.model')  # 模型可保存
        return model


    def get_embeddings(self,):
        if self.w2v_model is None:
            print("model not train")
            return {}

        self._embeddings = {}
        for word in self.graph.nodes():
            self._embeddings[word] = self.w2v_model.wv[word]

        return self._embeddings
