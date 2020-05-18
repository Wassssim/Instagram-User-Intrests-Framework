import requests


class ImageKeyWords:
    def __init__(self,filepath,filename,image_url):
      self.filepath = filepath
      self.filename = filename
      self.image_url=image_url
      self.client_id = 'm3l4FsAqqRAibgahWCggyZnO'
      self.client_secret = 'hA7TsgAOul2B3aiPH1WAnAWC0TXejAbxeD39ZspPWTf2eKns'

     
    def getKeyWords_of_uploaded_image(self):
        with open(self.filepath,'rb') as image:
                data = {'data': image}
                params={'num_keywords':3}
                response = requests.get('https://api.everypixel.com/v1/keywords',params=params,files=data, auth=(self.client_id,self.client_secret)).json()
                print(self.filename+":")
                print(response)
        return response
    
    
    
    
    def getKeyWords_of_image_with_url(self):
        params = {'url':self.image_url , 'num_keywords': 4}
        response = requests.get('https://api.everypixel.com/v1/keywords', params=params, auth=(self.client_id,self.client_secret)).json()
        return response
     
        