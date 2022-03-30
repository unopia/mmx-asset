from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import os, sys


home = os.environ['project_home']
workflow_home = os.environ['workflow_history_path']
step = 'models'
target_path = os.environ['target_path']
seq = os.environ.get('seq', '0')

model_path = os.path.join(home, 'model')
data_path = os.path.join(home, 'data_in')

train_file = os.path.join(workflow_home, step, target_path, seq, 'train.csv')

target = os.environ['target']
# args = sys.argv
algo = os.environ['model']

def create_df (col_list = []) : 
    df = pd.DataFrame(columns = col_list)
    return df

if not os.path.exists(model_path):
    os.mkdir(model_path)

X_train = pd.read_csv(os.path.join(data_path, 'X_train.csv'))
X_test = pd.read_csv(os.path.join(data_path, 'X_test.csv'))
y_train = pd.read_csv(os.path.join(data_path, 'y_train.csv'))
y_test = pd.read_csv(os.path.join(data_path, 'y_test.csv'))

train_col = ['target', 'path', 'score', 'args']
train_df = create_df(train_col)

import pickle

model_name = 'iris_' + algo + '.pkl'
model = eval(algo + '()')
model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score
y_predict = model.predict(X_test)

acc_score = accuracy_score(y_test, y_predict)

print('accuracy score :%f' % acc_score)
with open(os.path.join(model_path, model_name), 'wb') as f:
    pickle.dump(model, f)

print('model saved, path :%s' % os.path.join(model_path, model_name))

a = pd.DataFrame(data=[[ target, os.path.join(model_path, model_name), acc_score, 1]], columns=train_col)
print(a)

train_df = train_df.append(a).reset_index(drop=True)
    
print(train_df)
train_df.to_csv(train_file, index = False)
