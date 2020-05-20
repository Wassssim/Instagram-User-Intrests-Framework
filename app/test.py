import json
import pandas as pd
import re

if __name__ == "__main__":
    dff=pd.read_csv("../dataset/collected_data/Test.csv", index_col=0)
    df1 = pd.DataFrame(data = [['a'],['b'],['c']], columns=['X'])
    #df = df1.append(df2, ignore_index = True)
    df1.index.name = 'foo'
    #df1.to_csv("../dataset/collected_data/Test.csv")
    print(df1)
    print()
    print(dff.append(df1, ignore_index = True))