import telebot
from telebot import types
from config import keys
from settings import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    start = types.KeyboardButton('/start')
    help = types.KeyboardButton('/help')
    values = types.KeyboardButton('/values')
    markup.add(start, help, values)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username}!\
    \nНужна помощь в конвертации валют? Я помогу \
    \n \
    \nВведите запрос в формате: доллар рубль 100, где\
    \nдоллар - валюта для перевода (название из 2х слов вводить слитно) \
    \nрубль - валюта, в которую хотите перевести \
    \n100 - количество переводимой валюты \
    \n \
    \nПосмотреть список всех доступных валют: /values \
    \nНужна помощь? нажмите /help', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Введите запрос в формате: доллар рубль 100, где' \
           '\nдоллар - валюта для перевода (название из 2х слов вводить слитно)' \
           '\nрубль - валюта, в которую хотите перевести ' \
           '\n100 - количество переводимой валюты ' \
           '\n' \
           '\nПосмотреть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().replace(',', '.').split(' ')

        if len(values) != 3:
            raise APIException('Не совпадает количество введенных параметров\
            \nДля помощи нажмите /help')
        
        quote, base, amount = values 
        total = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} = {round(total, 2)} {base}'
        # text = f'{amount} {quote} = {round(total, 2)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
