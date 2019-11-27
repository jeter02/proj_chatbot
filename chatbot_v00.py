
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters
from emoji import emojize
import requests
from bs4 import BeautifulSoup
from flask import Flask
##import serial
import os

TOKEN ='719614337:AAGVXDHZtOK7YNUsokdtbgjqExNoTEMXxzA'

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
updater.start_polling()

url_1 = 'https://www.naver.com'
url_2 = 'https://www.clien.net/service/board/news'
url_3 = 'https://www.clien.net/service/board/cm_car'


## set for serial comm.

##ser = serial.Serial(
##    port='/dev/cu.usbmodem1411',
##    port='/dev/cu.Bluetooth-Incoming-Port',
##    baudrate=9600,
##)

## Flask
app = Flask(__name__)


class WebCrwl:
    def __init__(self, URL):
        self.url = URL

    def naver_rt(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        titles = soup.select('.ah_roll .ah_k')
        return titles

    def clien_bbs(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        titles = soup.select('.list_subject .subject_fixed')
        return titles



## telegram handler ###

def handler(bot, update):
    text = update.message.text
    chat_id = update.message.chat_id

    if ('실시간' or 'real') in text:
        a = WebCrwl(url_1)
        titles = a.naver_rt()
        for title in titles:
            bot.send_message(chat_id=chat_id, text=title.get_text())
    elif '새소식' in text:
        a = WebCrwl(url_2)
        titles = a.clien_bbs()
        for title in titles:
            bot.send_message(chat_id=chat_id, text=title.get_text())
    elif (u'굴당' or 'car') in text:
        a = WebCrwl(url_3)
        titles = a.clien_bbs()
        for title in titles:
            bot.send_message(chat_id=chat_id, text=title.get_text())
    ### IR control ###
    elif '모해' in text:
        bot.send_message(chat_id=chat_id, text='오빠생각')
    elif '주식' in text:
      ##  ir_code = 'channel up'
      ##  ser.write(ir_code.encode())
        my_schedule = 'https://finance.yahoo.com/'
        bot.send_message(chat_id=chat_id, text=my_schedule)
    elif '사진' in text:
      ##  ir_code = 'channel down'
      ##  ser.write(ir_code.encode())
        bot.send_message(chat_id=chat_id, text='사진을 전송합니다.')
        bot.sendPhoto(chat_id=chat_id, photo='https://post-phinf.pstatic.net/MjAxODExMjlfMTQ2/MDAxNTQzNDE5MDA5OTU4.B151oQt7MXABzRw4elfBDuafHB5Zv_x5CZgBldNBOeYg.jJqc7f6hQE5iVDtlZ5Xtgq-ZZvwk0hd0F9HAI-_W-Iwg.JPEG/1.jpg?type=w1200')

    else :
        bot.send_message(chat_id=chat_id, text='다시 입력해 주세요')
'''
def ir_handler(bot, update):

    text = update.message.text
    chat_id = update.message.chat_id
    if 'tv on' or u'티비 켜' in text:
        ir_code = '0x22221111'
        ser.write(ir_code.encode())
        bot.send_message(chat_id=chat_id, text=ir_code)
'''


echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegram-chatbot-v00.herokuapp.com' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))