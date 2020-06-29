from scrapper import Scrapper
from dataProcessor import DataProcessor
from cnnModel import CnnModel
import os
import numpy as np
scrapper=Scrapper()
username="cat"
threshold=3
folder_path=scrapper.dowload_data(username,threshold)
dataProcessor=DataProcessor(folder_path)
data=dataProcessor.create_dataframe_input()
print(data)
class_names=['food and drink', 'entertainment', 'business and industry', 'family and relationships', 'fitness and wellness', 'hobbies and activities', 'shopping and  fashion', 'sports and outdoors', 'technology']
model_path="./last_cnn_model.h5"
cnnModel=CnnModel(class_names,model_path,data)
#cnnModel.visualise_data()
model=cnnModel.load_model()
test_generator=cnnModel.create_generator()
prediction=cnnModel.getPrediction(model,test_generator)
print(prediction)
#prediction=[[0.2,0.5,0.3],[0.4,0.3,0.3]]
result=np.sum(prediction,axis=0)
result*=(1/len(prediction))
print(result)
