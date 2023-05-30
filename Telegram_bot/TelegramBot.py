import telebot
from config import TOKEN, keys
from extensions import APIException, ValuesConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду в формате:\n<исходная валюта> \
<в какую валюту перевести> \
<количество переводимой валюты>\nПосмотреть список доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("Слишком много параметров")

        value1, value2, count = values
        total_value2 = ValuesConverter.get_price(value1, value2, count)
    except APIException as error:
        bot.reply_to(message, f"Ошибка пользователя\n{error}")
    except Exception as error:
        bot.reply_to(message, f"Не удалось обработать команду\n{error}")
    else:
        text = f"Цена {count} {value1} в {value2} - {total_value2}"
        bot.send_message(message.chat.id, text)


bot.polling()