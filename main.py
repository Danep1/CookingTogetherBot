from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, \
    CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pyodbc as odbc
import time
from text_moderation import *

TOKEN = "1181461577:AAEGd2heqoKZfE0ZJHgnlhSXvRb8_hjIruw"
conn = odbc.connect(r'Driver={Microsoft Access Driver (*.mdb, '
                    r'*.accdb)};DBQ=db\Кулинарная книга.mdb;')
cursor = conn.cursor()


# def start(update, context):
#     print('/start\t' + time.asctime())
#     update.message.reply_text('Привет! Я - бот-кулинар, я помогу тебе в поиске нужных рецептов. '
#                               'Ты можешь искать блюда как по категорям, так и по ингордиентам. '
#                               'Выбери в меню нужную категорию или напиши продукт в чат.')


def help(update, context):
    print('/help\t' + time.asctime())
    update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def start(update, context):
    print('/choice_1\t' + time.asctime())
    cursor.execute('select * from Разделы')
    keyboard = [[InlineKeyboardButton(row[1], callback_data=row[0])] for row in cursor.fetchall()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выбери категорию рецептов:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()
    print('Получил ответ\t' + time.asctime())
    cursor.execute('select Название from Книга where id_category={}'.format(query.data))
    data = cursor.fetchall()
    keyboard = []
    for pos in data[:4]:
        keyboard.append([InlineKeyboardButton(pos[0], callback_data=pos[0])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите блюдо из списка:")
    query.edit_message_reply_markup(reply_markup)


def print_receipt(name, update, context):
    cursor.execute('select name, ingredients, cooking, photo from Книга where name=?', name)
    name, ingredients, cooking, photo = cursor.fetchall()

    cap = f"{name}\n" \
          f"Состав: {ingredients}"
    context.bot.send_photo(update.message.chat_id, photo, caption=cap)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    print('Принимаем сообщение')
    updater.idle()


if __name__ == '__main__':
    main()
