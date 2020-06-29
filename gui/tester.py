from dataProcessor import DataProcessor
from cnnModel import CnnModel
import os
import numpy as np
import tensorflow as tf
import timeit

class Tester:
    
    def test(self, folder_path, cnnModel, model):
        dataProcessor=DataProcessor(folder_path)
        data=dataProcessor.create_dataframe_input()
        class_names=['food and drink', 'entertainment', 'business and industry', 'family and relationships', 'fitness and wellness', 'hobbies and activities', 'shopping and  fashion', 'sports and outdoors', 'technology']
        """#print(data)
        class_names=['food and drink', 'entertainment', 'business and industry', 'family and relationships', 'fitness and wellness', 'hobbies and activities', 'shopping and  fashion', 'sports and outdoors', 'technology']
        model_path="./last_cnn_model.h5"
        cnnModel=CnnModel(class_names,model_path,data)
        #cnnModel.visualise_data()
        model=cnnModel.load_model()"""
        cnnModel.setData(data)
        test_generator=cnnModel.create_generator()
        prediction=cnnModel.getPrediction(model,test_generator)
        #print(prediction)
        #prediction=[[0.2,0.5,0.3],[0.4,0.3,0.3]]
        result=np.sum(prediction,axis=0)
        result*=(1/len(prediction))
        #print(result)
        return result, class_names


if __name__=="__main__":
    tester=Tester()
    predictions, classnames = tester.test("foodcookery",50, "")
    print(predictions)
    print(classnames)
    print(predictions.sum())

