from telegram import Update
from telegram.ext import callbackcontext
from dbmodels import Users


def clean_chat(update: Update, context: callbackcontext):

    if 'message_ids' in context.chat_data.keys():

        cid = get_cid(update)

        for mid in context.chat_data['message_ids']:
            try:
                context.bot.delete_message(chat_id=cid,
                                           message_id=mid)
            except Exception as e:
                print(e)

    context.chat_data['message_ids'] = list()


def get_cid(update: Update):

    return update.effective_message.chat.id


def get_uid(update: Update):

    return update.effective_message.from_user.id


def store_user(update: Update):

    uid = update.effective_message.from_user.id
    user_entry = Users.select().where(Users.uid == uid)

    if user_entry.exists():
        return

    username = update.effective_message.from_user.username
    if username is None:
        username = update.effective_message.from_user.first_name

    Users.create(uid=uid,
                 username=username)
    



