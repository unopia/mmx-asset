'''Trains a simple deep NN on the MNIST dataset.
Gets to 98.40% test accuracy after 20 epochs
(there is *a lot* of margin for parameter tuning).
2 seconds per epoch on a K520 GPU.
'''

from __future__ import print_function
import os, sys
import pandas as pd
import random
import json

import numpy as np

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

home = os.environ['project_home']
workflow_home = os.environ['workflow_history_path']
step = "models"
target_path = os.environ['target_path']
seq = os.environ.get('seq', '0')

DATA_PATH = os.path.join(workflow_home, 'data_in')
MODEL_PATH = os.path.join(workflow_home, step, target_path, seq)

os.makedirs(MODEL_PATH, exist_ok=True)

batch_size = 128
num_classes = 10
epochs = 20

target = os.environ.get('target', 'default')
argv = sys.argv

try:
    epochs = int(argv[1])
except:
    epochs = 2

hidden = 512

try:
    activate = argv[2]
except:
    activate = 'softmax'

try:
    dropout = float(sys.argv[3])
except:
    dropout = 0.2

print(epochs, activate, dropout)

with np.load("%s/mnist.npz" % DATA_PATH) as f:
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']

x_train = x_train.reshape(60000, 784)
x_train = x_train[:20000]
y_train = y_train[:20000]
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
print('here04')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(hidden, activation='relu', input_shape=(784,)))
model.add(Dropout(dropout))
model.add(Dense(hidden, activation='relu'))
model.add(Dropout(dropout))
model.add(Dense(num_classes, activation=activate))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])

print('train on prd')
history = model.fit(x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_data=(x_test, y_test))

print('train on prd')

score = model.evaluate(x_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
print(history.history)

arr = []
for i in range(5):
    model_path = '%s/%s_%s.h5' % (MODEL_PATH, target, "-".join(argv[1:] + [str(i)]))
    obj = {}
    obj['target'] = '%s_%s' % (target, str(i))
    obj['score'] = score[1]
    obj['model'] = '%s_%s' % (target, "-".join(argv[1:]+[str(i)]))
    obj['args'] = " ".join(argv[1:]+[str(i)])
    obj['path'] = model_path

    model.save(model_path)

    arr.append(obj)

df = pd.DataFrame(arr)
df.to_csv('%s/train.csv' % MODEL_PATH, index=False)
