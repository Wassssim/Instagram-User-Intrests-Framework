import json
import pandas as pd
import re
from os import listdir
from os.path import isfile,join
from sklearn.utils import shuffle

dataset_path="../dataset/collected_data/"
column_names=["captions","hashtags","photo_url","interests"]    

def get_all_files(my_path):
    onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    return onlyfiles


def retrieve_data(filename):
    try:
        df=pd.read_csv(filename)
        #print(df.head())
        return df
    except Exception as e:
            print(e)


def merge_dataset(df_list):
    pass

def suffle_dataset(df):
    df = shuffle(df)
    return df

def set_threshhold(df,threshhold):
    df = df.head(threshhold)
    return df 
    
def generate_model_data(threshhold):
    model_data=pd.DataFrame(columns=column_names)
    files = get_all_files(dataset_path)
    for _file in files :
        print(_file) 
        _file=dataset_path+_file
        df =    retrieve_data(_file)
        shuffle(df)
        df = set_threshhold(df,threshhold)
        model_data = model_data.append(df, ignore_index = True)
    print(model_data)

def save_data(clean_data,filename):
    clean_data.to_csv(filename)    
    
if __name__=="__main__":
    threshhold=1000
    generate_model_data(1000)