import json
import pandas as pd
import re

def get_dataframe(filename):
    try:
        df=pd.read_csv(filename, index_col=0)
        return df
    except Exception as e:
            print(e)

