from my_credantials import path_to_cache_folder
from context import Instagram # pylint: disable=no-name-in-module
import urllib.request
import time
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

def connect():
    global account_flag
    username , password=get_account()
    print(account_flag)
    instagram = Instagram()
    instagram.with_credentials(username, password, path_to_cache_folder)
    instagram = Instagram()
    print("connected")
    return instagram


if __name__=="__main__":
    #get_account()
    for i in range (0,6):
        connect()
        time.sleep(3)

    """
    instagram=connect()
    account = instagram.get_account('kevin')
    print(account)
    """