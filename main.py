from roblox import Roblox, RobloxClientMutex
from time import sleep
import time
import threading
from threading import Thread
import random
import requests

mutex = RobloxClientMutex()

with open("cookies.txt") as f:
    cookies = f.read().splitlines()

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
def likeGame(cookie, gameid):
    token = getToken(cookie)
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
    likereq = requests.post(f'https://www.roblox.com/voting/vote?assetId={gameid}&vote=true', data=data, headers=headers, cookies=cookies)
    if likereq.status_code == 200:
        print('Sucessfully liked game. If likes are not showing up account is unverified.')
    elif likereq.status_code == 429:
        print('Ratelimited. Waiting and trying again')
        time.sleep(20)
        return likeGame(cookie, gameid)
    else:
        print(likereq.text)

def dislikeGame(cookie, gameid):
    token = getToken(cookie)
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
    likereq = requests.post(f'https://www.roblox.com/voting/vote?assetId={gameid}&vote=false', data=data, headers=headers, cookies=cookies)
    if likereq.status_code == 200:
        print('Sucessfully disliked game. If likes are not showing up account is unverified.')
    elif likereq.status_code == 429:
        print('Ratelimited. Waiting and trying again')
        time.sleep(20)
        return dislikeGame(cookie, gameid)
    elif "FloodCheckThresholdMet" in likereq.text:
        print('Ratelimited. Waiting and trying again')
        time.sleep(20)
        return dislikeGame(cookie, gameid)
    else:
        print(likereq.text)

def getToken(cookie):
    try:
        request = requests.post("https://auth.roblox.com/v1/logout", headers={"Cookie": f".ROBLOSECURITY={cookie};"})
        if request.status_code == 200 or request.status_code == 403:
            print('Successfully updated token')
            return request.headers["x-csrf-token"]
        if request.status_code == 401:
            return "Invalid Cookie"
    except Exception as error:
        print("Unknown error occurred when attempting to update token")
        print(error)
        print(request.text)
def joinLike(gameid):
    while 1:
        try:
            cookie = random.choice(cookies)
            client = get_session_cookie(cookie).create_client(gameid)
            time.sleep(6)
            client.close()
            likeGame(cookie, gameid)
        except:
            pass
def joinDislike(gameid):
    while 1:
        try:
            cookie = random.choice(cookies)
            client = get_session_cookie(cookie).create_client(gameid)
            time.sleep(6)
            client.close()
            dislikeGame(cookie, gameid)
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
[5] Join no disconnect''')
option = input('\nOption: ')
if "1" in option:
    gamelink = input('Game ID: ')
    for i in range(15):
        Thread(target=noMessage, args=[gamelink]).start()
elif "2" in option:
    gamelink = input('Game ID: ')
    messagetosend = input('Message: ')
    for i in range(15):
        Thread(target=joinMessage, args=[messagetosend, gamelink]).start()
elif "3" in option:
    gamelink = input('Game ID: ')
    for i in range(15):
        Thread(target=joinLike, args=[gamelink]).start()
elif "4" in option:
    gamelink = input('Game ID: ')
    for i in range(15):
        Thread(target=joinDislike, args=[gamelink]).start()
elif "5" in option:
    gamelink = input('Game ID: ')
    for i in range(15):
        Thread(target=joinNoLeave, args=[gamelink]).start()
