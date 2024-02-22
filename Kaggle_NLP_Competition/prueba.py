import pandas as pd
import numpy as np
import nltk

X = pd.read_csv("train_essays.csv")

textos = X.text

n = len(textos)

L = []


for i in range(n):
    v = nltk.tokenize.word_tokenize(textos[i])
    v1 = nltk.tag.pos_tag(v)
    for w in v1:
        if w[1] not in L:
            L.append(w[1])
    print(i)
        

print(L)        

