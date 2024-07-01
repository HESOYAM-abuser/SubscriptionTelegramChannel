# -*- coding: utf-8 -*-
#imports===================================================
from time import sleep
import telebot
from telebot import types
import string
import random
import os
#==========================================================
bot_token = '000000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' # Telegram Bot TOKEN
data = {}
#options===================================================
bot = telebot.TeleBot(token=bot_token)
#data[message.chat.id] = ['code', None, 'A', message.chat.fitst_name, message.chat.last_name, message.chat.username]
#context===================================================
menu_context = '''
eyyyyyyy
choose one of them
'''
creator_content = '''
created by HESOYAM-abuser
'''
descriptions_content = '''
شما با این بات میتونید برای ورود به کانال VIP سارکستیک سوسایتی اشتراک بگیرید و اکانت خودتون رو مدیریت کنید.

گرفتن اشتراک کانال VIP، نوعی حمایت از ما در کنار دسترسی به محتوای بیشتر و اوریجینال هستش که بیشتر لذت ببرید 💙

در صورتی که به مشکلی خوردید، به آی‌دی زیر پیام بدید:
@VIP_Cservice
'''
frontpage = '''
Welcome! ❄️

In order to join Sarcastic Society’s VIP channel, choose the “Subscribe” button.
—————————————
 خوش آمدید! ☄️

جهت عضویت در کانال VIP سارکستیک سوسایتی، دکمه‌ی «Subscribe» را انتخاب کنید.
'''
buylist = '''
A - یک ماهه = ۵٫۰۰۰ تومان
B - سه ماهه = ۱۲٫۵۰۰ تومان
C - شش ماهه = ۲۵٫۰۰۰ تومان
D - یک ساله = ۵۰٫۰۰۰ تومان
'''
letters = ['A', 'B', 'C', 'D']
error = 'Ooops! something went wrong'
buy_context = [
'''
Please choose your Subscription Plan:
———————————————
لطفا نوع اشتراک خود را انتخاب کنید:
''',
'''
جهت پرداخت به لینک زیر (درگاه زرین‌پال) بروید. بعد از اینکه پرداخت شما کامل شد، به منوی «My Account» داخل بات برگشته تا لینک کانال و اطلاعات عضویت شما نمایش داده شود.

کد شما:
''',
'''Now go to this site and finish the purchase: https://www.sarcasticsociety.ir/request/''',
]
account_content = ['Your name is ','Your type of membership is ','Expiration date: ','You don’t have any subscriptions yet.','https://t.me/joinchat/AAAAAEvFaYmUTfKIvJ4wQg']
no_account = '''
You don’t have any subscriptions. Please get one from the “Subscribe” menu and try again. 
—————————————
شما هیچ اشتراکی ندارید. لطفا از منوی «Subscribe» یک مورد را انتخاب کرده و دوباره امتحان کنید.
'''
warning_text = '''
توجه: در صورت خرید دوباره، اشتراک قبلی حذف میشود و زمان عضویت شما از زمان خرید جدید محاسبه میشود.

برای بازگشت به منوی اصلی روی /start بزنید.
'''
#functions=================================================
def code(ID):
    id0 = ID
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number = hex_number[2:]
    file0 = open('database/Codes.txt', 'r')
    all_lines = file0.readlines()
    for i in all_lines:
        if i == hex_number:
            code(id0)
    file0.close()
    file0 = open('database/Codes.txt', 'a')
    file0.write(hex_number+'\n')
    file0.close()
    data[ID][0] = hex_number
    del file0
    data_w()
    return hex_number
#----------------------------------------------------------
def data_r():
    global data
    file0 = open('database/data.txt', 'r')
    data = eval(file0.read())
    file0.close()
    del file0
    return data
#----------------------------------------------------------
def data_w():
    global data
    file0 = open('database/data.txt', 'w')
    file0.write(str(data))
    file0.close()
    del file0
#----------------------------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('My Account')
    itembtnb = types.KeyboardButton('Subscribe')
    itembtnc = types.KeyboardButton('Descriptions')
    itembtnd = types.KeyboardButton('Creator')
    markup.row(itembtna)
    markup.row(itembtnb)
    markup.row(itembtnc, itembtnd)
    bot.send_message(message.chat.id, frontpage, reply_markup=markup)
#----------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "My Account")
def account(message):
    global data
    data_r()
    if message.chat.id in data.keys():
        if data[message.chat.id][1] != None:
            bot.send_message(message.chat.id, account_content[0]+str(data[message.chat.id][3]))
            bot.send_message(message.chat.id, account_content[1]+str(data[message.chat.id][2]))
            bot.send_message(message.chat.id, account_content[2]+str(data[message.chat.id][6]))
            bot.send_message(message.chat.id, account_content[4])
        else:
            bot.send_message(message.chat.id, account_content[0]+str(data[message.chat.id][3]))
            bot.send_message(message.chat.id, account_content[3])
    else:
        bot.send_message(message.chat.id, no_account)
#----------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Subscribe")
def send_buy(message):
    bot.send_message(message.chat.id, buylist)
    bot.send_message(message.chat.id, warning_text)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtna = types.KeyboardButton(letters[0])
    itembtnb = types.KeyboardButton(letters[1])
    itembtnc = types.KeyboardButton(letters[2])
    itembtnd = types.KeyboardButton(letters[3])
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc, itembtnd)
    msg = bot.send_message(message.chat.id, buy_context[0], reply_markup=markup)
    bot.register_next_step_handler(msg, buy0)
def buy0(message):
    global data
    data_r()
    if message.text == 'A' or message.text == 'B' or message.text == 'C' or message.text == 'D':
        data[message.chat.id] = ['code', None, message.text, message.from_user.first_name, message.from_user.last_name, message.from_user.username, False]
        data_w()
        markup = types.ReplyKeyboardMarkup()
        itembtna = types.KeyboardButton('My Account')
        itembtnb = types.KeyboardButton('Subscribe')
        itembtnc = types.KeyboardButton('Descriptions')
        itembtnd = types.KeyboardButton('Creator')
        markup.row(itembtna)
        markup.row(itembtnb)
        markup.row(itembtnc, itembtnd)
        bot.send_message(message.chat.id, buy_context[1]+code(message.chat.id))
        bot.send_message(message.chat.id, buy_context[2]+data[message.chat.id][0], reply_markup=markup)
    else:
        bot.send_message(message.chat.id, error)
#----------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Descriptions")
def descriptions(message):
    bot.send_message(message.chat.id, descriptions_content)
#----------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Creator")
def Creator(message):
    bot.send_message(message.chat.id, creator_content)
#==========================================================
while True:
    try:
        bot.polling()
    except Exception:
        sleep(2)
