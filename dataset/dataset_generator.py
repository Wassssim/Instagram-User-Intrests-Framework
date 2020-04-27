from context import Instagram
import pickle
import re
import json

instagram = Instagram()
dataset = {}

def extract_hash_tags(s):
    return list(set(part[1:] for part in s.split() if part.startswith('#')))

def remove_hash_tags(s):
    return ' '.join(re.sub(" #[A-Za-z0-9_]+"," ",s).split())

def deEmojify(inputString): #remove emojis
    if(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')
    return ''

def generateDataset(input_filename):
    file = open(input_filename, "r", encoding = "utf-8")
    Lines = file.readlines()
    #print(Lines)
    print ('scrapping...')
    interest = ""
    for line in Lines:
        if re.match(r"^.+:$", line): #new interest category
            interest = line[:-1].lower()
        else:
            account = line[:-1].split(' ')
            medias = instagram.get_medias(account[0], int(account[1]))
            user = {}
            user['interest'] = interest
            for i in range(len(medias)):
                user['post'+str(i)] = {}
                user['post'+str(i)]['photo_url'] = medias[i].image_high_resolution_url #high_res
                caption = None
                caption = deEmojify(medias[i].caption)
                user['post'+str(i)]['caption'] = remove_hash_tags(caption)
                user['post'+str(i)]['hashtags'] = extract_hash_tags(caption)
                user['post'+str(i)]['comments'] = medias[i].comments_count
            dataset[account[0]] = user
    file.close()


try:
    generateDataset("account_names.txt")
    print("Dataset generated")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent = 4)
except Exception as e:
    print(e)




#print(media.__dict__)



#Problems:
#high_res image always available?
#hash tag functions testing