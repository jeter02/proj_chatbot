
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
    elif (u'굴당') or ('car') in text:
        a = WebCrwl(url_3)
        titles = a.clien_bbs()
        for title in titles:
            bot.send_message(chat_id=chat_id, text=title.get_text())
    ### IR control ###
    elif '모해' in text:
        bot.send_message(chat_id=chat_id, text=emojize('오빠생각:heart_eyes:', use_aliases=True))
    elif '주식' in text:
      ##  ir_code = 'channel up'
      ##  ser.write(ir_code.encode())
        my_schedule = 'https://finance.yahoo.com/'
        bot.send_message(chat_id=chat_id, text=my_schedule)
    elif '사진' in text:
      ##  ir_code = 'channel down'
      ##  ser.write(ir_code.encode())
        bot.send_message(chat_id=chat_id, text='yes~')
        ##bot.sendPhoto(chat_id=chat_id, photo='https://thumb.named.com/normal/resize/origin/file/photo/editor/1811/9f95a04042dd42948a7463ed2ff023c8_XV7DNV5NejAwRFIcJcfga.jpeg')
    elif (u'다이버젼스' or u'다이버' or u'다이버전스') in text:
        bot.send_message(chat_id=chat_id, text='Divergence guide!!')
        bot.sendPhoto(chat_id=chat_id, photo='http://www.hozaebox.com/data/editor/1807/19d4be4d03d9a22daa42c10f9133be9f_1530486409_6612.png')
    elif ('kelly' or 'bat' ) in text:
        bot.send_message(chat_id=chat_id, text="kelly's criterion!")
        bot.sendPhoto(chat_id=chat_id, photo='https://i1.wp.com/s3-us-west-2.amazonaws.com/finbox-blog/2018/03/Kelly-Criterion-Total-Capital-Allocated-Equation.png?w=640&ssl=1')
        bot.sendPhoto(chat_id=chat_id, photo='https://welovealgos.com/wp-content/uploads/2019/06/Kelly-criterion-formula.png')
    elif '아리' in text:
        bot.send_message(chat_id=chat_id, text="유즙 분비 예방 및 억제를 위해 카버락틴 복용")
        bot.sendPhoto(chat_id=chat_id, photo='http://www.druginfo.co.kr/detailimg/%EC%B9%B4%EB%B2%84%EB%9D%BD%ED%8B%B4%EB%B6%80%EC%9E%91%EC%9A%A9%ED%91%9C2.JPG')
        bot.send_message(chat_id=chat_id, text="클래라정 복용")
        bot.sendPhoto(chat_id=chat_id, photo='http://www.druginfo.co.kr/detailimg/%ED%81%B4%EB%9E%98%EB%9D%BC%EC%9A%A9%EB%B2%95%EC%9A%A9%EB%9F%89%ED%91%9C1.JPG')
        bot.sendPhoto(chat_id=chat_id, photo='https://junoyo.tistory.com/119')
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