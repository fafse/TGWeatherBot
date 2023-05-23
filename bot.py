import pyowm
import telebot
from telebot import types
from pyowm.utils.config import get_default_config

#ключи для ботов
BOT_TOKEN = '5923181267:AAFYAZdvErb_0vqFsKr-ig6gwtxGlyhJPws'
OWM_API_KEY = 'fa6352d4e922729eb5e5420ba93cb9b2'
#настройка русского языка
config_dict = get_default_config()
config_dict['language'] = 'ru'
#подключение ботов и службы погоды
owm = pyowm.OWM(OWM_API_KEY, config_dict)
bot = telebot.TeleBot(BOT_TOKEN)

#первоначальное сообщение
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id,
                     "👋 Привет! Я бот, показывающий погоду в разных городах! "
                     "Чтобы узнать, как задать мне вопрос, нажмите на кнопку Помощь🆘",
                     reply_markup=markup)

#Обработчик сообщений и запросов
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Череповец')
        btn2 = types.KeyboardButton('Санкт-Петербург')
        btn3 = types.KeyboardButton('Москва')
        btn4 = types.KeyboardButton('Помощь🆘')
        markup.add(btn1, btn2, btn3, btn4)#кнопочки для городов и помощи
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)  # ответ бота


    elif message.text == 'Помощь🆘':
        bot.send_message(message.from_user.id,
                         'Для создания запроса мне вы можете воспользоваться кнопками внизу '
                         'для предложенных городов или же ввести запрос самостоятельно, просто написав название города'
                         ' на русском или английском. '
                         ' Например, Челябинск или Санкт-Петербург.',
                         parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id,
                         weather(message.text),#вызов функции weather с целью получения погоды в заданном пользователем городе
                         parse_mode='Markdown')


def weather(city):

    if not city:#если не указан город
        reply = 'Пожалуйста, укажите город'
        return reply

    # получаем текущую погоду для конкретного города
    try:
        observation = owm.weather_manager().weather_at_place(f"{city},RU")
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        status = w.detailed_status
        wind = w.wind()['speed']
        humidity = w.humidity
        response = f'Текущая погода в городе {city}: {status}, температура {temperature}°C, ветер {wind} m/s, влажность {humidity}%'
    except pyowm.commons.exceptions.NotFoundError:#если не получается найти город с таким названием
        response = f'Не могу найти погоду для {city}'

    return response


bot.polling(none_stop=True, interval=0)  #заставляет бота работать
