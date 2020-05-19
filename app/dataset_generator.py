from context import Instagram
import pickle
import re
import json
from os import listdir
from os.path import isfile, join
from time import sleep
import pandas as pd
from caption_formater import extract_hash_tags , remove_hash_tags , deEmojify
from logger import connect
import igramscraper
from retrive_data import get_dataframe
account_names_path="../dataset/account_names/"
output_path="../dataset/collected_data/"
instagram = Instagram()
threshhold = 3000
columns = {"photo_url": 0, "captions": 1, "hashtags": 2, "interest": 3}
data = []

def get_all_files(my_path):
    onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    return onlyfiles


    

def get_medias(account,threshhold,current_file_start_index,current_index):
    try :
        
        account_attributes = instagram.get_account(account)
        media_count = account_attributes.media_count
        post_number = min(media_count,threshhold)
        print(media_count)
        medias = instagram.get_medias(account, post_number)
        #sleep(30)
        return medias
    except igramscraper.exception.instagram_exception.InstagramException :
        """
            when recieving this exception we save the current_index which represents 
            the last non processed index so we process it in next iteration

        """
        #YOUR CODE HERE
        checkpoint_file=open('./checkpoint.txt','w')
        checkpoint_file.truncate(0)
        current_file_start_index=str(current_file_start_index)+'\n'
        current_index=str(current_index)
        checkpoint_file.write(current_file_start_index)
        checkpoint_file.write(current_index)
        return None
        
    except Exception as e:
        print(e)
        return None
    """
        ---Here We tried Handling this exception by creating a session pool 
        It didn't work

    except igramscraper.exception.instagram_exception.InstagramException :
        try:
            instagram=connect()  
            account_attributes = instagram.get_account(account)
            media_count = account_attributes.media_count
            post_number = min(media_count,threshhold)
            print(media_count)
            medias = instagram.get_medias(account, post_number)
            #sleep(30)
            
            return medias 
        except Exception as e:
            print(e)
            return None
    """
    


def create_post(media, columns, interest):
    post = [0 for i in columns.keys()]
    post[columns['interest']] = str(interest).lower()
    post[columns['photo_url']] = str(media.image_high_resolution_url) #high_res
    caption = None
    caption = deEmojify(media.caption)
    post[columns['captions']] = remove_hash_tags(caption)
    post[columns['hashtags']] = extract_hash_tags(caption)
    return post



def generateDataset(input_filename,current_file_start_index,start_index):
    file = open(input_filename, "r", encoding = "utf-8")
    Lines = file.readlines()
    #print(Lines)
    print ('scrapping...')
    interest = input_filename.replace(account_names_path,'')
    current_index=start_index
    
    if int(current_index)>= len(Lines):
        current_file_start_index=current_file_start_index+1
        current_index=str(0)
        current_file_start_index=str(current_file_start_index)+'\n'
        checkpoint_file=open('./checkpoint.txt','w')
        checkpoint_file.truncate(0)
        checkpoint_file.write(current_file_start_index)
        checkpoint_file.write(current_index)
        return 
    
    
    for line in Lines[start_index:]:
        account = line[:-1].split(' ')[0]  
        post = []
        medias=get_medias(account,threshhold,current_file_start_index,current_index)
        #______________________ We got Medias
        if medias!=None:
            current_index=current_index+1
            ## Logging account 
            print("interest : "+interest+"\n")
            print("account name : "+account+"\n")            
            for i in range(len(medias)):
                #Creating a new row
                post = create_post(medias[i], columns, interest)
                ## Logging Post Number 
                print("post :"+str(i))
                data.append(post)
            #dataset[account] = user
        else:
            break
            
    if int(current_index)>= len(Lines):
        '''if all medias of this interest are dowloaded initialise 
            the start_index and file_start_index in checkpoint file'''
            
        current_file_start_index=current_file_start_index+1
        current_index=str(0)
        current_file_start_index=str(current_file_start_index)+'\n'
        checkpoint_file=open('./checkpoint.txt','w')
        checkpoint_file.truncate(0)
        checkpoint_file.write(current_file_start_index)
        checkpoint_file.write(current_index)
    
    file.close()
    return interest
def laod_data_into_dataframe(start_index,output_file_added_to_path):
    new_dataframe = pd.DataFrame(data=data, columns=columns)
    if (isfile(output_file_added_to_path)):
        df = get_dataframe(output_file_added_to_path)
        df.append(new_dataframe, ignore_index = True)
        return df
    else :
        return new_dataframe


def make_output_file(input_file):
    output_file=input_file+".csv"
    output_file_added_to_path=output_path+output_file
    return output_file_added_to_path        

          
if __name__=="__main__":
    #input_files = get_all_files()
    #input_files = get_all_files(account_names_path)
    input_files = ['Entertainment']
    #Use Second Line In case you want to get all files
    #input_files=["shopping and  fashion"]
    ''' we will retrieve name last_file processed with it's start_index from checkpoint file'''
    checkPoint_file = open('./checkpoint.txt', "r", encoding = "utf-8")
    Lines = checkPoint_file.readlines()
    file_start_index=0
    start_index=0
    if len(Lines)==2:
        '''get file_start_undex and start_index from checkpoint file'''
        file_start_index=int(Lines[0])
        start_index=int(Lines[1])
    print(file_start_index)   
    print(start_index)
    #input_files=["shopping and  fashion"]
    #print(input_files)
    current_file_start_index=file_start_index
    if current_file_start_index >= len(input_files):
        exit()
    for input_file in input_files[file_start_index:] :
        
        input_file_added_to_path=account_names_path+input_file
        print(input_file_added_to_path )
        try:
            '''  if it's not the first iteration we should retrieve start_index '''
            checkPoint_file = open('./checkpoint.txt', "r", encoding = "utf-8")
            Lines = checkPoint_file.readlines()
            start_index=0
            if len(Lines)==2:
                start_index=Lines[1]
            start_index=int(start_index)
            interest=generateDataset(input_file_added_to_path,current_file_start_index,start_index)
            
            ouput_file=make_output_file(input_file)
            df=laod_data_into_dataframe(start_index,output_file)
            print("Dataset generated")
            print(df.info())
            #with open(output_file_added_to_path, 'w', encoding='utf-8') as f:
            df.to_csv(output_file)
            
        except Exception as e:
            print(e)
    
        current_file_start_index=current_file_start_index+1

#Problems:
#high_res image always available?
#hash tag functions testing