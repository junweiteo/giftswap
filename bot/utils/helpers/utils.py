
import json
from html import escape

from pyrogram import Message


def html_escape(string, *args, **kwargs):
    if string is None:
        return None

    return escape(string, *args, **kwargs)


def plugin(name: str):
    return name.split('.')[-1]


def message_link(message: Message):
    if message.chat.username:
        return 'https://t.me/{}/{}'.format(message.chat.username, message.message_id)
    else:
        chat_id = str(message.chat.id).replace('-100', '')
        return 'https://t.me/c/{}/{}'.format(chat_id, message.message_id)


def inline_mention(user):
    return '<a href="tg://user?id={}">{}</a>'.format(user.id, html_escape(user.first_name))
