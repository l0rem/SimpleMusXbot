from telegram.ext import (CommandHandler, MessageHandler, Filters, CallbackQueryHandler)
from telegram import (ParseMode, InlineKeyboardButton, InlineKeyboardMarkup)
from engine import *
from consts import song_form, storage_cid
import os
from random import randint


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='<b>Hello there!</b>\n'
                                                                  'The only command this bot supports is /start. '
                                                                  'Just send performer and(/ or) title of wished song '
                                                                  'and choose one from list.',
                             parse_mode=ParseMode.HTML)


start_handler = CommandHandler('start', start)


def query(update, context):
    q = update.message.text

    if 'mids' in context.chat_data.keys() and len(context.chat_data['mids']) != 0:
        for mid in context.chat_data['mids']:
            try:
                context.bot.delete_message(update.message.chat_id, mid)
            except Exception as e:
                print(e)
    context.chat_data['mids'] = list()

    results = parse_html(get_html(add_url(format_query(q))))

    if len(results) == 0:
        context.bot.send_message(update.message.chat_id, '<b>Didnt find any matching songs.</b>'
                                                         '\nTry changing search query.', parse_mode=ParseMode.HTML)
        return
    mids = []
    context.chat_data.update({'results': results})
    context.chat_data.update({'current_page': 0})
    mids.append(context.bot.send_message(update.message.chat_id, '<b>###### Page 1 ######</b>',
                                         parse_mode=ParseMode.HTML).message_id)

    for i in range(5):
        d_button = InlineKeyboardButton(text='\U00002B07 Download', callback_data='download:{}'.format(i))
        kb = InlineKeyboardMarkup([[d_button]])
        mids.append(context.bot.send_message(update.message.chat_id, song_form.format(results[i]['performer'],
                                                                                      results[i]['title'],
                                                                                      results[i]['duration']),
                                             parse_mode=ParseMode.HTML,
                                             reply_markup=kb).message_id)

    if len(results) > 5:
        next_b = InlineKeyboardButton('Next page \U000027A1', callback_data='+page')
        page_kb = InlineKeyboardMarkup([[next_b]])
    else:
        page_kb = InlineKeyboardMarkup([[]])

    mids.append(context.bot.send_message(update.message.chat_id, '<b>###### Page 1 ######</b>', parse_mode=ParseMode.HTML,
                                         reply_markup=page_kb).message_id)
    context.chat_data.update({'mids': mids})


query_handler = MessageHandler(Filters.text, query, pass_chat_data=True)


def change_page(update, context):
    if update.callback_query.data[0] == '+':
        page = context.chat_data['current_page'] + 1
    else:
        page = context.chat_data['current_page'] - 1

    for mid in context.chat_data['mids']:
        context.bot.delete_message(update.callback_query.message.chat_id, mid)
    context.chat_data.update({'current_page': page})
    mids = list()
    mids.append(context.bot.send_message(update.callback_query.message.chat_id, '<b>###### Page {} #####</b>'.format(page + 1),
                                         parse_mode=ParseMode.HTML).message_id)
    for i in range(5):
        d_button = InlineKeyboardButton(text='\U00002B07 Download', callback_data='download:{}'.format(i + 5*page))
        kb = InlineKeyboardMarkup([[d_button]])
        mids.append(context.bot.send_message(update.callback_query.message.chat_id,
                                             song_form.format(context.chat_data['results'][i + page*5]['performer'],
                                                              context.chat_data['results'][i + page*5]['title'],
                                                              context.chat_data['results'][i + page*5]['duration']),
                                             parse_mode=ParseMode.HTML,
                                             reply_markup=kb).message_id)

    next_b = InlineKeyboardButton('Next page\U000027A1', callback_data='+page')
    prev_b = InlineKeyboardButton('\U00002B05Previous page', callback_data='-page')

    if len(context.chat_data['results']) > 5 + page*5 and context.chat_data['results'][page*5] == context.chat_data['results'][0]:
        page_kb = InlineKeyboardMarkup([[next_b]])
    elif len(context.chat_data['results']) > 5 + page*5 and context.chat_data['results'][page*5] != context.chat_data['results'][0]:
        page_kb = InlineKeyboardMarkup([[prev_b, next_b]])
    elif len(context.chat_data['results']) <= 5 + page*5:
        page_kb = InlineKeyboardMarkup([[prev_b]])
    else:
        page_kb = InlineKeyboardMarkup([[]])

    mids.append(context.bot.send_message(update.callback_query.message.chat_id,
                                         '<b>####### Page {} #######</b>'.format(page + 1),
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=page_kb).message_id)
    context.chat_data.update({'mids': mids})


change_page_handler = CallbackQueryHandler(change_page, pattern='(.*)page', pass_chat_data=True)


def download(update, context):
    context.bot.answerCallbackQuery(update.callback_query.id, text='Started downloading...')
    song = context.chat_data['results'][int(update.callback_query.data.split(':')[1])]
    d_url = song.get('d_link')
    performer = song.get('performer')
    title = song.get('title')
    r = requests.get(d_url, stream=True)
    fname = (performer + '-' + title + str(randint(1, 999)) + '.mp3').replace('/', 'or')
    with open(fname, 'bw') as f:
        for chunk in r.iter_content(2048):
            f.write(chunk)
    path = os.path.abspath(fname)
    size = ((os.path.getsize(path)) / 1024) / 1024
    size = round(size, 2)
    if size > 50:
        os.remove(path)
        context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                 text='Song <b>{}</b> by <b>{}</b> is too big.\nI can\'t upload it.'.format(title,
                                                                                                            performer),
                                 parse_mode=ParseMode.HTML)
        return
    fid = 0
    for i in range(10):
        try:
            audio = open(path, 'rb')
            fid = context.bot.send_audio(chat_id=storage_cid,
                                         performer=performer,
                                         title=title,
                                         audio=audio,
                                         timeout=1000).audio.file_id
            audio.close()
        except Exception as e:
            print(e)
            continue
        break
    os.remove(path)
    if not fid:
        context.bot.send_message(update.callback_query.message.chat_id,
                                 '<b>Sorry, an error occured while uploading song.</b>')
        return
    context.bot.send_audio(update.callback_query.message.chat_id,
                           fid)


download_handler = CallbackQueryHandler(download, pattern='download:(.*)', pass_chat_data=True)


