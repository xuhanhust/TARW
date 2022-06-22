"""
@Time: 2020/11/13 15:39
@version: ,
@author: ,
@description: 
"""


def save_path(walks, id):
    # storage
    filename = 'target2vec_test' + str(id) + '.txt'
    with open(filename, encoding="utf-8", mode="w") as f:
        for walk in walks:
            for node in walk:
                f.write(str(node) + " ")
            f.write("\n")