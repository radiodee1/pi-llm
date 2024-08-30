#!/bin/env python3

import argparse
import gensim
import re 
import codecs
import multiprocessing
from gensim.models import Word2Vec
import nltk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 
from sklearn.manifold import TSNE
import numpy as np


keys = ['Paris', 'Python', 'Sunday', 'Tolstoy', 'Twitter', 'bachelor', 'delivery', 'election', 'expensive',
        'experience', 'financial', 'food', 'iOS', 'peace', 'release', 'war']

def tsne_plot_similar_words(title, labels, embedding_clusters, word_clusters, a, filename=None):
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
    for label, embeddings, words, color in zip(labels, embedding_clusters, word_clusters, colors):
        x = embeddings[:,0]
        y = embeddings[:,1]
        plt.scatter(x, y, c=color, alpha=a, label=label)
        for i, word in enumerate(words):
            plt.annotate(word, alpha=0.5, xy=(x[i], y[i]), xytext=(5, 2),
                         textcoords='offset points', ha='right', va='bottom', size=8)
    plt.legend(loc=4)
    plt.title(title)
    plt.grid(True)
    if filename:
        plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pi LLM Output File Plotter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file', default='', help="File name and path.")
    parser.add_argument('--bin', default='', help="Input Word2Vec binary file.")
    parser.add_argument('--output', default='', help="Filename for output plot.")
    parser.add_argument('--p', default=15, help="perplexity value.")
    parser.add_argument('--topn', default=5, help="topn value.")
    parser.add_argument('--all', action="store_true", help="plot all words (include test words.)")
    args = parser.parse_args()
 
    if args.file != None and str(args.file).strip() != "":
        print(args.file)
        if not args.all == True:
            keys = []
        f = open(str(args.file).strip(), 'r')
        x = f.readlines()
        for i in x:
            if len(i.split(' ')) == 2:
                keys.append(i.split(' ')[0][:-1])
        f.close()
        #keys = keys[:16]
        print(keys)

    ## we're not using perplexity...
    TOPN = 30
    PERPLEXITY = 15 
    W2V_BIN = '../../GoogleNews-vectors-negative300.bin'
    OUTPUT_FILE = 'similar_words.png'

    if args.topn != None and int(args.topn) > 0:
        TOPN = int(args.topn)

    if args.p != None and int(args.p) > 0:
        PERPLEXITY = int(args.p)

    if args.bin != None and str(args.bin).strip() != "":
        W2V_BIN = str(args.bin).strip()

    if args.output != None and str(args.output).strip() != "":
        OUTPUT_FILE = str(args.output).strip() + ".png"

    model = gensim.models.KeyedVectors.load_word2vec_format(W2V_BIN, binary=True)

    embedding_clusters = []
    word_clusters = []
    for word in keys:
        embeddings = []
        words = []
        for similar_word, _ in model.most_similar(word, topn=TOPN):
            words.append(similar_word)
            embeddings.append(model[similar_word])
        embedding_clusters.append(embeddings)
        word_clusters.append(words)


    #embeddings_en_2d = embedding_clusters
    #% matplotlib inline

    embedding_clusters = np.array(embedding_clusters)
    n, m, k = embedding_clusters.shape
    tsne_model_en_2d = TSNE(perplexity=PERPLEXITY, n_components=2, init='pca', n_iter=3500, random_state=32)
    embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(embedding_clusters.reshape(n * m, k))).reshape(n, m, 2)

    tsne_plot_similar_words('Similar words from Google News', keys, embeddings_en_2d, word_clusters, 0.7,
                            OUTPUT_FILE)
    print('keys', len(keys))
