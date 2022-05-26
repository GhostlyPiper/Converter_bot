import telebot

from telebot import types
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

conv_markup = types.ReplyKeyboardMarkup(
    row_width=2,
    one_time_keyboard=True
)

buttons = []
for val in keys.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))

conv_markup.add(*buttons)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Чтобы конвертировать валюту введите команду: /convert\
\nУвидеть список всех доступных валют: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):

    text = '<b>Доступные валюты:</b>'
    for key, value in keys.items():
        l_ = f'{key}  :  {value}'
        text = '\n'.join((text, l_,))
    bot.reply_to(message, text, parse_mode='HTML')


@bot.message_handler(commands=['convert'])
def quote_handler(message: telebot.types.Message):

    text = 'Выберите валюту из которой \nконвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):

    quote = message.text.strip().lower()
    try:
        text = f'<b>{keys[quote]}</b> ->\nВыберите валюту в которую \
        \nконвертировать:'

    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{e}')

    else:
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=conv_markup,
            parse_mode='HTML'
        )

        bot.register_next_step_handler(message, amount_handler, quote)


def amount_handler(message: telebot.types.Message, quote):

    base = message.text.strip().lower()
    try:
        text = f'<b><strong>{keys[quote]} -> {keys[base]}</strong></b>\
        \nВыберите количество\
        \nконвертируемой валюты:'

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f'Ошибка пользователя:\n{e}'
        )

    else:
        bot.send_message(message.chat.id, text, parse_mode='HTML')
        bot.register_next_step_handler(
            message,
            total_base_handler,
            quote, base
        )


def total_base_handler(message: telebot.types.Message, quote, base):

    amount = message.text.strip()
    try:
        total_base = CryptoConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.send_message(
            message.chat.id,
            f'Ошибка пользователя:\n{e}'
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f'Не удалось обработать команду:\n{e}'
        )

    else:
        text = f'<b>Цена {amount} {keys[quote]} <i>({quote})</i> \
в {keys[base]} <i>({base})</i> = {total_base} {keys[base]}</b>'

        bot.send_message(message.chat.id, text, parse_mode='HTML')


bot.polling()
