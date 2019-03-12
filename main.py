import logging
from consts import *
from handlers import *

from telegram.ext import Updater


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def main():
    upd = Updater(token=token, use_context=True)
    dp = upd.dispatcher

    dp.add_handler(start_handler)
    dp.add_handler(query_handler)
    dp.add_handler(change_page_handler)
    dp.add_handler(download_handler)

    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    main()

