import locale
from datetime import datetime
from datetime import timedelta

import pyowm
import telebot
from telebot import types

import secure
from libs import emojies, emoji

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
TOKEN = secure.tg_token()

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
owm = pyowm.OWM(secure.owm_token(), language='ru')
bot = telebot.TeleBot(TOKEN)


# wind direction degree to NSWE
def wind_d(direction):
    """
    Returns direction callout according to wind's direction in degrees
    :param direction:
    :return: direction wording
    """
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
def temp(input_temp):
    """
    Formats input temperature with "+" or "-" sign
    :param input_temp:
    :return: formated temperature
    """
    decimal = 0
    temp2 = float(input_temp)
    if temp2 < 0:
        temp_sign = ''
    elif temp2 > 0:
        temp_sign = '+'
    else:
        temp_sign = ''
        decimal = 0
    temp_result = temp_sign + str(round(temp2, decimal))
    return temp_result


# emoji weather condition

# emoji constants

# messages
err_message = 'Что-то пошло не так...'


# greeting message
@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Привет!\n\nНапишите название города, погоду в котором вы хотели бы узнать.')


# /help message
@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 'Просто пришите название города на русском языке.')


# /log displays the whole list of searches
@bot.message_handler(commands=['log'])
def start_handler(message):
    try:
        with open('logs.txt', mode='r+') as file_log:
            log = ''
            for line in file_log.readlines():
                log += str(line)
        if len(log) > 0:
            bot.send_message(message.chat.id, log)
    except Exception as e:
        bot.send_message(message.chat.id, e)


# /clr clears the log's entries
@bot.message_handler(commands=['clr'])
def start_handler(message):
    """
    Clears the whole log file
    :param message: none
    :return: cleared log file
    """
    try:
        with open('logs.txt', mode='w') as file_log:
            file_log.write('')
        bot.send_message(message.chat.id, "Логи очищены.")
    except Exception as e:
        bot.send_message(message.chat.id, e)


# search for last requested city
def last_city(message):
    try:
        data = []
        with open('logs.txt', 'r+') as file_log:
            for line in file_log.readlines():
                data.append(line.split(";"))  # String splitting with ";" sign
        rev_data = data[::-1]  # reverse log
        for i in rev_data:
            if i[1] == str(message.from_user.id):
                # the 5th position in log's string is a user's successfully requested city name
                city = i[4]
                break
    except Exception as e:
        bot.send_message(message.chat.id, e)
        city = ''
    return city


# /city outputs last searched city
@bot.message_handler(commands=['city'])
def start_handler(message):
    try:
        bot.send_message(message.chat.id, last_city(message))
    except Exception as e:
        bot.send_message(message.chat.id, e)


def keyboard(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton(last_city(message))
    markup.add(btn1)
    return markup


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    try:
        user = message.from_user
        texts = message.text.capitalize()
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
        try:
            w_wdeg = (w.get_wind()['deg'])
        except KeyError:
            w_wdeg = 0.0

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
                    rain = f' ({lastrain} мм)'
                else:
                    rain = ''

                template = f"{temp(f_temp)}°, {f_status_detailed}{rain}{emojies.get(f_code, '')}\n"
                forecast += f"{str(datetime.strftime(f_date, '%H:%M'))} {template}"
                # forecast += template

            # вывод прогноза на 3 дня
            if f_now3 < f_date3 <= f_end:
                if lastrain != '0':
                    rain = f' ({lastrain} мм)'
                else:
                    rain = ''
                template = f"{temp(f_temp)}°, {f_status_detailed}{emojies.get(f_code, '')}{rain}\n"
                if f_time == f_night:
                    a_forecast += f"{str(datetime.strftime(f_date, '%a, %d %B'))}\n"
                    a_forecast += f"{emoji.get('night')}{template}"
                elif f_time == f_day:
                    a_forecast += f"{emoji.get('day')}{template}\n"

        answer = f"{user.first_name}, cейчас в *{texts}:*\n\n" \
            f"{emojies.get(w_code, '')}{str(w_det).title()}\n" \
            f"Температура воздуха: {temp(w_temp)}°\n" \
            f"Облачность: {str(w_cloud)}%\n" \
            f"Ветер: {str(w_wspeed)} м/с, {wind_d(w_wdeg)}\n" \
            f"Атмосферное давление: {str('{0:.0f}'.format(round(w_press / 1.333, 0)))} мм.рт.ст\n" \
            f"Относительная влажность: {str(w_humid)}%\n" \
            f"_Обновление от {str('{:%d.%m.%y %H:%M:%S}'.format(w_rec_time))}_\n\n" \
            f"{str(forecast)}\n" \
            f"*Прогноз на 3 дня:*\n\n" \
            f"{str(a_forecast)}"
        # logging
        with open("logs.txt", mode="a") as file:
            date_log = (datetime.utcfromtimestamp(message.date) + (timedelta(hours=3))).strftime(
                '%Y-%m-%d %H:%M:%S')
            log_out = f'{date_log};{user.id};{user.first_name};{user.last_name};{texts};\n'
            file.write(log_out)

        bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=keyboard(message))

        if call.data == "second":
            keyboard2 = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(text="Назад", callback_data="back")
            keyboard2.add(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, parse_mode='Markdown',
                                  message_id=call.message.message_id, text=answer,
                                  reply_markup=keyboard2)
        else:
            False

    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling(none_stop=True)
