from roblox import Roblox, RobloxClientMutex
from time import sleep
import time
import threading
from threading import Thread
import random

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

def t():
    while 1:
        try:
            client = get_session().create_client(2185020)
            time.sleep(5)
            client.chat_message('Acier')
            time.sleep(1)
            client.close()
        except:
            pass
for _ in range(15):
    Thread(target=t).start()