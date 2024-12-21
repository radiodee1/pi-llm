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
from numpy.linalg import cond
from sklearn.manifold import TSNE
import numpy as np
import math 
#import os 

keys = ['Paris', 'Python', 'Sunday', 'Tolstoy', 'Twitter', 'bachelor', 'delivery', 'election', 'expensive',
        'experience', 'financial', 'food', 'iOS', 'peace', 'release', 'war']

show_plot = True 

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
    if show_plot:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pi LLM Output File Plotter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('files', default='',nargs='+', help="File name and path.")
    parser.add_argument('--bin', default='', help="Input Word2Vec binary file.")
    parser.add_argument('--p', default=15, help="perplexity value.")
    parser.add_argument('--topn', default=5, help="topn value.")
    parser.add_argument('--all', action="store_true", help="plot all words (include test words.)")
    parser.add_argument('--single_graph', action="store_true", help="plot all words on single graph.")
    parser.add_argument('--words', default=-1, help="number of words from each count document.")
    args = parser.parse_args()
    
    embedding_clusters = []
    word_clusters = []
    filename_clusters = []

    PERPLEXITY = 15 
    out_path = "." 
    OUTPUT_FILE = '/diagram.png'

    if len(args.files) > 1:
        show_plot = False
    for i in args.files:
        file = i 
        if file != None and str(file).strip() != "" and file.endswith('.count.txt'):
            print(file)
            if not args.all == True:
                keys = []
            f = open(str(file).strip(), 'r')
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
            #OUTPUT_FILE = 'similar_words.png'

            if args.topn != None and int(args.topn) > 0:
                TOPN = int(args.topn)

            if args.p != None and float(args.p) >= 0:
                PERPLEXITY = float(args.p)

            if args.bin != None and str(args.bin).strip() != "":
                W2V_BIN = str(args.bin).strip()

            file_out = file.split('/')[-1]
            if file_out.startswith('count-'):
                file_out = file_out[len('count-'):]

            out_path = file.split('/')[0:-1] 
            out_path = '/'.join(out_path)
            OUTPUT_FILE = str(out_path + '/pic-' + file_out).strip()[0:-len('.count.txt')] + ".png"

            model = gensim.models.KeyedVectors.load_word2vec_format(W2V_BIN, binary=True)

            if not args.single_graph:
                embedding_clusters = []
                word_clusters = []
                filename_clusters = []

            for word in keys:
                embeddings = []
                words = []
                filenames = []
                #if int(args.words) != -1 and num >= int(args.words):
                #    print(num, 'break')
                #    break
                if word not in model:
                    print('not in model', word)
                    continue
                if TOPN == 1:
                    words.append(word)
                    embeddings.append(model[word])
                    filenames.append(file_out)
                else:
                    for similar_word, _ in model.most_similar(word, topn=TOPN):
                        words.append(similar_word)
                        embeddings.append(model[similar_word])
                        filenames.append(file_out)

                embedding_clusters.append(embeddings)
                word_clusters.append(words)
                filename_clusters.append(filenames)


    embedding_clusters = np.array(embedding_clusters)
    n, m, k = embedding_clusters.shape
    tsne_model_en_2d = TSNE(perplexity=PERPLEXITY, n_components=2, init='pca', n_iter=3500, random_state=32)
    embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(embedding_clusters.reshape(n * m, k))).reshape(n, m, 2)

    if not args.single_graph:
        tsne_plot_similar_words('Similar words from Google News', keys, embeddings_en_2d, word_clusters, 0.7,
                                OUTPUT_FILE)
        print('keys', len(keys))
        #exit()

    print(embeddings_en_2d) 
    ff = open(out_path + "/distance.csv", 'w')
    oldf = ""
    dist = 0
    xold = 0 
    yold = 0
    num = 0 
    for embeddings, file in zip(embeddings_en_2d, filename_clusters):
        x = embeddings[:,0][0]
        y = embeddings[:,1][0]
        f = file[0]
        if oldf == f:
            #print('here...')
            tempx = x - xold
            tempy = y - yold
            tempx = tempx * tempx
            tempy = tempy * tempy
            dist = math.sqrt(tempx + tempy )
        else:
            dist = 0
            num = 0
            print(f)
        dist_origin = math.sqrt(x * x + y * y)
        oldf = f 
        xold = x 
        yold = y 
        if num >= int(args.words):
            continue 
        print(num, x,y, f, dist, dist_origin)
        ff.write(str(x) + ", " + str(y) + ", " + str(f) + ", " + str(dist) + ", " + str(dist_origin) + "\n")
        num += 1 
        pass
    ff.close()
