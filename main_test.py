from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, \
    ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import time
import requests

TOKEN = "1181461577:AAEGd2heqoKZfE0ZJHgnlhSXvRb8_hjIruw"


def get_ll_spn(toponym):
    ll = ','.join(toponym['Point']['pos'].split())
    dx = str(abs(float(toponym['boundedBy']['Envelope']['upperCorner'].split()[0])
             - float(toponym['boundedBy']['Envelope']['lowerCorner'].split()[0])))
    dy = str(abs(float(toponym['boundedBy']['Envelope']['upperCorner'].split()[1])
             - float(toponym['boundedBy']['Envelope']['lowerCorner'].split()[1])))
    print("Получил ll и spn")
    return ll, dx + ',' + dy


def geocoder(update, context):
    geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text
    })

    toponym = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    print("Обрабатываю...")
    ll, spn = get_ll_spn(toponym)
    print("Получил ll и spn")
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
    print('Sending Photo')
    context.bot.send_photo(update.message.chat_id, static_api_request, caption="Нашёл:")
    print('Sent Photo')

def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("geo", geocoder))

    updater.start_polling()
    print('Принимаем сообщение')
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
