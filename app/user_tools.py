from my_credantials import username , password , path_to_cache_folder
from context import Instagram # pylint: disable=no-name-in-module
import urllib.request

#Login Singleton
class Meta_Logger:
    instagram=None
    def __init__(self):
        print("initializing Meta Logger")
        Meta_Logger.instagram = Instagram()
        Meta_Logger.instagram.with_credentials(username, password, path_to_cache_folder)
        Meta_Logger.instagram.login()

class Logger():
   __instance = None
   @staticmethod 
   def getInstance():
      """ Static access method. """
      if Logger.__instance == None:
         Logger()
      print("returning Singleton")
      return Logger.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if Logger.__instance != None:
         raise Exception("This class is a singleton!")
      else:
        print("initializing Logger")
        Logger.__instance = Meta_Logger ()

def __get_media_by_url(url):
    #instagram = Instagram()
    instagram=Logger.getInstance().instagram
    media = instagram.get_media_by_url(url)
    print(media)
    print(media.owner)
def __get_account_medias_by_username(username):
    instagram = Instagram()

    medias = instagram.get_medias(username, )
    media = medias[6]

    print(media)
    
    account = media.owner
    print(account)
    return media 
def __get_media_comments(id):
    instagram=Logger.getInstance().instagram
    comments = instagram.get_media_comments_by_id(id, 10000)
    for comment in comments['comments']:
        print(comment.text)
        print(comment.owner)

def __get_media_likes(code):
    instagram=Logger.getInstance().instagram
    likes = instagram.get_media_likes_by_code(code, 100)
    print("Result count: " + str(len(likes['accounts'])))
    for like in likes['accounts']:
        print(like)
def __get_account_by_username(username,number_of_medias):
    instagram=Logger.getInstance().instagram
    medias = instagram.get_medias(username, number_of_medias)
    media = medias[6]
    print(medias)   
    account = media.owner
    print(account)


__get_account_by_username("natgeo",1000)