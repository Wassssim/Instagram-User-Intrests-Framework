from context import Instagram
import pandas as pd
from caption_formater import extract_hash_tags , remove_hash_tags , deEmojify
import igramscraper
import progressbar

instagram = Instagram()
columns = {"photo_url": 0, "captions": 1, "hashtags": 2}


def create_post(media, columns):
    post = [0 for i in columns.keys()]
    post[columns['photo_url']] = str(media.image_high_resolution_url) #high_res
    caption = None
    caption = deEmojify(media.caption)
    post[columns['captions']] = remove_hash_tags(caption)
    post[columns['hashtags']] = extract_hash_tags(caption)
    return post

def get_medias(account,mx):
    try :
        account_attributes = instagram.get_account(account)
        media_count = account_attributes.media_count
        post_number = min(media_count,mx)
        medias = instagram.get_medias(account, post_number)
        print("media count"+str(media_count))
        #sleep(30)
        return medias
    except igramscraper.exception.instagram_exception.InstagramException as e :
        print(e)
        return []
        
    except Exception as e:
        print(e)
        return []

def laod_data_into_dataframe(data):
    new_dataframe = pd.DataFrame(data=data, columns=columns)
    return new_dataframe


def generate_test_data(account, threshold = 1000):
    data=[]
    medias=get_medias(account, threshold)
    if medias!=[]:
        print("account name : "+account+"\n")            
        with progressbar.ProgressBar(max_value=len(medias)) as bar:
            for i in range(len(medias)):
                post = create_post(medias[i], columns)
                data.append(post)
        df=laod_data_into_dataframe(data)
        print("Dataframe generated")
        return df
    return None

if __name__=="__main__":
    account="techrax"
    df = generate_test_data(account,5)
    print(df)
    