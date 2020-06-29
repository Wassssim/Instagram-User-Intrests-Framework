from context import Instagram 
from image import Image
import PyQt5.QtCore as QtCore


class Scrapper:
    
    def dowload_data(self,username,threshold):
        instagram = Instagram()
        medias = instagram.get_medias(username, threshold)
        dirName=""
        for media in medias:
            QtCore.QCoreApplication.processEvents() 
            media = instagram.get_media_by_url(media.link)
            image =Image(media) 
            dirName=image.saveImage()
        return dirName
            
