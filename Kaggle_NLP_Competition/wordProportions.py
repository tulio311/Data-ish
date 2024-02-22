import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt

X = pd.read_csv("train_essays.csv")

textos = X.text
labels = X.generated

n = len(textos)

arr = ['NNS', '.', 'VBP', 'VBN', 'IN', 'PRP', 'VBD', 'JJ', 'DT', 'CD', ',', 'WRB', 'NNP', 'CC', 'NN', 'PRP$', 'VBZ', 'RB', 'VBG', 'TO', 'VB', 'MD', '``', "''", ':', 'NNPS', 'PDT', 'WDT', 'RP', 'JJR', 'JJS', 'RBR', 'EX', 'POS', 'RBS', 'WP', 'UH', 'FW', '$', 'WP$']
numAt = len(arr)

M = np.eye(n,numAt)

for r in range(n):
    print(r)
    v = nltk.tokenize.word_tokenize(textos[r])
    m = len(v)
    v1 = nltk.tag.pos_tag(v)
    k = np.zeros(numAt)
    
    for var in v1:
        for j in range(numAt):
            if var[1] == arr[j]:
                k[j] += 1/m 
    M[r] = k

    # Uncomment these 2 lines if you want to plot the AI written texts
    #if labels[r] == 1:
    #    plt.plot(np.arange(0,numAt),k,color="red")

    # Uncomment these 2 lines if you want to plot the human written texts
    #if labels[r] == 0:
    #    plt.plot(np.arange(0,numAt),k,color="blue")


plt.show()



