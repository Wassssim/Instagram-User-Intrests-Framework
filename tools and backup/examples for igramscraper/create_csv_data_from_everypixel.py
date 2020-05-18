
#import computerVision
import csv
import pandas as pd



username="techomg"
number_of_images=3

#result=get_keywords_of_images_with_url(username,number_of_images)
result=['hh iii pppp','michou uuuu ththth','sikimisation']
print(result)
my_dict = {'username':['fgbfg'],'postnumber':['gggg'],'content':['content'],'interest':['tech']}
df = pd.DataFrame(my_dict)
df.to_csv('dataset.csv')
interest='technology'

with open('dataset.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    for index, content in enumerate(result, start=0):
        writer.writerow([index+1,username,index,content,interest])



