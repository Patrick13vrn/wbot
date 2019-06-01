import telebot
import pyowm

owm = pyowm.OWM('ee53bd221ce171abd050ae88362dc095', language="ru")
TOKEN = '823149895:AAHOU6KMCsjF-swa7fKLFyVUZpUoQvREy8U'
owm = pyowm.OWM('ee53bd221ce171abd050ae88362dc095')
bot = telebot.TeleBot(TOKEN)
trans_detailed = {'clear sky': 'Ясно',
                  'few clouds': 'Переменная облачность',
                  'scattered clouds': 'Облачно',
                  'broken clouds': 'Тучи',
                  'shower rain': 'Ливень',
                  'rain': 'Дождь',
                  'thunderstorm': 'Гром и молния',
                  'snow': 'Снег',
                  'mist': 'Дымка',
                  }


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Привет!')


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    observation = owm.weather_at_place(message.text)
    w = observation.get_weather()

    # answer = 'Сегодня в ' + message.text + w.get_status + ' сейчас ' + str(temp)
    answer = 'Сегодня в ' + message.text + ':\n\n' + \
             str(trans_detailed[(w.get_detailed_status())]) + \
             '\nТемпература воздуха - ' + str(w.get_temperature('celsius')['temp']) + '°' + \
             '\nОблачность - ' + str(w.get_clouds()) + \
             '\nВетер ' + str(w.get_wind()['speed']) + ' м/с' + \
             '\nНаправление - ' + str(w.get_wind()['deg']) + '°' + \
             '\nАтмосферное давление - ' + str("{0:.0f}".format(round(w.get_pressure()['press'] / 1.333,
                                                                      0))) + ' мм.рт.ст' + \
             '\nОтносительная влажность - ' + str(w.get_humidity()) + '%'

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
