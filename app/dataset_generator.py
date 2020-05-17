from context import Instagram
import pickle
import re
import json
from os import listdir
from os.path import isfile, join

account_names_path="../dataset/account_names/"
output_path="../dataset/collected_data/"
instagram = Instagram()
dataset = {}
threshhold = 3

def get_all_files(my_path=account_names_path):
    onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    return onlyfiles

def extract_hash_tags(s):
    return list(set(part[1:] for part in s.split() if part.startswith('#')))

def remove_hash_tags(s):
    return ' '.join(re.sub(" #[A-Za-z0-9_]+"," ",s).split())

def deEmojify(inputString): #remove emojis
    if(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')
    return ''

def get_medias(account,threshhold):
    try :
        account_attributes = instagram.get_account(account)
        media_count = account_attributes.media_count
        post_number = min(media_count,threshhold)
        print(media_count)
        medias = instagram.get_medias(account, post_number)
        return medias
    except Exception as e:
        print(e)
        return None

def generateDataset(input_filename):
    file = open(input_filename, "r", encoding = "utf-8")
    Lines = file.readlines()
    #print(Lines)
    print ('scrapping...')
    interest = input_filename.replace(account_names_path,'')
    for line in Lines:
        account = line[:-1].split(' ')[0]
            
        medias=get_medias(account,threshhold)
        #______________________ We got Medias
        if medias!=None :
            user = {}
            user['interest'] = interest
            ## Logging account 
            print("interest : "+interest+"\n")
            print("account name : "+account+"\n")
            for i in range(len(medias)):
                #Filling Dict
                user['post'+str(i)] = {}
                user['post'+str(i)]['photo_url'] = medias[i].image_high_resolution_url #high_res
                caption = None
                caption = deEmojify(medias[i].caption)
                user['post'+str(i)]['caption'] = remove_hash_tags(caption)
                user['post'+str(i)]['hashtags'] = extract_hash_tags(caption)
                user['post'+str(i)]['comments'] = medias[i].comments_count
                ## Logging Post Number 
                print("post :"+str(i))
            dataset[account] = user
    file.close()
    return interest

if __name__=="__main__":
    #input_files = get_all_files( )
    input_files=['Technology']
    for input_file in input_files :
        input_file_added_to_path=account_names_path+input_file
        print(input_file_added_to_path )
        try:
            interest=generateDataset(input_file_added_to_path)
            print("Dataset generated")
            output_file=input_file+".json"
            output_file_added_to_path=output_path+output_file
            with open(output_file_added_to_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent = 4)
            dataset={}
        except Exception as e:
            print(e)


#Problems:
#high_res image always available?
#hash tag functions testing