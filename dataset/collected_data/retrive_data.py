import json
import pandas as pd
file = 'Fitness.json'
with open(file) as train_file:
    dict_train = json.load(train_file)

# converting json dataset from dictionary to dataframe
train = pd.DataFrame.from_dict(dict_train, orient='index')
train.reset_index(level=0, inplace=True)
print(train)
train.to_csv('Fitness.csv',index=False,header=True)