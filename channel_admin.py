# -*- coding: utf-8 -*-
#==========================================================
from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import GetParticipantsRequest
import telebot
from datetime import datetime
from time import sleep
import os
#==========================================================
channel_id = -0000000000 # channel numeric id
api_id = 000000 # api id of app hash from my.telegram.org
api_hash = '' # client app hash from my.telegram.org
bot_token = '000000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' # Telegram Bot TOKEN
bot2_token = '000000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' # Telegram Bot TOKEN
bot = telebot.TeleBot(token=bot_token)
bot2 = telebot.TeleBot(token=bot2_token)
client = TelegramClient('main', api_id, api_hash, )
member_list = []
member_kick = []
member_del = []
data = {}
#==========================================================
client.start()
client.connect()
channel = client.get_entity('https://t.me/joinchat/AAAAAEvFaYmUTfKIvJ4wQg')
#==========================================================
content = ['Your membership is ending soon, consider subscribing again?!']
#==========================================================
def list_diff(list1, list2): 
	return (list(set(list1) - set(list2))) 
#==========================================================
def data_w():
    global data
    file0 = open('database/data.txt', 'w')
    file0.write(str(data))
    file0.close()
    del file0
#==========================================================
def data_r():
    global data
    file0 = open('database/data.txt', 'r')
    data = eval(file0.read())
    file0.close()
    del file0
#==========================================================
def member_checker():
    global member_list, data, member_kick, channel
    client.start()
    client.connect()
    offset = 0
    limit = 10000000
    while True:
        participants = client(GetParticipantsRequest(
            channel, channel, offset, limit,hash=0))
        if not participants.users:
            break
        for _user in participants.users:
            member_list.append(_user.id)
#            print('user : ', _user.id, _user.username)
        offset += len(participants.users)
    non_permission = list_diff(member_list, data.keys())
    for i in non_permission:
        member_kick.append(i)
#==========================================================
def time_checker():
    global data, member_kick
    for i in data.keys():
        try:
            if data[i][1] < int(datetime.now().timestamp()):
                member_del.append(i)
                try:
                    bot2.send_message(i, 'Your membership expired')
                except:
                    pass
                member_kick.append(i)
            else:
                pass
        except:
            member_kick.append(i)
#==========================================================
def member_kicker():
    global member_kick
    for i in member_kick:
        try:
            bot.kick_chat_member(channel_id, i)
            print(i, 'kicked')
        except Exception:
            pass
#==========================================================
def member_deler():
    global data, member_del
    for i in member_del:
        del data[i]
    data_w()
#==========================================================
while True:
    try:
        while True:
            member_del = []
            member_list = []
            member_kick = []
            data_r()
            time_checker()
            member_deler()
            member_checker()
            member_kicker()
            sleep(1)
            if os.path.isfile('main.session-journal'):
                os.system('rm main.session-journal')
    except Exception:
        sleep(10)
#==========================================================

