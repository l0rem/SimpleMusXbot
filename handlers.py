from telegram.ext import (CommandHandler, MessageHandler, Filters, CallbackQueryHandler, callbackcontext, run_async)
from telegram import (ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Update)
from telegram.error import BadRequest
from musxtools import parse_html, get_html, add_url, format_query, store_track
import requests
from phrases import track_form, start_phrase, no_results_phrase, searching_phrase, download_started_phrase,\
    file_too_large_phrase, error_occurred_phrase
from buttons import download_button_text, next_button_text, previous_button_text
from chattools import clean_chat, get_cid, store_user
import os
from random import randint


def start_callback(update: Update, context: callbackcontext):
    """ /start callback (private chat only)"""

    clean_chat(update, context)
    store_user(update)

    update.message.reply_text(text=start_phrase,
                              parse_mode=ParseMode.HTML)


start_handler = CommandHandler(command='start',
                               callback=start_callback,
                               pass_chat_data=True,
                               filters=Filters.private)


def query_callback(update: Update, context: callbackcontext):
    """ search query callback (private chat only) """

    cid = get_cid(update)
    q = update.message.text

    clean_chat(update, context)
    store_user(update)

    message_id = context.bot.send_message(chat_id=cid,
                                          text=searching_phrase,
                                          parse_mode=ParseMode.HTML).message_id

    results = parse_html(get_html(add_url(format_query(q))))

    if len(results) == 0:

        context.bot.edit_message_text(chat_id=cid,
                                      message_id=message_id,
                                      text=no_results_phrase,
                                      parse_mode=ParseMode.HTML)

        context.chat_data.update({'message_ids': [message_id]})

        return

    context.chat_data.update({'results': results})

    download_button = InlineKeyboardButton(text=download_button_text,
                                           callback_data='download:0')

    if len(results) > 1:
        next_button = InlineKeyboardButton(text=next_button_text,
                                           callback_data='track:1')

        keyboard = InlineKeyboardMarkup([[download_button],
                                         [next_button]])
    else:

        keyboard = InlineKeyboardMarkup([[download_button]])

    context.bot.edit_message_text(chat_id=cid,
                                  message_id=message_id,
                                  text=track_form.format(1,
                                                         len(results),
                                                         results[0]['performer'],
                                                         results[0]['title'],
                                                         results[0]['duration']),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=keyboard)

    context.chat_data.update({'message_ids': [message_id]})


query_handler = MessageHandler(callback=query_callback,
                               filters=Filters.text,
                               pass_chat_data=True)


@run_async
def switch_track_callback(update: Update, context: callbackcontext):

    cid = get_cid(update)
    mid = update.callback_query.message.message_id
    next_track = int(update.callback_query.data.split(':')[-1])
    results = context.chat_data['results']

    download_button = InlineKeyboardButton(text=download_button_text,
                                           callback_data='download:{}'.format(next_track))

    next_button = InlineKeyboardButton(text=next_button_text,
                                       callback_data='track:{}'.format(next_track + 1))

    previous_button = InlineKeyboardButton(text=previous_button_text,
                                           callback_data='track:{}'.format(next_track - 1))
    if next_track == len(results) - 1:

        keyboard = InlineKeyboardMarkup([[download_button],
                                         [previous_button]])

    elif next_track == 0:

        keyboard = InlineKeyboardMarkup([[download_button],
                                         [next_button]])

    else:

        keyboard = InlineKeyboardMarkup([[download_button],
                                         [previous_button, next_button]])

    context.bot.edit_message_text(chat_id=cid,
                                  message_id=mid,
                                  text=track_form.format(next_track + 1,
                                                         len(results),
                                                         results[next_track]['performer'],
                                                         results[next_track]['title'],
                                                         results[next_track]['duration']),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=keyboard)


switch_track_handler = CallbackQueryHandler(callback=switch_track_callback,
                                            pattern='track:(.*)',
                                            pass_chat_data=True)


@run_async
def download_track_callback(update: Update, context: callbackcontext):

    cid = get_cid(update)

    try:

        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                        text=download_started_phrase)
    except BadRequest:          # user spams bot with downloads
        pass

    song_index = int(update.callback_query.data.split(':')[-1])
    song = context.chat_data['results'][song_index]

    download_url = song['download_url']
    performer = song['performer']
    title = song['title']

    r = requests.get(download_url, stream=True)
    file_name = (performer + '-' + title + str(randint(0, 9999)) + '.mp3').replace('/', ' ')

    with open(file_name, 'bw') as file:
        for chunk in r.iter_content(2048):
            file.write(chunk)

    path = os.path.abspath(file_name)
    size = ((os.path.getsize(path)) / 1024) / 1024
    size = round(size, 2)

    if size > 50:
        os.remove(path)

        try:

            context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                            text=file_too_large_phrase)

        except BadRequest:
            pass

        return

    file_id = 0

    audio = open(path, 'rb')

    for i in range(5):
        try:
            message = context.bot.send_audio(chat_id=cid,
                                             performer=performer,
                                             title=title,
                                             audio=audio,
                                             timeout=1000)

            file_id = message.audio.file_id

        except BadRequest:              # this is the only way to make sure the file was sent
            continue
        break

    audio.close()
    os.remove(path)

    if file_id == 0:

        try:

            context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                            text=error_occurred_phrase)

        except BadRequest:          # callback_query is too old

            pass

    store_track(uid=cid,
                title=title,
                performer=performer,
                file_id=file_id,
                download_url=download_url)


download_track_handler = CallbackQueryHandler(pattern='download:(.*)',
                                              callback=download_track_callback,
                                              pass_chat_data=True)


