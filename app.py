from flask import Flask, request
from budgetBot.classes.teleBot import TeleBot
from budgetBot.classes.Db import Db
from budgetBot.classes.models.new_expense import NewExpense

import re
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


logger = logging.getLogger(__name__)

ACTION_PARSE, NEW_TRANSACTION, AMOUNT, BUSINESS, PRODUCT, PAYMENT_METHOD, PAYMENTS, END_TRANSACTION = range(8)

def start(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['new', 'report']]

    update.message.reply_text("""
                              Hi, I am budgetBot, testing purposes, \n
                              What do ya want, ya twat?
                            """, reply_markup=ReplyKeyboardMarkup(reply_keyboard))            
    return ACTION_PARSE

def parse_action(update:Update, _: CallbackContext) ->int:
    action = update.message.text.lower()
    user = update.message.chat.username
    logger.info(f"action: {action}, context: {_}")

    if action == 'report':
        pass
    elif action == 'new':
        expense_model = NewExpense()
        expense_model.set_default_values()
        expense_model.set_user(user)
        return NEW_TRANSACTION
    elif action == 'commit':
        return END_TRANSACTION

def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.chat.username
    logger.info("User %s canceled the conversation.", user)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def new_transaction(update: Update, _: CallbackContext) -> int:
     update.message.reply_text("""
                              ok, what's the name of the place what robbed yo ass? \n
                            """)            
     return BUSINESS

def set_business_name(update: Update, _: CallbackContext) -> int:
    business = update.message.text
    logger.info("Business name is: %s ", business)
    expense_model = NewExpense()
    expense_model.set_business_name(business)
    update.message.reply_text("""
                              And what did you buy? \n
                            """)            
    return PRODUCT

def set_product(update: Update, _: CallbackContext) -> int:
    product = update.message.text
    expense_model = NewExpense()
    expense_model.set_product(product)
    logger.info("Product name is: %s ", product)

    update.message.reply_text("""
                              how much did we part with? \n
                            """)            
    return AMOUNT


def set_amount(update: Update, _: CallbackContext) -> int:
    amount = update.message.text
    logger.info("amount name is: %s ", amount)
    expense_model = NewExpense()
    expense_model.set_amount(amount)
    update.message.reply_text("""
                              how many payments? \n
                            """)            
    return PAYMENTS

def set_payments(update: Update, _: CallbackContext) -> int:
    payments = update.message.text
    expense_model = NewExpense()
    expense_model.set_payments(payments)
    methods_arr = [["cash", "credit", "paypal", "check" ,"crypto"]]
    logger.info("payments: %s ", payments)

    update.message.reply_text("""
                              what method did you use? \n
                            """, reply_markup=ReplyKeyboardMarkup(methods_arr, one_time_keyboard=True))            
    return PAYMENT_METHOD


def set_method(update: Update, _: CallbackContext) -> int:
    method = update.message.text
    logger.info("method: %s ", method)
    expense_model = NewExpense()
    expense_model.set_payment_method(method)
    expanse_dict = expense_model.to_dict()
    expanse_string = "\n".join(["{}: {}".format(key, val) for key, val in expanse_dict.items()])
    update.message.reply_text(f"""
                              Thank You! \n
                              your transaction lookes like this: \n
                              {expanse_string} \n
                              if you want to commit this type 'commit'
                              else type 'new'
                            """)            
    return ACTION_PARSE


def end_transaction(update: Update, _: CallbackContext) -> int:
    Database = Db()
    expense_model = NewExpense()
    if expense_model.product == '':
        update.message.reply_text(f"""
                              not enough data to commit, \n
                              please start again by typing 'new'
                            """)    
        return ACTION_PARSE
    Database.insert(tb_name = "tb_expenses", insert_model=expense_model)
    pass

def main() -> None:
    bot = TeleBot()

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)], 
        states = {
            ACTION_PARSE: [MessageHandler(Filters.text, parse_action)],
            NEW_TRANSACTION: [MessageHandler(Filters.text & ~Filters.command, new_transaction)],
            BUSINESS: [MessageHandler(Filters.text & ~Filters.command, set_business_name)],
            PRODUCT: [MessageHandler(Filters.text & ~Filters.command, set_product)],
            AMOUNT: [MessageHandler(Filters.text & ~Filters.command, set_amount)],
            PAYMENTS: [MessageHandler(Filters.text & ~Filters.command, set_payments)],
            PAYMENT_METHOD: [MessageHandler(Filters.text & ~Filters.command, set_method)],
            END_TRANSACTION: [MessageHandler(Filters.text & ~Filters.command, end_transaction)],

        }
        , fallbacks = [CommandHandler('cancel', cancel)])
    
    bot.add_handler(conv_handler)
    bot.init()
    bot.idle()
   
    print(bot)


if __name__ == '__main__':
    main()

