import tensorflow
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.layers import Dropout, Flatten, Dense, BatchNormalization ,GlobalAveragePooling2D

from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.callbacks import ModelCheckpoint

from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input

from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import tensorflow as tf

import json
import pandas as pd
import re

from os import listdir
from os.path import isfile,join,isdir
from sklearn.utils import shuffle

import seaborn as sns

from pylab import rcParams

import matplotlib.pyplot as plt

from matplotlib import rc

class CnnModel:
    
    def __init__(self,class_names,model_path,test_data = None):
        self.class_names =class_names
        self.model_path=model_path
        self.test_data=test_data
        tf.autograph.set_verbosity(10, True)
    img_width=224; img_height=224
    batch_size=1
    
    
    def visualise_data(self):
        
        sns.set(style='whitegrid', palette='muted', font_scale=1.2)
        
        HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#ADFF02", "#8F00FF"]
        
        sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))
        
        rcParams['figure.figsize'] = 12, 8
        
        sns.countplot(self.test_data.interests)
        plt.xlabel('review interest')
            
    def create_generator(self):
        
        test=self.test_data
        test_datagen=ImageDataGenerator(rescale=1.0/255.0)
        
        test_generator=test_datagen.flow_from_dataframe(
          dataframe=test,
          x_col="images",
          y_col=None,
          batch_size=self.batch_size,
          seed=42,
          shuffle=False,
          class_mode=None)
        return test_generator
    
    def setData(self, data):
        self.test_data = data

    def load_model(self):
        print(self.model_path)
        print(tf.__version__)
        model=tensorflow.keras.models.load_model(self.model_path)
        model.summary()
        return model
    
    def getPrediction(self,model,test_generator):
        prediction = model.predict(test_generator,verbose=1)
        return prediction

        
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    