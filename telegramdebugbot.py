import telegram
import logging
import json

from telegram import Message, Chat, Update, Bot, MessageEntity, ParseMode, TelegramObject, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, run_async, Filters, Handler, InlineQueryHandler
from os import path

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

if path.exists("config.py"):
    import config
else:
    logger.error("config.py was not found")
    exit(-1)

def tgoToJson(tgo: TelegramObject):
    return json.dumps(tgo.to_dict(), sort_keys=True, indent=2)

@run_async
def dump_everything(bot: Bot, update: Update):
    message = update.effective_message
    message.reply_text('```\n' + tgoToJson(update) + '\n```', ParseMode.MARKDOWN)

@run_async
def dump_everything_inline(bot: Bot, update: Update):
    update.inline_query
    bot.answerInlineQuery(update.inline_query.id, [InlineQueryResultArticle('dump','Dump', InputTextMessageContent('```\n' + tgoToJson(update) + '\n```', ParseMode.MARKDOWN))])

@run_async
def dump(bot: Bot, update: Update):
    message = update.effective_message
    if (message.reply_to_message):
        message.reply_to_message.reply_text('```\n' + tgoToJson(message.reply_to_message) + '\n```', ParseMode.MARKDOWN)
    else:
        message.reply_text('Tf u trying to do')


updater = telegram.ext.Updater(config.TOKEN)
dispatcher = updater.dispatcher

dump_handler = CommandHandler('dump', dump)
dispatcher.add_handler(dump_handler)

dump_everything_handler = MessageHandler(Filters.private, dump_everything)
dispatcher.add_handler(dump_everything_handler)

dump_everything_inline_handler = InlineQueryHandler(dump_everything_inline, pass_user_data=True)
dispatcher.add_handler(dump_everything_inline_handler)

updater.start_polling(timeout=15, read_latency=4)
updater.idle()
