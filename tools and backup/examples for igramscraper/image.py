import os
import urllib.request

class Image:
    def __init__(self,media):
      self.media = media
      
    def saveImage(self):
        image_url =self.media.image_high_resolution_url
        ownerName=self.media.owner.username
        imageName=str(self.media.identifier)+'.jpg'
        dirName=os.path.join("./images",(str)(ownerName));
        filepath =os.path.join(dirName,imageName) 
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        urllib.request.urlretrieve(image_url,filepath)
        
    
    





