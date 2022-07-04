from sklearn.linear_model import LogisticRegression
import pandas as pd

import os
import pickle
import csv

home = os.environ['project_home']
workflow_history_path = os.environ['workflow_history_path']
step = 'train'
target_path = os.environ['target_path']
seq = os.environ.get('seq', '0')

data_path = os.path.join(home, 'data_in')
model_path = os.path.join(home, 'model')

train_file = os.path.join(workflow_history_path, step, target_path, seq, 'train.csv')

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(model_path):
    os.mkdir(model_path)

X_train = pd.read_csv(os.path.join(data_path, 'X_train.csv'))
y_train = pd.read_csv(os.path.join(data_path, 'y_train.csv'))

logistic = LogisticRegression()
logistic.fit(X_train, y_train)

with open(os.path.join(model_path, 'logistic_model.pkl'), 'wb') as f:
    pickle.dump(logistic, f)

with open(train_file, 'w') as csvfile:
    fieldnames = ['target', 'path', 'args']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'target': 'iris_classifier', 'path': os.path.join(model_path, 'logistic_model.pkl'), 'args': 'LR'})
