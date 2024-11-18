import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Чтобы узнать цену валюты, введите команду в формате:\n"
        "<имя валюты, цену которой Вы хотите узнать> <имя валюты,\n"
        "в которой надо узнать цену первой валюты> <количество первой валюты>\n\n"
        "Например: USD RUB 10\n\n"
        "Название валюты НЕОБХОДИМО писать в точности как указано в списке валют\n\n"
        "Список доступных валют можно получить командой /values"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def send_values(message):
    text = "Доступные валюты:\n- EUR\n- USD\n- RUB"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        base, quote, amount = values
        amount = float(amount)

        total_base = CurrencyConverter.get_price(base, quote, amount)
        text = f'{amount} {base} стоит {total_base} {quote}.'
        bot.reply_to(message, text)

    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except ValueError:
        bot.reply_to(message, 'Ошибка: количество должно быть числом.')
    except Exception as e:
        bot.reply_to(message, f'Произошла непредвиденная ошибка: {e}')

if __name__ == '__main__':
    bot.polling(none_stop=True)
