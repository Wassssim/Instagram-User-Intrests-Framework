import json
import pandas as pd
import hashtags as ht
import re

def retrieve_data(filename):
    try:
        df=pd.read_csv(filename)
        return df
    except Exception as e:
            print(e)
