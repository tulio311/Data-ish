import numpy as np
import pandas as pd
import nltk

test_data_path = '/kaggle/input/llm-detect-ai-generated-text/test_essays.csv'
X = pd.read_csv(test_data_path)

textos = X.text
n = len(textos)

test_preds = np.zeros(n)

AIdif = 0.00550321648
humandif = -0.00970366534
midpoint = (AIdif + humandif)/2

Delta = AIdif - humandif

for r in range(n):
    v = nltk.tokenize.word_tokenize(textos[r])
    v1 = nltk.tag.pos_tag(v)
    m = len(v)
    sumaIN = 0
    sumaDT = 0
    
    for var in v1:
        if var[1] == 'IN':
            sumaIN += 1/m
        if var[1] == 'DT':
            sumaDT += 1/m
    
            
    worddif = sumaDT - sumaIN      
            
    if worddif >= midpoint + Delta:
        test_preds[r] = 1
    elif worddif <= midpoint - Delta:
        test_preds[r] = 0
    elif worddif >= midpoint:
        test_preds[r] = (worddif) / (2*Delta) + 0.5
    else:
        test_preds[r] = 0.5 - (midpoint - worddif) / (2*Delta)


output = pd.DataFrame({'id': X.id,
                       'generated': test_preds})
output.to_csv('submission.csv', index=False)