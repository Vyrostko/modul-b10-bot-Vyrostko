import telebot

from config import *

from extensions import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
         <в какую валюту перевести> \
            <количество переводимой валюты>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        base, quote, amount = values
    
        new_price = Converter.get_prise(base, quote, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {quote} : {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    
bot.polling()