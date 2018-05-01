
#This code is incomplete

import numpy as np
np.random.seed(1)
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.utils import np_utils
from keras.applications import InceptionV3

import cv2

import sys
import csv

def main(argv):
    try:
        myDict = frame_to_input_map(argv[1])
    except:
        print("Filename needed")
        return False
    
    #This bit is basically verbaitum from https://youtu.be/5DknTFbcGVM
    #Not attempting to plagerize, but what they're doing is similiar enough
    #To what we're doing that I don't want to reinvent the wheel here
    
    frames = keras.Input(shape=(None, 400, 240, 3), name='frames')
    cnn = InceptionV3(weights='imagenet', include_top=False, pooling=None)
    cnn.trainable = False
    frame_features = keras.layers.TimeDistributed(cnn)(frames)
    
    model = Sequential([
            frame_features,
            LSTM(6), #<w a s d j k>
            Activation('relu'),
    ])
    
    model.compile(optimizer='rmsprop', 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'],
    )

    

def frame_to_input_map(dir_name):
    out_dict = {}
    try:
        with open('{0}/inputlog.csv'.format(dir_name)) as input_log:
            input_log_csv = csv.DictReader(input_log)
            for row in input_log_csv:
                out_dict[row['frame']] = row['input']
    except:
        print("Directory not found or malformed")
        return None
    
    return out_dict

if __name__ is "__main__":
    main(sys.argv)