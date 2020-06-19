from scrapper import Scrapper
from dataProcessor import DataProcessor
from cnnModel import CnnModel
import os
import numpy as np
import tensorflow as tf
import tensorflow as tf
import timeit

class Tester:
    
    def test(self,username,threshold):
        scrapper=Scrapper()
        folder_path=scrapper.dowload_data(username,threshold)
        dataProcessor=DataProcessor(folder_path)
        data=dataProcessor.create_dataframe_input()
        #print(data)
        class_names=['food and drink', 'entertainment', 'business and industry', 'family and relationships', 'fitness and wellness', 'hobbies and activities', 'shopping and  fashion', 'sports and outdoors', 'technology']
        model_path="./last_cnn_model.h5"
        cnnModel=CnnModel(class_names,model_path,data)
        model=cnnModel.load_model()
        test_generator=cnnModel.create_generator()
        prediction=cnnModel.getPrediction(model,test_generator)
        result=np.sum(prediction,axis=0)
        result*=(1/len(prediction))
        return result



tester=Tester();
predictions=tester.test("cat",5)
print(predictions)

