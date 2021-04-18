import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from classes.singleton import Singleton
from flask import request
from bot.creds import bot_token, bot_user_name,URL



class TeleBot(metaclass = Singleton):
    def __init__(self):
        self.bot = telegram.Bot(bot_token)
        self.updater = Updater(token = bot_token)
        self.dispatcher = self.updater.dispatcher

    def get_token(self):
        return bot_token

    def get_json_message(self):
        return telegram.Update.de_json(request.get_json(force=True), self.bot)

    def add_handler(self, handler):
        self.dispatcher.add_handler(handler)

    def set_start_handler(self, start_message):
        def start(update, context):
            print(update, context)
            context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)

        start_handler = CommandHandler('start', start)
        self.dispatcher.add_handler(start_handler)

    def init(self):
        self.updater.start_polling()


    def idle(self):
        self.updater.idle()
        
    def stop(self):
        self.updater.stop()