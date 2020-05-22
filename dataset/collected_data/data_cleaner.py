import json
import pandas as pd
import hashtags as ht
import re
interest = 'technology'
filename=interest+".csv"
def get_filename(interest):
    filename=interest+".csv"
    return filename

def output_interest(interest_1,interest_2):
    output=interest_1+" and "+interest_2
    return output

def merge(interest_1,interest_2):
    filename_1=get_filename(interest_1)
    filename_2=get_filename(interest_2)
    df1=retrieve_data(filename_1)
    df2=retrieve_data(filename_2)
    df = df1.append(df2, ignore_index = True)
    my_interest= output_interest(interest_1,interest_2)    
    df['interest']=my_interest
    saving_file=get_filename(my_interest)
    save_data(df,saving_file)
    print(df)

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

def save_data(clean_data,filename):
    clean_data.to_csv(filename)    
    
if __name__=="__main__":
    #data=retrieve_data(filename)
    #clean_data=clean_data(data)
    #print(clean_data.head())
    #clean_data.to_csv(filename)    
    interest_1="Business"
    interest_2="Industry"
    merge(interest_1,interest_2)
    print("all good")
    