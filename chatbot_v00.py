from telegram.ext import Updater, MessageHandler, Filters
from emoji import emojize
import requests
from bs4 import BeautifulSoup

updater = Updater(token='719614337:AAGVXDHZtOK7YNUsokdtbgjqExNoTEMXxzA')
dispatcher = updater.dispatcher
updater.start_polling()

url_1 = 'https://www.naver.com'
url_2 = 'https://www.clien.net/service/board/news'
url_3 = 'https://www.clien.net/service/board/cm_car'


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


class Bitcoin:
    pass


## telegram handler ###

def handler(bot, update):
    text = update.message.text
    chat_id = update.message.chat_id

    if '실시간' in text:
        a = WebCrwl(url_1)
        titles = a.naver_rt()
        for title in titles:
            bot.send_message(chat_id=chat_id, text=title.get_text())
    elif '새소식' in text:
        a = WebCrwl(url_2)
        titles = a.clien_bbs()
        for title in titles:
            bot.send_message(chat_id=chat_id, text=title.get_text())
    elif '굴당' or '굴러간당' in text:
        a = WebCrwl(url_3)
        titles = a.clien_bbs()
        for title in titles:
            bot.send_message(chat_id=chat_id, text=title.get_text())

    else:
        bot.send_message(chat_id=chat_id, text='다시 입력해 주세요')


print('now running...')
echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)

