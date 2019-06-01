# import urllib3
# import parser
# import socks
# import socket
import telebot
import pyowm

# owm = pyowm.OWM('ee53bd221ce171abd050ae88362dc095', language="ru")
TOKEN = '823149895:AAHOU6KMCsjF-swa7fKLFyVUZpUoQvREy8U'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Привет, народ!')


# @bot.message_handler(content_types=['text'])
# def send_welcome(message):
#     observation = owm.weather_at_place(message.text)
#     w = observation.get_weather()
#     temp = w.get_temperature('celsius')['temp']
#     answer = 'В городе ' + message.text + ' сейчас ' + str(temp)
#     bot.send_message(message.chat.id, answer)
#     bot.send_message(message.chat.id, w)


bot.polling(none_stop=True)
