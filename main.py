from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, \
    CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pyodbc as odbc

TOKEN = "1181461577:AAEGd2heqoKZfE0ZJHgnlhSXvRb8_hjIruw"
conn = odbc.connect(r'Driver={Microsoft Access Driver (*.mdb, '
                    r'*.accdb)};DBQ=C:\Users\epikm\Downloads\kulinarnaya_kniga\Кулинарная '
                    r'книга.mdb;')


def start(update, context):
    keyboard = [InlineKeyboardButton("Option 1", callback_data='1'),
                InlineKeyboardButton("Option 2", callback_data='2'),
                InlineKeyboardButton("Option 3", callback_data='3')]

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
