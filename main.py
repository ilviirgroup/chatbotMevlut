import constants as key
from telegram.ext import *
import responses as r

print("Bot started ...")

def start_command(update,context):
    update.message.reply_text("Type smth random to get started")

def help_command(update,context):
    update.message.reply_text("if u need help")

def handle_message(update, context):
    text = str(update.message.text).lower()
    responses = r.sample_responses(text)
    update.message.reply_text(responses)
def show_ngrams(update, context):
    update.message.reply_text("input any text to see ngrams")
def error(update,context):
        print(f"update {update} caused error")

def main():
    updater = Updater(key.API_KEY,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start_command))
    dp.add_handler(CommandHandler('start',help_command))
    dp.add_handler(CommandHandler('ngrams',show_ngrams))
    dp.add_handler(MessageHandler(Filters.text,handle_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

main()