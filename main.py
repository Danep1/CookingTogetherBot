from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, \
    CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pyodbc as odbc

TOKEN = "1181461577:AAEGd2heqoKZfE0ZJHgnlhSXvRb8_hjIruw"
conn = odbc.connect(r'Driver={Microsoft Access Driver (*.mdb, '
                    r'*.accdb)};DBQ=db\Кулинарная книга.mdb;')
cursor = conn.cursor()


def start(update, context):
    cursor.execute('select * from Разделы')
    keyboard = [InlineKeyboardButton(row[0], callback_data=row[0]) for row in cursor.fetchall()]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def help(update, context):
    update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Selected option: {}".format(query.data))


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
