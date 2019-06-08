import telebot
import pyowm
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')
TOKEN = '823149895:AAGUwtRQ9dOQPvtqA8ZxZYmhd2MA4GbUK8k'
owm = pyowm.OWM('ee53bd221ce171abd050ae88362dc095', language='ru')
bot = telebot.TeleBot(TOKEN)


def wind_d(direction):
    return {
        direction == 0.0: '',
        0.0 < direction < 22.5: 'Северный',
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


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Привет!\n\nНапишите название города, погоду в котором вы хотели бы узнать.')


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    try:
        texts = message.text
        observation = owm.weather_at_place(texts)
        f_3h = owm.three_hours_forecast(texts)
        w = observation.get_weather()
        w2 = f_3h.get_forecast()
        a_forecast = ''
        forecast = ''

        w_det = w.get_detailed_status()
        w_cloud = w.get_clouds()
        w_humid = w.get_humidity()
        w_rec_time = w.get_reference_time(timeformat='date') + timedelta(hours=3)
        w_wspeed = w.get_wind()['speed']
        w_temp = w.get_temperature('celsius')['temp']
        w_press = w.get_pressure()['press']

        try:
            w_wdeg = (w.get_wind()['deg'])
        except KeyError:
            w_wdeg = 0.0

        for weather in w2:

            f_date2 = (datetime.fromtimestamp(weather.get_reference_time()))
            f_date = datetime.strptime(str(f_date2), '%Y-%m-%d %H:%M:%S')
            f_now2 = (datetime.strftime((datetime.today().replace(microsecond=0)), '%Y-%m-%d %H:%M:%S'))
            f_now = datetime.strptime(str(f_now2), '%Y-%m-%d %H:%M:%S')

            f_time = datetime.strftime(f_date, '%H')
            f_night = '03'
            f_day = '15'
            f_end = f_now.replace(hour=0, minute=0, second=0) + timedelta(days=3)
            f_now3 = f_now.replace(hour=0, minute=0, second=0)
            f_date3 = f_date.replace(hour=0, minute=0, second=0)
            raw_temp = round(weather.get_temperature('celsius')['temp'])
            if raw_temp > 0:
                f_temp = '+' + str(raw_temp)
            elif raw_temp < 0:
                f_temp = '-' + str(raw_temp)
            else:
                f_temp = str(raw_temp)

            f_status_detailed = str(weather.get_detailed_status())
            f_rain = weather.get_rain()
            if len(f_rain) == 0:
                lastrain = '0'
            else:
                lastrain = str(round(f_rain["3h"]))

            if f_now3 < f_date3 <= f_end:
                if lastrain != '0':
                    rain = ' (' + lastrain + ' мм)'
                else:
                    rain = ''
                template = f_temp + '°, ' + f_status_detailed + rain + '\n'
                if f_time == f_night:
                    a_forecast += str(datetime.strftime(f_date, '%a, %d %B')) + '\n'
                    a_forecast += 'Ночью: ' + template
                elif f_time == f_day:
                    a_forecast += 'Днём: ' + template + '\n'

        answer = 'Сегодня в ' + texts + ':\n\n' + str(w_det).title() + \
                 '\nТемпература воздуха - ' + str(w_temp) + '°' + \
                 '\nОблачность - ' + str(w_cloud) + '%' + \
                 '\nВетер ' + str(w_wspeed) + ' м/с, ' + wind_d(w_wdeg) + \
                 '\nАтмосферное давление - ' + str("{0:.0f}".format(round(w_press / 1.333, 0))) + ' мм.рт.ст' + \
                 '\nОтносительная влажность - ' + str(w_humid) + '%' + \
                 '\nОбновление ' + str('{:%d.%m.%y %H:%M:%S}'.format(w_rec_time)) + \
                 '\n\n\n' + 'Прогноз на 3 дня:\n' + str(a_forecast)
        bot.send_message(message.chat.id, answer)


    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling(none_stop=True)
