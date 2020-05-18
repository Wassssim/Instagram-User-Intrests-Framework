import os
from imageKeywords import ImageKeyWords
from context import Instagram # pylint: disable=no-name-in-module


#this file is for getting keywords  of user's images
username="catpipie2"
instagram = Instagram()

'''
def get_keywords_of_local_images(username):
    directory=os.path.join("./images",(str)(username));
    if  os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                filepath=os.path.join(directory, filename)
                response=ImageKeyWords(filepath,filename,'').getKeyWords_of_uploaded_image();
                print(filename+":::")
                for keyword in response['keywords']:
                    key,score=keyword['keyword'],keyword['score']
                    print(key+":")
                    print(score)
                continue
            else:
                continue

'''


def get_keywords_of_images_with_url(username,number_of_images):
    medias = instagram.get_medias(username,number_of_images)
    result=[]
    for media in medias:
        image_url =media.image_high_resolution_url
        response=ImageKeyWords('','',image_url).getKeyWords_of_image_with_url();
        print("the response from every_pixel")
        print(response)
        return 
        concatenated_keywords=""
        for keyword in response['keywords']:
            key,score=keyword['keyword'],keyword['score']
           # print(key+":")
            #print(score) 
            concatenated_keywords+=key
            concatenated_keywords+="  "
        
        result.append(concatenated_keywords)
    
    return result
        
            
        

username="catpipie2"
number_of_images=3
#result=get_keywords_of_images_with_url(username,number_of_images)