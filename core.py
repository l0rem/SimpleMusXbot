import logging
import dbmodels
from handlers import start_handler, query_handler, switch_track_handler, download_track_handler
from decouple import config
from telegram.ext import Updater


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.getLevelName(config('LOG_LEVEL',
                                                      default='DEBUG')))

env = config('ENV',
             default='DEV')

bot_token = config('BOT_TOKEN',
                   default='token')

webhook_url = config('WEBHOOK_URL',
                     default='url')


upd = Updater(bot_token,
              use_context=True)
dp = upd.dispatcher


def main():

    dp.add_handler(start_handler)
    dp.add_handler(query_handler)
    dp.add_handler(switch_track_handler)
    dp.add_handler(download_track_handler)

    if env == 'DEV':
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

