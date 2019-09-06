import logging
from handlers import *
from decouple import config
from telegram.ext import Updater


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

env = config('ENV', default='dev')

bot_token = config('BOT_TOKEN', default='token')

webhook_url = config('WEBHOOK_URL', default='url')


upd = Updater(bot_token,
              use_context=True)
dp = upd.dispatcher


def main():

    dp.add_handler(start_handler)
    dp.add_handler(query_handler)
    dp.add_handler(change_page_handler)
    dp.add_handler(download_handler)

    if env == 'dev':
        upd.start_polling()
    else:

        upd.start_webhook(listen='0.0.0.0',
                          port=8080,
                          url_path=bot_token)

        upd.bot.set_webhook(webhook_url + bot_token)

    logging.info("Ready and listening for updates...")
    upd.idle()


if __name__ == '__main__':
    main()

