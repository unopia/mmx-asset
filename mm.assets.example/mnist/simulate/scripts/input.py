'''Trains a simple deep NN on the MNIST dataset.
Gets to 98.40% test accuracy after 20 epochs
(there is *a lot* of margin for parameter tuning).
2 seconds per epoch on a K520 GPU.
'''

from __future__ import print_function
import os, sys
import pandas as pd
import json

import keras
from keras.datasets import mnist

# the data, split between train and test sets
home = os.environ['project_home']
workflow_home = os.environ['workflow_history_path']
DATA_PATH = os.path.join(workflow_home, 'data_in')

os.makedirs(DATA_PATH, exist_ok=True)
(x_train, y_train), (x_test, y_test) = mnist.load_data(path='%s/mnist.npz' % DATA_PATH)
