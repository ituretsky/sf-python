import telebot
from cur_bot_config_hidden import TOKEN, cur_dic
from cur_bot_utils import ConvertionExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы пересчитать валюту укажите через пробел:\
\nнаименование валюты, \
в какую валюту пересчитать и \
количество переводимой валюты.\
\nЧтобы увидеть список доступных валют наберите: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for cur in cur_dic.keys():
        text = '\n'.join((text, cur, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('Нужно ввести три параметра: валюта1, валюта2 и число.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
