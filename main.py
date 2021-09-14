import telebot
from faunahelper import faunahelper
from faunadb.client import FaunaClient
from faunadb.errors import NotFound
import os

bot_token = os.environ['BOT_TOKEN']
faunnakey = os.environ['FAUNNAKEY']

bot = telebot.TeleBot(bot_token)
faunahelper = faunahelper(FaunaClient(faunnakey))

@bot.message_handler(commands=['getdays'])
def getdays(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, 'До конца курса осталось %s дней.' % str(faunahelper.get_days_by_telegram_id(chat_id) + 1))
    except NotFound:
        bot.send_message(chat_id, 'Извините, информации о Вас нету в базе данных.')

if __name__ == '__main__':
    bot.polling(none_stop=True)
