# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 13:23:32 2022

@author: monsi
"""
import numpy as np
import tensorflow as tf
import tensorflow.keras as tfk
from tensorflow.keras.layers import Dense, Input, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential as Seq

#Setting float print options for nicer floats :)
np.set_printoptions(precision=2)
np.set_printoptions(formatter={"float_kind": lambda x: "%g" % x})

#import data from txt file and convert to numpy array
filename = 'match_data_collection_safe.txt'
data = np.loadtxt(filename, delimiter=',', dtype=float, converters={0: lambda s: s[1:], -1: lambda s: s[:-1]})
#Remove last column of match id
data = data[:,:-1]
#shuffle to avoid using data from only same players/elo for training
np.random.shuffle(data)

#scale values from mastery points via logarithm
mastery_indices = [1,5,9,13,17,21,25,29,33,37]
data[:,mastery_indices]=np.log2(data[:,mastery_indices]*0.001+1)*10

#champion id to class map
classes=["1 engange_tank", "2 adc", "3 apc", "4 adfighter","5 apfighter", "6 enchanter", "7 assasins", "8 adpoke"
         , "9 ap poke"]
champion_id_to_class={
    266:3, 103:3, 84:5, 166:2, 12:1, 32:1, 34:3, 1:3, 523:2, 22:8, 136:5, 268:3, 432:5, 53:1, 63:3, 201:1,
    51:2, 164:4, 69:3, 31:1, 42:9, 122:4, 131:1, 119:2, 36:1, 245:7, 60:5, 28:7, 81:8, 9:1, 114:4, 105:8, 3:1,
    41:8, 86:4, 150:1, 79:1, 104:2, 887:5, 120:1, 74:3, 420:4, 39:4, 427:6, 40:6, 59:1, 24:4, 126:8, 202:2,
    222:2, 145:9, 429:2, 43:9, 30:3, 38:5, 55:5, 10:2, 141:4, 85:1, 121:7, 203:2, 240:4, 96:2, 7:7, 64:4,
    89:1, 876:5, 127:1, 236:2, 117:6, 99:9, 54:1, 90:3, 57:9, 11:7, 21:2, 62:1, 82:5, 25:9, 267:6, 75:4, 111:1,
    518:3, 76:9, 56:4, 20:1, 2:4, 61:3, 516:1, 80:4, 78:1, 555:7, 246:7, 133:2, 497:1, 33:1, 421:4, 526:1, 
    888:6, 58:4, 107:4, 92:4, 68:5, 13:3, 360:2, 113:1, 235:2, 147:6, 875:4, 35:7, 98:1, 102:9, 27:1, 14:1,
    15:2, 16:6, 50:5, 517:5, 134:3, 223:1, 163:3, 91:7, 44:6, 17:9, 412:1, 18:2, 48:4, 23:4, 4:9, 29:2, 77:4,
    6:4, 110:8, 67:2, 45:3, 161:9, 711:3, 254:4, 234:4, 112:3, 8:3, 106:4, 19:4, 498:2, 101:9, 5:4, 157:4, 
    777:4, 83:4, 350:6, 154:1, 238:7, 221:2, 115:9, 26:6, 142:9, 143:9, 72:1, 37:6
    }

#Add the champion classes to the training data
f = np.vectorize(champion_id_to_class.get)
ch_ids=list(range(0,40,4))
for i in reversed(ch_ids):
    x = f(data[:,i])
    data = np.insert(data,i+1,x,axis=1)

#Remove Champions from the training data after adding classes
ch_ids=list(range(0,49,5))
for i in reversed(ch_ids):
    data = np.delete(data,obj=i,axis=1)

#Remove Champions from the training data without adding classes
# ch_ids=list(range(0,40,4))
# for i in reversed(ch_ids):
#     data = np.delete(data,obj=i,axis=1)

#Take only champions as network input
# ch_ids=list(range(0,41,4))
# data=data[:,ch_ids]

#split the data into training and test
split = int(0.9*data.shape[0])
training_data, test_data        = data[:split,:], data[split:,:]
#split off the labels
training_data, training_labels  = training_data[:,:-1], training_data[:,-1:]
test_data, test_labels          = test_data[:,:-1], test_data[:,-1:]



#define keras model
model = Seq()
model.add(BatchNormalization())
#model.add(Dropout(0.3))
model.add(Dense(8, input_dim=40, activation='sigmoid'))
model.add(Dense(8, activation='sigmoid'))
model.add(Dense(6, activation='sigmoid'))
model.add(Dense(4, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
model.fit(training_data, training_labels, epochs=50, batch_size=30)
print()
print("Model Performance")
model.evaluate(test_data, test_labels)
predictions = model.predict_on_batch(test_data)
predictlabel= np.concatenate((predictions,test_labels),axis=1)

#Looking at weights
# for layer in model.layers:
#     print(layer.get_weights()[0])
#     print()