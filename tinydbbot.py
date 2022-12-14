from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
import os
from tinydb import TinyDB, Query
from tinydb.database import Document

TOKEN = os.environ['TOKEN']
db    = TinyDB('db.json')

updater: Updater = Updater(TOKEN)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    update.message.reply_text(text='Xabarlaringizni yozib olish boshlandi!')


def insert_into_db(update: Update, context: CallbackContext):
    User = Query()

    if not db.contains(cond=User.text==update.message.text):
        data = {
            'user_id': update.message.from_user.id,
            'text': update.message.text
        }
        document = Document(value=data, doc_id=update.update_id)
        db.insert(document=document)
        update.message.reply_text('done')
    else:
        update.message.reply_text('already done')






dispatcher.add_handler(handler=CommandHandler(command='start', callback=start))
dispatcher.add_handler(handler=MessageHandler(filters=Filters.text, callback=insert_into_db))

updater.start_polling()
updater.idle()