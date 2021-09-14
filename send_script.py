import telebot
import schedule
import time
from faunahelper import faunahelper
from faunadb.client import FaunaClient
import datetime as d
import os

bot_token = os.environ['BOT TOKEN']
faunnakey = os.environ['FAUNNAKEY']

def job(bot, faunahelper):
    students = faunahelper.get_all_students()
    print(students)
    for student in students:
        try:
            if student['days'] == 0:
                bot.send_message(student['telegram_id'], 'Добрый день у вас закончилось время поддержки')
            elif (student['days'] == 7 or student['days'] % 10 == 0 or student['days'] == 1) and student['days'] > 0:
                bot.send_message(student['telegram_id'], 'Добрый день. Напоминаю, что до конца курса у Вас осталось %s дней ' % str(student['days']))
        except telebot.apihelper.ApiTelegramException:
            bot.send_message(814803585,
                             'Добрый день. Напоминаю, что до конца курса у %s осталось %s дней ' % (student['name'], str(student['days'])))
        faunahelper.decrement_days_by_telegram_id(student['telegram_id'])

    bot.send_message(814803585, 'Программа была запущена %s' % str(d.date.today()))

bot = telebot.TeleBot(bot_token)
faunahelper = faunahelper(FaunaClient(faunnakey))

schedule.every(3).seconds.do(job, bot, faunahelper)

while True:
    schedule.run_pending()
    time.sleep(1)