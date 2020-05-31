import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram_bot import start, text, error

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')


def main():
    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
