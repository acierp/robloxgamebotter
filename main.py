from roblox import Roblox, RobloxClientMutex
from time import sleep
import time
import threading
from threading import Thread
import random
import requests
import json
from itertools import cycle

mutex = RobloxClientMutex()

with open("cookies.txt", 'r+', encoding='utf-8') as f:
    cookies = f.read().splitlines()

with open('proxies.txt','r+', encoding='utf-8') as f:
	ProxyPool = cycle(f.read().splitlines())

with open('config.json','r+', encoding='utf-8') as f:
    config = json.load(f)

threads = config['threads']


messagesrealtosend = open('messages.txt').read().splitlines()
mymessage = random.choice(messagesrealtosend)

def get_session():
    while 1:
        try:
            cookie = random.choice(cookies)
            session = Roblox(cookie)
            return session
        except Exception as err:
            print(err)

def get_session_cookie(cookie):
    while 1:
        try:
            session = Roblox(cookie)
            return session
        except Exception as err:
            print(err)

def joinMessage(message, gameid):
    while 1:
        try:
            client = get_session().create_client(gameid)
            time.sleep(5)
            client.chat_message(message)
            time.sleep(1)
            client.close()
        except:
            pass

def noMessage(gameid):
    while 1:
        try:
            client = get_session().create_client(gameid)
            time.sleep(6)
            client.close()
        except:
            pass
def likeGame(cookie, gameid, proxy):
    token = getToken(cookie, proxy)
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    data = {
        "assetId": gameid,
        "vote": True
    }
    headers = {
        'x-csrf-token': token
    }
    likereq = requests.post(f'https://www.roblox.com/voting/vote?assetId={gameid}&vote=true', proxies=proxy, data=data, headers=headers, cookies=cookies)
    if likereq.status_code == 200:
        if "EmailIsVerified" in likereq.text:
            print('Account is not verified.')
        else:
            print('Sucessfully liked game.')
            print(likereq.text)
    elif likereq.status_code == 429:
        print('Ratelimited. Waiting and trying again')
        time.sleep(20)
        return likeGame(cookie, gameid, proxy)
    elif "FloodCheckThresholdMet" in likereq.text:
        print('Ratelimited. Waiting and trying again')
        time.sleep(20)
        return likeGame(cookie, gameid, proxy)
    else:
        print(likereq.text)

def dislikeGame(cookie, gameid, proxy):
    token = getToken(cookie, proxy)
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    data = {
        "assetId": gameid,
        "vote": False
    }
    headers = {
        'x-csrf-token': token
    }
    likereq = requests.post(f'https://www.roblox.com/voting/vote?assetId={gameid}&vote=false', proxies=proxy, data=data, headers=headers, cookies=cookies)
    if likereq.status_code == 200:
        if "EmailIsVerified" in likereq.text:
            print('Account is not verified.')
        else:
            print('Sucessfully disliked game.')
            print(likereq.text)
    elif likereq.status_code == 429:
        print('Ratelimited. Waiting and trying again')
        time.sleep(20)
        return dislikeGame(cookie, gameid, proxy)
    elif "FloodCheckThresholdMet" in likereq.text:
        print('Ratelimited. Waiting and trying again')
        time.sleep(20)
        return dislikeGame(cookie, gameid, proxy)
    else:
        print(likereq.text)

def getToken(cookie, proxy):
    try:
        request = requests.post("https://auth.roblox.com/v1/logout", proxies=proxy, headers={"Cookie": f".ROBLOSECURITY={cookie};"})
        if request.status_code == 200 or request.status_code == 403:
            print('Successfully updated token')
            return request.headers["x-csrf-token"]
        if request.status_code == 401:
            return "Invalid Cookie"
    except Exception as error:
        print("Unknown error occurred when attempting to update token")
        print(error)
        print(request.text)
def joinLike(gameid, proxy):
    while 1:
        try:
            cookie = random.choice(cookies)
            client = get_session_cookie(cookie).create_client(gameid)
            time.sleep(6)
            client.close()
            likeGame(cookie, gameid, proxy)
        except:
            pass
def joinDislike(gameid, proxy):
    while 1:
        try:
            cookie = random.choice(cookies)
            client = get_session_cookie(cookie).create_client(gameid)
            time.sleep(6)
            client.close()
            dislikeGame(cookie, gameid, proxy)
        except:
            pass

def joinNoLeave(gameid):
    while 1:
        try:
            client = get_session().create_client(gameid)
            time.sleep(900)
            client.close()
            print('Client was closed due to being idle for 15 minutes.')
        except:
            pass

def spamGame(gameid, message):
    while True:
        try:
            client = get_session().create_client(gameid)
            while True:
                client.chat_message(message)
                time.sleep(3)
        except:
            pass

def realPlayerjoin(gameid):
    while 1:
        try:
            client = get_session().create_client(gameid)
            while True:
                time.sleep(random.randrange(5, 20))
                mymessage = random.choice(messagesrealtosend)
                client.chat_message(mymessage)
                time.sleep(1)
                client.antiafk()
                time.sleep(random.randrange(5, 20))
        except:
            pass
    
print('''

░██████╗░░█████╗░███╗░░░███╗███████╗██████╗░░█████╗░████████╗
██╔════╝░██╔══██╗████╗░████║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝
██║░░██╗░███████║██╔████╔██║█████╗░░██████╦╝██║░░██║░░░██║░░░
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░██╔══██╗██║░░██║░░░██║░░░
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗██████╦╝╚█████╔╝░░░██║░░░
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═════╝░░╚════╝░░░░╚═╝░░░

[1] Join
[2] Join and send a message
[3] Join and like
[4] Join and dislike
[5] Join no disconnect
[6] Spam a message
[7] Join player normalizer''')

option = input('\nOption: ')
if "1" in option:
    gamelink = input('Game ID: ')
    for i in range(int(threads)):
        Thread(target=noMessage, args=[gamelink]).start()
elif "2" in option:
    gamelink = input('Game ID: ')
    messagetosend = input('Message: ')
    for i in range(int(threads)):
        Thread(target=joinMessage, args=[messagetosend, gamelink]).start()
elif "3" in option:
    gamelink = input('Game ID: ')
    for i in range(int(threads)):
        proxy = {
            "https": "https://" + next(ProxyPool)
        }
        Thread(target=joinLike, args=[gamelink, proxy]).start()
elif "4" in option:
    gamelink = input('Game ID: ')
    for i in range(int(threads)):
        proxy = {
            "https": "https://" + next(ProxyPool)
        }
        Thread(target=joinDislike, args=[gamelink, proxy]).start()
elif "5" in option:
    gamelink = input('Game ID: ')
    for i in range(int(threads)):
        Thread(target=joinNoLeave, args=[gamelink]).start()
elif "6" in option:
    gamelink = input('Game ID: ')
    message = input('Message to spam: ')
    for i in range(int(threads)):
        Thread(target=spamGame, args=[gamelink, message]).start()
elif "7" in option:
    gamelink = input('Game ID: ')
    for i in range(int(threads)):
        Thread(target=realPlayerjoin, args=[gamelink]).start()
else:
    print('Invalid choice entered.')
