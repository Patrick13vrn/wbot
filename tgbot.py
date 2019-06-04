import telebot
import pyowm
from datetime import datetime, timedelta

TOKEN = '823149895:AAGUwtRQ9dOQPvtqA8ZxZYmhd2MA4GbUK8k'
owm = pyowm.OWM('ee53bd221ce171abd050ae88362dc095', language='ru')
bot = telebot.TeleBot(TOKEN)


# trans_detailed = {'clear sky': 'Ясно',
#                   'light intensity shower rain': 'Морось',
#                   'few clouds': 'Переменная облачность',
#                   'overcast clouds': 'Облачно',
#                   'scattered clouds': 'Облачно',
#                   'broken clouds': 'Тучи',
#                   'shower rain': 'Ливень',
#                   'rain': 'Дождь',
#                   'thunderstorm': 'Гром и молния',
#                   'snow': 'Снег',
#                   'mist': 'Дымка',
#                   }


def wind_d(direction):
    return {
        0 <= direction < 22.5: 'Северный',
        22.5 <= direction < 67.5: 'Северо-Восточный',
        67.5 <= direction < 112.5: 'Восточный',
        112.5 <= direction < 157.5: 'Юго-Восточный',
        157.5 <= direction < 202.5: 'Южный',
        202.5 <= direction < 247.5: 'Юго-Западный',
        247.5 <= direction < 292.5: 'Западный',
        292.5 <= direction < 337.5: 'Северо-Западный',
        337.5 <= direction <= 360: 'Северный',
    }[True]


err_message = 'Что-то пошло не так...'
weather_1h = datetime.now() + timedelta(hours=1)
weather_3h = datetime.now() + timedelta(hours=3)
weather_5h = datetime.now() + timedelta(hours=5)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Привет!\n\nНапишите название города, погоду в котором вы хотели бы узнать.')


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    try:
        observation = owm.weather_at_place(message.text)
        f_3h = owm.three_hours_forecast(message.text)
        w = observation.get_weather()
        w2 = f_3h.get_forecast()
        a_forecast = ''
        forecast = ''
        answer = str(owm.is_API_online())
        for weather in w2:
            f_date = str('{:%d %b - %H:%M}'.format((weather.get_reference_time('date') + timedelta(hours=3))))
            f_temp = str(weather.get_temperature('celsius')['temp'])
            f_status_detailed = str(weather.get_detailed_status())
            forecast = f_date + ' ' + f_temp + ' ' + f_status_detailed + ' ' + '\n'
            a_forecast = a_forecast + str(forecast)
            # if '{:%d %b - %H:%M}'.format(weather.get_reference_time('date') + timedelta(hours=3)) <= '{:%d %b - %H:%M}'.format((datetime.now())):
            answer = 'Сегодня в ' + message.text + ':\n\n' + str((w.get_detailed_status())) + '\nТемпература воздуха - ' + str(w.get_temperature('celsius')['temp']) + '°' + '\nОблачность - ' + str(w.get_clouds()) + '%' + '\nВетер ' + str(w.get_wind()['speed']) + ' м/с, ' + wind_d(w.get_wind()['deg']) + '\nАтмосферное давление - ' + str("{0:.0f}".format(round(w.get_pressure()['press'] / 1.333, 0))) + ' мм.рт.ст' + '\nОтносительная влажность - ' + str(w.get_humidity()) + '%\n' + 'Обновление ' + str('{:%d.%m.%y %H:%M:%S}'.format(w.get_reference_time(timeformat='date') + timedelta(hours=3))) + '\n\n\n' + 'Прогноз на 3 дня:\n' + str(a_forecast)
            # else:
            #     break
        bot.send_message(message.chat.id, answer)
        # forecast = str(w2.get_weathers())
        # bot.send_message(message.chat.id, forecast)
    except:
        bot.send_message(message.chat.id, err_message)


bot.polling(none_stop=True)
