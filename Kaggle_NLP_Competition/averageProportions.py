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
    

arrfIA = np.zeros(numAt)
arrfHu = np.zeros(numAt)

for i in range(numAt):
    sumIA = 0
    sumHu = 0
    contIA = 0
    contHu = 0

    for j in range(n):
        if labels[j] == 1:
            sumIA += M[j][i]
            contIA += 1
        else:
            sumHu += M[j][i]
            contHu += 1
    arrfIA[i] = sumIA/contIA
    arrfHu[i] = sumHu/contHu

print("La IA tiene %f IN",arrfIA[4] )
print("La IA tiene %f DT",arrfIA[8] )
print("La IA tiene %f IN",arrfHu[4] )
print("La IA tiene %f DT",arrfHu[8] )

# Uncomment the first one if you want the AI written texts plot
# and the second human if you want the human written texts plot
     
#plt.plot(np.arange(0,numAt),arrfIA, color = "red")
#plt.plot(np.arange(0,numAt),arrfHu, color = "blue")
    
plt.show()


