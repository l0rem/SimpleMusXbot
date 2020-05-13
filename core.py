import logging
from handlers import start_handler, query_handler, switch_track_handler, download_track_handler
from decouple import config
from telegram.ext import Updater


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.getLevelName(config('LOG_LEVEL',
                                                      default='INFO')))

bot_token = config('BOT_TOKEN')


upd = Updater(bot_token,
              use_context=True)
dp = upd.dispatcher


def main():

    dp.add_handler(start_handler)
    dp.add_handler(query_handler)
    dp.add_handler(switch_track_handler)
    dp.add_handler(download_track_handler)

    upd.start_polling()

    logging.info("Ready and listening for updates...")
    upd.idle()


if __name__ == '__main__':
    main()

