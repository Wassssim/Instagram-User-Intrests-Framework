import json
import pandas as pd
import re
from os import listdir
from os.path import isfile,join

def get_dataframe(filename):
    try:
        df=pd.read_csv(filename, index_col=0)
        return df
    except Exception as e:
            print(e)
def get_all_files(my_path):
    onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    return onlyfiles
