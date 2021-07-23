
import random
import re
from collections import defaultdict

from pyrogram import Client
from pyrogram import Message
from pyrogram import Filters
from pyrogram import Emoji
from pyrogram.errors import BadRequest

from bot import bot
from bot.utils import utils
from config import config

__plugin__ = utils.plugin(__name__)


GIFT_SWAP_MESSAGE = """<a href="{message_link}">{chat_name}'s gift swap draw</a>: you are \
{receiver_mention}'s gifter! {gift}
"""

MATCH_RESULT = """I've been able to match <b>{number}</b> people! \
{party}{hands}
You should have received a message with the name of your match, go check it out :)"""

NOT_ENOUGH_PEOPLE = """Uh-oh, it looks like a lot of people here didn\'t start me yet. You must be at least in two :/"""

limit = 25

def reply_to_our_message_test(_, message):
    return message.reply_to_message and message.reply_to_message.from_user.id == bot.me.id


def bot_command_extended_test(_, message):
    if message.text:
        return bool(re.search(r'^\/(?:match)(?:@{})?$'.format(bot.me.username), message.text, re.I))


reply_to_our_message_filter = Filters.create(reply_to_our_message_test)

bot_command_extended_filter = Filters.create(bot_command_extended_test)


def list_to_text(users):
    if not isinstance(users, (list, tuple)):
        users = [users]

    if len(users) == 1:
        return utils.inline_mention(users[0])

    last_item_index = len(users) - 1
    users, last_user = users[:last_item_index], users[last_item_index:][0]

    return '{} and {}'.format(
        ', '.join([utils.inline_mention(u) for u in users]),
        utils.inline_mention(last_user)
    )


@Client.on_message(
    Filters.text & Filters.group & (
        bot_command_extended_filter
        | (reply_to_our_message_filter & Filters.regex(r'^(?:match)\b.*', flags=re.I))
    )
)
def on_pair(client: Client, message: Message):

    all_members = client.get_chat_members(message.chat.id, limit=limit)

    valid_members = list()
    for member in all_members:
        if member.user.is_bot:
            continue

        valid_members.append(member.user)

    chat_message = message.reply('<i>Matching users...</i> {}'.format(Emoji.GEAR))

    users_to_message = list()
    users_to_pick = list()
    for user in valid_members:
        try:
            client.send_chat_action(user.id, 'typing')

            users_to_message.append(user)
            users_to_pick.append(user)
        except BadRequest as br:
            continue

    number_of_users = len(users_to_message)
    assert(number_of_users == len(users_to_pick))

    if number_of_users < 2:
        chat_message.edit_text(NOT_ENOUGH_PEOPLE)
        return

    random.shuffle(users_to_pick)

    while users_to_message[-1].id == users_to_pick[0].id:
        random.shuffle(users_to_pick)

    chat_message.edit_text('<i>Sending messages...</i> {}'.format(Emoji.ENVELOPE))
    for user in users_to_message:
        pick = users_to_pick.pop() 
        if pick.id == user.id:
            old_pick = pick
            new_pick = users_to_pick.pop()
            users_to_pick.append(old_pick)
            pick = new_pick

        text = GIFT_SWAP_MESSAGE.format(
            receiver_mention=utils.inline_mention(pick),
            chat_name=utils.html_escape(message.chat.title),
            gift=Emoji.WRAPPED_GIFT,

            message_link=utils.message_link(chat_message),
        )
        client.send_message(user.id, text)

    text = MATCH_RESULT.format(
            party=Emoji.PARTYING_FACE,
            hands=Emoji.RAISING_HANDS_LIGHT_SKIN_TONE, 
            number=len(users_to_message))

    chat_message.edit_text(text)