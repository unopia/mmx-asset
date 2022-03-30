import pandas as pd
import numpy as np


from sklearn import datasets
import os

home = os.environ['project_home']
workflow_history_path = os.environ['workflow_history_path']
step = 'parameter'

data_path = os.path.join(home, 'data_in')

parameter_file = os.path.join(workflow_history_path, step, 'parameter.csv')

# Other datasets in sklearn have similar "load" functions
iris = datasets.load_iris()

# Leave one value out from training set - that will be test later on
X_train, y_train = iris.data[:-1,:], iris.target[:-1]

X_train_pdf = pd.DataFrame(X_train)
y_train_pdf = pd.DataFrame(y_train)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train_pdf,y_train_pdf, test_size = 0.2)

print("train dataset dimension : %s" % (X_train.shape,))
print("test dataset dimension : %s" % (X_test.shape,))
print("train target dimension : %s" % (y_train.shape,))
print("test target dimension : %s" % (y_test.shape,))

#os.chmod(data_path, 0o777)
print(os.system('whoami'))
import getpass
print(getpass.getuser())
import subprocess
print(subprocess.check_output('whoami'))
a = subprocess.check_output(['ls','-al',data_path])
print(a.decode('utf-8'))


X_train.to_csv(os.path.join(data_path, 'X_train.csv'), index=False)
X_test.to_csv(os.path.join(data_path, 'X_test.csv'), index=False)
y_train.to_csv(os.path.join(data_path, 'y_train.csv'), index=False)
y_test.to_csv(os.path.join(data_path, 'y_test.csv'), index=False)

#original data
if len(X_train) < 120:
    target = 'LOGISTIC'
else: # Augmented
    target = 'ARD'

import pandas as pd
df = pd.DataFrame([['dynamic-train', 'train', target,'1' ]],
                  columns = ['workflow', 'step', 'target', 'args'])

df.to_csv(parameter_file,index= False)