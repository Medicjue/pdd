# -*- coding: utf-8 -*-

import os

if not os.path.exists('../output/digest_result/'):
    os.makedirs('../output/digest_result/')

#%%
data = []
predict_labels = []
column_names = []
with open('../output/arff/arff_2019-05-04_12:53:50.txt', 'r') as f:
    line = f.readline()
    line = line.strip()
    while line is not None:
        if '@attribute' in line:
            column_names.append(line[len('@attribute')+1:])
        if '@data' in line:
            print('QQ')
            break
        line = f.readline()
        line = line.strip()
    line = f.readline()
    line = line.strip()
    
    while line is not None and line != '':
        label = line.split(',')[-1]
        data.append(line.split(','))
        predict_labels.append(label)
        line = f.readline()
        line = line.strip()
    
#%%
import pandas as pd    
data = pd.DataFrame(data, columns=column_names)

data.to_csv('../output/digest_result/data.csv', index=False, encoding='utf8')
        
#%%

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import numpy as np

data = shuffle(data)
data = data.reset_index(drop=True)

labels = data['class {phish, legitimate}']
features = data.iloc[:,0:39]

kfold = KFold()
kfold.get_n_splits(features)

predict_labels = []
for train_index, test_index in kfold.split(features):
    mdl = RandomForestClassifier(random_state=23)
    mdl.fit(features.iloc[train_index,:], labels[train_index])
    predict_label = mdl.predict(features.iloc[test_index,:])
    predict_labels = np.concatenate([predict_labels, predict_label])

#%%
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

print(confusion_matrix(labels, predict_labels))

print(precision_recall_fscore_support(labels, predict_labels))