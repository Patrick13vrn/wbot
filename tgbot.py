import telebot
import pyowm
from datetime import datetime, timedelta
from telebot import types
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
TOKEN = '823149895:AAGUwtRQ9dOQPvtqA8ZxZYmhd2MA4GbUK8k'
owm = pyowm.OWM('ee53bd221ce171abd050ae88362dc095', language='ru')
bot = telebot.TeleBot(TOKEN)


# wind direction degree to NSWE
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


# temp add plus and minus
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


# emoji weather condition
emojies = {
    200: "\u26C8",  # гроза с мелким дождём
    201: "\u26C8",  # гроза с дождём
    202: "\u26C8",  # гроза с проливным дождём
    210: "\U0001F329",  # возможна гроза
    211: "\u26C8",  # гроза
    212: "\U0001F32A",  # буря
    221: "\u26C8",  # жестокая гроза
    230: "\u26C8",  # гроза с мелким дождём
    231: "\u26C8",  # гроза с дождём
    232: "\u26C8",  # гроза с сильным дождём
    300: "\U0001F4A7",  # сыро
    301: "\U0001F4A7",  # сыро
    302: "\U0001F4A7",  # очень сыро
    310: "\U0001F326",  # лёгкий дождь
    311: "\U0001F326",  # лёгкий дождь
    312: "\U0001F327",  # интенсивный дождь
    313: "\U0001F327",  # дождь и морось
    314: "\U0001F327",  # сильный дождь и морось
    321: "\U0001F326",  # мелкий дождь
    500: "\U0001F326",  # легкий дождь
    501: "\U0001F327",  # дождь
    502: "\U0001F327",  # сильный дождь
    503: "\U0001F327",  # проливной дождь
    504: "\U0001F327",  # сильный дождь
    511: "\U0001F327",  # холодный дождь
    520: "\U0001F327",  # дождь
    521: "\U0001F327",  # дождь
    522: "\U0001F327",  # сильный дождь
    531: "\U0001F327",  # переодические дожди
    600: "\U0001F328",  # небольшой снегопад
    601: "\U0001F328",  # снегопад
    602: "\U0001F328",  # сильный снегопад
    611: "\U0001F4A7",  # слякоть
    612: "\U0001F328",  # дождь со снегом
    620: "\U0001F328",  # мокрый снег
    621: "\U0001F328",  # снегопад
    622: "\U0001F328",  # сильный снегопад
    701: "\U0001F32B",  # туман
    711: "\U0001F32B",  # туманно
    721: "\U0001F32B",  # туманно
    731: "\U0001F3DC",  # песчаная буря
    741: "\U0001F32B",  # туманно
    751: "\U0001F3DC",  # песок
    761: "\U0001F3DC",  # пыльная буря
    762: "\U0001F3DC",  # вулканический пепел
    771: "\U0001F32A",  # шквальный ветер
    781: "\U0001F32A",  # торнадо
    800: "\u2600",  # ясно
    801: "\U0001F325",  # облачно
    802: "\U0001F324",  # слегка облачно
    803: "\u2601",  # пасмурно
    804: "\u2601",  # пасмурно
}

# emoji constants
emoji = {
    "day": "\u2600",
    "night": "\U0001F319",
    "temp": "\U0001F321",
}

# messages
err_message = 'Что-то пошло не так...'


# greating message
@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Привет!\n\nНапишите название города, погоду в котором вы хотели бы узнать.')


# /help message
@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Просто пришите название города на русском языке   .')


markup = types.ReplyKeyboardMarkup(row_width=1)
markup.add('1')
hide_markup = telebot.types.ReplyKeyboardRemove()




@bot.message_handler(content_types=['text'])
def send_welcome(message):
    try:

        user = message.from_user
        texts = message.text
        chat_id = message.chat.id
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
            f_code = weather.get_weather_code()

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
                template = f_temp + '°, ' + f_status_detailed + emojies.get(f_code, '') + rain + '\n'
                if f_time == f_night:
                    a_forecast += str(datetime.strftime(f_date, '%a, %d %B')) + '\n'
                    a_forecast += emoji.get('night') + template
                elif f_time == f_day:
                    a_forecast += emoji.get('day') + template + '\n'
        answer = user.first_name + ', *Сейчас в ' + texts + ':*\n\n' + emojies.get(w_code, '') + str(w_det).title() + \
                 '\nТемпература воздуха: ' + temp(w_temp) + '°' + \
                 '\nОблачность: ' + str(w_cloud) + '%' + \
                 '\nВетер: ' + str(w_wspeed) + ' м/с, ' + wind_d(w_wdeg) + \
                 '\nАтмосферное давление: ' + str("{0:.0f}".format(round(w_press / 1.333, 0))) + ' мм.рт.ст' + \
                 '\nОтносительная влажность: ' + str(w_humid) + '%' + \
                 '\n_Обновление от ' + str('{:%d.%m.%y %H:%M:%S}'.format(w_rec_time)) + '_\n\n' + str(forecast) + \
                 '\n' + '*Прогноз на 3 дня:*\n\n' + str(a_forecast)

        bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=hide_markup)



    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling(none_stop=True)
