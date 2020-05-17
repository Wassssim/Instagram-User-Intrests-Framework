import os
from imageKeywords import ImageKeyWords

#this file is for getting keywords  of user's images
username="catpipie2"
directory=os.path.join("./images",(str)(username));
if  os.path.exists(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            filepath=os.path.join(directory, filename)
            response=ImageKeyWords(filepath,filename).getKeyWords();
            print(filename+":::")
            for keyword in response['keywords']:
                key,score=keyword['keyword'],keyword['score']
                print(key+":")
                print(score)
            continue
        else:
            continue