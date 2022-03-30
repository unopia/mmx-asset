from sklearn.linear_model import LogisticRegression, ARDRegression
import pandas as pd

import os, sys

home = os.environ['project_home']
model_path = os.path.join(home, 'model')
data_path = os.path.join(home, 'data_in')
target = 'LOGISTIC'
#######################

if not os.path.exists(model_path):
    os.mkdir(model_path)
# Our model - a multiclass regression
# FIRST we initialize it with default params or specify some
X_train = pd.read_csv(os.path.join(data_path, 'X_train.csv'))
X_test = pd.read_csv(os.path.join(data_path, 'X_test.csv'))
y_train = pd.read_csv(os.path.join(data_path, 'y_train.csv'))
y_test = pd.read_csv(os.path.join(data_path, 'y_test.csv'))

logistic = LogisticRegression()
import sklearn.linear_model as lm

# dynamic param
if not os.environ['target'] == 'default':
    target = os.environ['target']

if not len(sys.argv) is 1:
    intercept_param = int(sys.argv[1])
else:
    intercept_param = 1

print('--------log--------')
print(target)

if target == 'LOGISTIC':
    model = LogisticRegression(intercept_scaling=intercept_param)

elif target == 'ARD':
    model = ARDRegression()
# Train on iris training set
# SECOND we give the model some training data
model.fit(X_train, y_train)

# THIRD we give our model some test data and predict something
from sklearn.metrics import accuracy_score

y_predict = model.predict(X_test)

acc_score = accuracy_score(y_test, y_predict)

print("accuracy score :%f" % acc_score)
import pickle

# save model
with open(os.path.join(model_path, 'iris_logistic.pkl'), 'wb') as f:
    pickle.dump(model, f)

print("model saved, path :%s" % model_path)