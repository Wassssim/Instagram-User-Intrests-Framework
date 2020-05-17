import requests


class ImageKeyWords:
    def __init__(self,filepath,filename):
      self.filepath = filepath
      self.filename = filename
      self.client_id = 'm3l4FsAqqRAibgahWCggyZnO'
      self.client_secret = 'hA7TsgAOul2B3aiPH1WAnAWC0TXejAbxeD39ZspPWTf2eKns'
     
    def getKeyWords(self):
        with open(self.filepath,'rb') as image:
                data = {'data': image}
                params={'num_keywords':3}
                response = requests.get('https://api.everypixel.com/v1/keywords',params=params,files=data, auth=(self.client_id,self.client_secret)).json()
                print(self.filename+":")
                print(response)
        return response
     
        