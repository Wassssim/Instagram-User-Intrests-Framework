import json
import pandas as pd
import hashtags as ht
import re
filename = 'Entertainment.csv'

def retrieve_data(filename):
    try:
        df=pd.read_csv(filename)
        return df
    except Exception as e:
            print(e)

def clean_data():
    #print(df.captions.apply(ht.remove_hashtags(lambda x : remove_hashtags(str(x)))))
    df=retrieve_data(filename)
    df['captions'] = df['captions'].apply(lambda x: ht.remove_hashtags(x))
    df.to_csv(filename)

if __name__=="__main__":
    clean_data()
    print("all good")
    