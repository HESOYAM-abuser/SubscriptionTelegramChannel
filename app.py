# -*- coding: utf-8 -*-
#========================================================
import random
import flask
from flask import Flask, url_for, redirect, request
from suds.client import Client
import os
from datetime import datetime, timedelta
import telebot
#==========================================================
os.system('nohup python3 channel_admin.py &')
os.system('nohup python3 bot.py &')
bot_token = '000000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' # Telegram Bot TOKEN
bot = telebot.TeleBot(token=bot_token)
channel_id = -00000000000 # channel numeric id
app = Flask(__name__)
MMERCHANT_ID = 'XXXX-XXXX-XXXXXXXXXXXXXX' # merchant id from Zarinpal
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
amount = 1000  # Amount will be based on Toman  Required
data = {}
permission = False
email = 'user@userurl.ir'  # Optional
mobile = '09123456789'  # Optional
#==========================================================
def code_generator():
    global permission
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number = hex_number[2:]
    permission = hex_number
    return hex_number
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
    return data
#==========================================================
def cost(ID):
    global data
    ID = int(ID)
    data_r()
    if data[ID][2] == 'A':
        return 5000
    elif data[ID][2] == 'B':
        return 12500
    elif data[ID][2] == 'C':
        return 25000
    elif data[ID][2] == 'D':
        return 50000
#==========================================================
def description(ID):
    global data
    data_r
    x = str(data[ID][3])+' '+str(data[ID][4])+' @'+str(data[ID][5])+' Sarcastic Society membership'
    return x
#==========================================================
def day(ID):
    global data
    data_r()
    ID = int(ID)
    if data[ID][2] == 'A':
        data[ID][1] = int((datetime.now()+timedelta(days=30)).timestamp())
        data[ID][6] = str(datetime.now()+timedelta(days=30))
        data_w()
        try:
            bot.unban_chat_member(channel_id, ID)
        except:
            pass
    elif data[ID][2] == 'B':
        data[ID][1] = int((datetime.now()+timedelta(days=90)).timestamp())
        data[ID][6] = str(datetime.now()+timedelta(days=90))
        data_w()
        try:
            bot.unban_chat_member(channel_id, ID)
        except:
            pass
    elif data[ID][2] == 'C':
        data[ID][1] = int((datetime.now()+timedelta(days=180)).timestamp())
        data[ID][6] = str(datetime.now()+timedelta(days=180))
        data_w()
        try:
            bot.unban_chat_member(channel_id, ID)
        except:
            pass
    elif data[ID][2] == 'D':
        data[ID][1] = int((datetime.now()+timedelta(days=365)).timestamp())
        data[ID][6] = str(datetime.now()+timedelta(days=365))
        data_w()
        try:
            bot.unban_chat_member(channel_id, ID)
        except:
            pass
#==========================================================
def data_logger():
    global data
    data_r()
    logs = {}
    for i in data.keys():
        logs[i] = dict({'key':i,
        'name':data[i][3],
        'last_name':data[i][4],
        'username':data[i][5],
        'type01':data[i][2],
        'day45':data[i][6],
        't_code':data[i][0]})
    return logs
#==========================================================
@app.route('/')
def index():
    return flask.render_template('index.html')
#==========================================================
@app.route('/login')
def login():
    return flask.render_template('login.html')
#==========================================================
@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    if request.method == 'POST':
        user12 = request.form['user']
        pass12 = request.form['pass']
        if user12 == 'user' and pass12 == 'password': # user and password of admin panel
            return redirect(url_for('log',code12 = code_generator()))
        else:
            return 'wrong username or password'
    else:
        user12 = request.form['user']
        pass12 = request.form['pass']
        if user12 == 'user' and pass12 == 'password': # user and password of admin panel
            return redirect(url_for('log',code12 = code_generator()))
        else:
            return 'wrong username or password'
    return'Ooooops! something went wrong'
#==========================================================
@app.route('/log/<code12>')
def log(code12):
    global permission
    if code12 == permission:
        permission = False
        return flask.render_template('log.html', result = data_logger())
    else:
        return 'u dont have permission'
#==========================================================
@app.route('/request/<code>')
def send_request(code):
    global data
    data_r()
    for i in data.keys():
        if data[i][0] == code:
            client = Client(ZARINPAL_WEBSERVICE)
            result = client.service.PaymentRequest(MMERCHANT_ID,
                                                cost(i),
                                                description(i),
                                                email,
                                                mobile,
                                                str(url_for('verify', _external=True, i0=i)))
            if result.Status == 100:
                return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
            else:
                return 'Error'
    return 'There is no code try subscribe again in telegram bot'
#==========================================================
@app.route('/verify/<i0>', methods=['GET', 'POST'])
def verify(i0):
    client = Client(ZARINPAL_WEBSERVICE)
    if request.args.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.args['Authority'],
                                                    cost(i0))
        if result.Status == 100:
            day(i0)
            return 'Transaction success. RefID: ' + str(result.RefID)
        elif result.Status == 101:
            day(i0)
            return 'Transaction submitted : ' + str(result.Status)
        else:
            return 'Transaction failed. Status: ' + str(result.Status)
    else:
        return 'Transaction failed or canceled by user'
#==========================================================
if __name__ == '__main__':
    app.run(debug=True)
