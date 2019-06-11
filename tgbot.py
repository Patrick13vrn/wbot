import telebot
import pyowm
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
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


def temp(temp):
    temp2 = float(temp)
    if temp2 < 0:
        temp_sign = '-'
    elif temp2 > 0:
        temp_sign = '+'
    else:
        temp_sign = ''
    temp_result = temp_sign + str(round(temp2))
    return temp_result


emojies = {
    200: "\u26c8",
    201: "\u26c8",
    202: "\u26c8",
    210: "\ud83c\udf29",
    211: "\u26c8",
    212: "\ud83c\udf2a",
    221: "\u26c8",
    230: "\u26c8",
    231: "\u26c8",
    232: "\u26c8",
    300: "\ud83d\udca7",
    301: "\ud83d\udca7",
    302: "\ud83d\udca6",
    310: "\ud83c\udf26",
    311: "\ud83c\udf26",
    312: "\ud83c\udf27",
    313: "\ud83c\udf28",
    314: "\ud83c\udf27",
    321: "\ud83c\udf26",
    500: "\ud83c\udf26",
    501: "\ud83c\udf28",
    502: "\ud83c\udf27",
    503: "\ud83c\udf27",
    504: "\ud83c\udf27",
    511: "\ud83c\udf27",
    520: "\ud83c\udf28",
    521: "\ud83c\udf28",
    522: "\ud83c\udf27",
    531: "\ud83c\udf26",
    600: "\u2744\ufe0f",
    601: "\u2744\ufe0f",
    602: "\u2744\ufe0f",
    611: "\ud83d\udca7",
    612: "\u2744\ufe0f",
    620: "\u2744\ufe0f",
    621: "\u2744\ufe0f",
    622: "\u2744\ufe0f",
    701: "\ud83c\udf2b",
    711: "\ud83c\udf2b",
    721: "\ud83c\udf2b",
    731: "\ud83d\udca8",
    741: "\ud83c\udf2b",
    751: "\ud83d\udca8",
    761: "\ud83d\udca8",
    762: "\ud83d\udca8",
    771: "\ud83d\udca8",
    781: "\ud83c\udf2a",
    800: "\u2600\ufe0f",
    801: "\u2601\ufe0f",
    802: "\ud83c\udf24",
    803: "\u2601\ufe0f",
    804: "\u2601\ufe0f"
}

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

        w_det = (w.get_detailed_status()).title()
        w_cloud = w.get_clouds()
        w_humid = w.get_humidity()
        w_rec_time = w.get_reference_time(timeformat='date') + timedelta(hours=3)
        w_wspeed = w.get_wind()['speed']
        w_temp = w.get_temperature('celsius')['temp']
        w_press = w.get_pressure()['press']
        w_code = w.get_weather_code()

        # print(w2.get_weather)

        try:
            w_wdeg = (w.get_wind()['deg'])
        except KeyError:
            w_wdeg = 0.0

        # current day weather forecast
        #         for weather in w2:

        # 3days weather forecast
        for weather in w2:
            f_date2 = (datetime.fromtimestamp(weather.get_reference_time()))
            f_date = datetime.strptime(str(f_date2), '%Y-%m-%d %H:%M:%S')
            f_now2 = (datetime.strftime((datetime.today().replace(microsecond=0)), '%Y-%m-%d %H:%M:%S'))
            f_now = datetime.strptime(str(f_now2), '%Y-%m-%d %H:%M:%S')

            f_time = datetime.strftime(f_date, '%H')
            f_night = '03'
            f_morning = '09'
            f_day = '15'
            f_evening = '18'
            f_wtime = {'night': '03',
                       'morning': '09',
                       'day': '15',
                       'evening': '18'}

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

            # вывод прогноза на сегодня
            if f_date3 < f_now3 + timedelta(days=1):
                if lastrain != '0':
                    rain = ' (' + lastrain + ' мм)'
                else:
                    rain = ''

                template = f_temp + '°, ' + f_status_detailed + rain + '\n'
                forecast += str(datetime.strftime(f_date, '%H:%M')) + ' '
                forecast += template

            # вывод прогноза на 3 дня
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
        answer = '*Сейчас в ' + texts + ':*\n\n' + (emojies.get(w_code, '')) + str(w_det).title() + \
                 '\nТемпература воздуха: ' + temp(w_temp) + '°' + \
                 '\nОблачность: ' + str(w_cloud) + '%' + \
                 '\nВетер: ' + str(w_wspeed) + ' м/с, ' + wind_d(w_wdeg) + \
                 '\nАтмосферное давление: ' + str("{0:.0f}".format(round(w_press / 1.333, 0))) + ' мм.рт.ст' + \
                 '\nОтносительная влажность: ' + str(w_humid) + '%' + \
                 '\n_Обновление от' + str('{:%d.%m.%y %H:%M:%S}'.format(w_rec_time)) + '_\n\n' + str(forecast) + \
                 '\n' + 'Прогноз на 3 дня:\n\n' + str(a_forecast)
        bot.send_message(message.chat.id, answer, parse_mode='Markdown')

    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling(none_stop=True)
