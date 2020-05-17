from my_credantials import path_to_cache_folder
from context import Instagram # pylint: disable=no-name-in-module
import urllib.request

connection_pool={
    "b43a9c43e2":"b43a9c43e2@emailmonkey.club",
    "f49e9c0744":"f49e9c0744@emailmonkey.club",
    "999efb85d6":"999efb85d6@emailmonkey.club"
}

account_flag=0

def get_account(account_flag=account_flag):
    #
    # username,password=connection_pool.values()[0]
    print(account_flag)
    print(connection_pool.values())
    account_flag=(account_flag+1)%3
    #return username,password

def connect(username,password,path_to_cache_folder):
    instagram = Instagram()
    instagram.with_credentials(username, password, path_to_cache_folder)
    instagram = Instagram()
    return instagram
if __name__=="__main__":
    for i in range (0,6):
        get_account()
    #    print (get_account())
    """
    instagram=connect()
    account = instagram.get_account('kevin')
    print(account)
    """