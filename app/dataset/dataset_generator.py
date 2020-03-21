from context import Instagram
import pickle
import re

instagram = Instagram()

def deEmojify(inputString): #remove emojis 
    return inputString.encode('ascii', 'ignore').decode('ascii')

def generateDataset(input_filename):
    file = open(input_filename, "r", encoding = "utf-8")
    Lines = file.readlines()
    #print(Lines)
    print ('scrapping...')
    for line in Lines:
        if re.match(r"^.+:$", line): #new interest category
            if 'category_file' in locals(): #if local variable exists
                category_file.close()
            filename = line[:-1].lower()+".txt"
            category_file = open(filename, "w", encoding = "utf-8")
        else:
            account = line[:-1].split(' ')
            medias = instagram.get_medias(account[0], int(account[1]))
            for media in medias:
                if(media.caption):
                    category_file.write(str(deEmojify(media.caption).replace('\n', ' ') + '\n'))
        


try:
    generateDataset("account_names.txt")
    print("Dataset generated")
except Exception as e:
    print(e)