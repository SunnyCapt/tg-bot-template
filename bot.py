import re
import sys
from logging import getLogger

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.parsemode import ParseMode

from config.settings import *
from utils import log, Views, DataManager

logger = getLogger("general")


@log
def start(update, context):
    view = Views.render_start()
    update.message.reply_text(view, parse_mode=ParseMode.HTML)


@log
def command_handler(update, context):
    """Processing commands with a dynamic part"""
    data = None
    if re.match("^/example_command_[0-9]*$", update.message.text) is not None:
        data = DataManager.get_example_command_data(update, context)

    view = Views.render_example_command(data) if data is not None else f"{update.message.text} command not found"
    update.message.reply_text(view, parse_mode=ParseMode.HTML)


@log
def help_command(update, context):
    message = Views.render_help()
    update.message.reply_text(message, parse_mode=ParseMode.HTML)


def error(update, context):
    """Log errors caused by updates"""
    logger.error(context.error)
    update.message.reply_text("something broke")


try:
    BOT_TOKEN = BOT_TOKEN or (sys.argv[1] if len(sys.argv) > 1 else None)
    assert BOT_TOKEN is not None
except AssertionError:
    logger.error(f"Wrong token config")
    exit(-1)


def run_bot():
    logger.info("Start polling bot")
    updater = Updater(BOT_TOKEN, use_context=True, **({"request_kwargs": REQUEST_KWARGS} if REQUEST_KWARGS is not None else {}))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, command_handler))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_bot()
