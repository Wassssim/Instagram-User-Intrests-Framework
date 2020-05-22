import json
import pandas as pd
import hashtags as ht
import re
interest = 'technology'
filename=interest+".csv"
def merge():
    pass
def retrieve_data(filename):
    try:
        df=pd.read_csv(filename)
        #print(df.head())
        return df
    except Exception as e:
            print(e)

def clean_data(df):
    df.drop_duplicates(keep=False,inplace=True) 
    df_filtered = df[df['interest']==str.lower(interest)] 
    #df['interest']="business"
    #print(df.head())
    return df


if __name__=="__main__":
    data=retrieve_data(filename)
    clean_data=clean_data(data)
    print(clean_data.head())
    clean_data.to_csv(filename)    
    print("all good")
    