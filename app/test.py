import json
import pandas as pd
import re

if __name__ == "__main__":
    df1 = pd.DataFrame(data = [['a'],['b'],['c']])
    df2 = pd.DataFrame(data = [['a'],['b'],['c']])
    df = df1.append(df2, ignore_index = True)
    print(df)