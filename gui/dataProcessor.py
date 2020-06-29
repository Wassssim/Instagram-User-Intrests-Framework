import json
import pandas as pd
import re
import PyQt5.QtCore as QtCore

from os import listdir
from os.path import isfile,join,isdir
from sklearn.utils import shuffle


class DataProcessor:
    
    def __init__(self,path):
      self.dataset_path = path
    
    #dataset_path="/content/drive/My Drive/interest_dataset_folder/data/images"
    column_names=["captions","hashtags","photo_url","interests"]    
    
    DEFAULT_THRESHHOLD=100
    
    def get_all_files(self,my_path):
        onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
        return onlyfiles
    
    def get_all_directories(self,my_path):
        onlyfiles = [f for f in listdir(my_path) if isdir(join(my_path, f))]
        return onlyfiles
    
    
    def retrieve_data(self,filename):
        try:
            df=pd.read_csv(filename)
            #print(df.head())
            return df
        except Exception as e:
                print(e)
    
    
    def merge_dataset(df_list):
        pass
    
    def suffle_dataset(self,df):
        df = shuffle(df)
        return df
    
    def set_threshhold(self,df,threshhold=DEFAULT_THRESHHOLD,use_threshhold=False):
        if use_threshhold:
          df = df.head(threshhold)
        return df 
        
    def generate_model_data(self,threshhold=DEFAULT_THRESHHOLD,use_threshhold=False):
        model_data=pd.DataFrame(columns=self.column_names)
        files =self.get_all_files(self.dataset_path)
        for _file in files :
            #print(_file) 
            _file=self.dataset_path+_file
            df = self.retrieve_data(_file)
            #shuffle(df)
            df =self.set_threshhold(df,threshhold,use_threshhold)
            model_data = model_data.append(df, ignore_index = True)
            
        model_data = model_data[['photo_url','captions','hashtags','interest']]
        return model_data
    
    
    def save_data(clean_data,filename):
        clean_data.to_csv(filename)

    def create_dataframe_input(self):
        IMAGES_PATH=self.dataset_path+"/"
        rows=[]
        row={"images":"","interests":""}
        print(IMAGES_PATH)
        all_images=self.get_all_files(IMAGES_PATH)
        for image in all_images:
            QtCore.QCoreApplication.processEvents() 
            image_path=IMAGES_PATH+image
            row['images']=image_path
            row['interests']="unknown"
            rows.append(row)
        data=pd.DataFrame(rows)
        data.info()
        return data

