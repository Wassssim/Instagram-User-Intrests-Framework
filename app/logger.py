from my_credantials import path_to_cache_folder
from context import Instagram # pylint: disable=no-name-in-module
import urllib.request
account_flag = 0

connection_pool={
    "b43a9c43e2":"b43a9c43e2@emailmonkey.club",
    "f49e9c0744":"f49e9c0744@emailmonkey.club",
    "999efb85d6":"999efb85d6@emailmonkey.club"
}


def get_account():
    #
    # username,password=connection_pool.values()[0]
    global account_flag
    #print(account_flag)
    usernames=list(connection_pool.keys())
    passwords=list(connection_pool.values())
    #print(keys)
    username=usernames[account_flag]
    password=passwords[account_flag]
    account_flag=(account_flag+1)%3
    return username,password

def connect(username,password,path_to_cache_folder):
    instagram = Instagram()
    instagram.with_credentials(username, password, path_to_cache_folder)
    instagram = Instagram()
    return instagram
if __name__=="__main__":
    #get_account()
    for i in range (0,6):
        print (get_account())
    """
    instagram=connect()
    account = instagram.get_account('kevin')
    print(account)
    """