from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
from collections import Counter

index = []
result = []
sentences = [['1', '2', '5', '10'],
             ['2', '4', '8'],
             ['3', '4', '6'],
             ['4', '8'],
             ['5', '2', '1'],
             ['6', '4', '9'],
             ['7', '4', '6'],
             ['8', '4', '6'],
             ['9', '4', '8'],
             ['10', '5', '2', '1'],
             ['11', '5', '10']]
model = Word2Vec(sentences, size=2, window=3, min_count=0, sg=1, workers=8, iter=2)
#model = Word2Vec.load('text.model')
for i in range(1, 12):
        sims = model.wv.most_similar(str(i), topn=5)
        print('node number{}:'.format(i))
        print(sims)
        #print('\n')
        for j in range(5):
            index.append(sims[j][0])

#print(index)
collection_words = Counter(index)
print('出现次数统计')
print(collection_words)
most_counterNum = collection_words.most_common(3)
print(most_counterNum)
for k in range(3):
    result.append(most_counterNum[k][0])
print(result)
X = model[model.wv.vocab]
#print(type(X))
#pca = PCA(n_components=2)
#result = pca.fit_transform(X)
#print(result)
#lmodel = list(X)
pyplot.scatter(X[:, 0], X[:, 1])
words = list(model.wv.vocab)
#print(words)
for i, word in enumerate(words):
    pyplot.annotate(word, xy=(X[i, 0], X[i, 1]))
pyplot.show()