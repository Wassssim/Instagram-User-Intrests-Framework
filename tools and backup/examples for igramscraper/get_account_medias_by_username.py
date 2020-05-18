from context import Instagram # pylint: disable=no-name-in-module
from image import Image

# If account is public you can query Instagram without auth
#this files is made for downloading exact number of user's images
instagram = Instagram()

username="catpipie2"
number_of_images=2

def store_images(username,number_of_images):
    medias = instagram.get_medias(username,number_of_images)
    for media in medias:
        media = instagram.get_media_by_url(media.link)
        image =Image(media) 
        image.saveImage()
        print(medias[1])
        account = medias[1].owner
        print(account)










# print('Username', account.username)
# print('Full Name', account.full_name)
# print('Profile Pic Url', account.get_profile_picture_url_hd())


# If account private you should be subscribed and after auth it will be available

# username = ''
# password = ''
# session_folder = ''
# instagram = Instagram()
# instagram.with_credentials(username, password, session_folder)
# instagram = Instagram()
# instagram.login()
# instagram.get_medias('private_account', 100)
