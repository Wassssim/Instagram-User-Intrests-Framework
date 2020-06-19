from context import Instagram 
from image import Image


class Scrapper:
    
    def dowload_data(self,username,threshold):
        instagram = Instagram()
        medias = instagram.get_medias(username, threshold)
        dirName=""
        for media in medias:
            media = instagram.get_media_by_url(media.link)
            image =Image(media) 
            dirName=image.saveImage()
        return dirName
            
