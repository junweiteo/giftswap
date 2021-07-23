
from pyrogram import Client
from pyrogram import Message
from pyrogram import Filters
from pyrogram import Emoji

from bot.utils import utils
from config import config

__plugin__ = utils.plugin(__name__)

START_MESSAGE = """Hi hi {first_name}!
Let me help you to organise a <b>gift swap</b> {smiling} in your group chats :)
Just add me to a chat and I'll tell you what to do!

Use /help for more info"""

HELP_MESSAGE = """To use me, just add me to your group chat and I'll answer to one of your messages with 
"/match". I will send you your match via private message. 

{exclamation} <b>Note that I will include in the draw only the people who have started me in private message.</b>

{warning} This bot will not work with more than 25 members in the group."""

GROUP_COMMAND = """{} You have to use this command in a group where you've added me!
Use /help for more info"""


@Client.on_message(Filters.text & Filters.private & Filters.command(['start'], prefixes=['/']))
def on_start(_, message: Message):

    text = START_MESSAGE.format(
        first_name=utils.html_escape(message.from_user.first_name),
        smiling=Emoji.GRINNING_SQUINTING_FACE,
    )

    message.reply(text, disable_web_page_preview=True)


@Client.on_message(Filters.text & Filters.private & Filters.command(['help'], prefixes=['/']))
def on_help(_, message: Message):

    text = HELP_MESSAGE.format(
        exclamation=Emoji.DOUBLE_EXCLAMATION_MARK,
        warning=Emoji.WARNING
    )

    message.reply(text, disable_web_page_preview=True)


@Client.on_message(Filters.text & Filters.private & Filters.command(['match'], prefixes=['/']))
def on_group_command(_, message: Message):

    message.reply(GROUP_COMMAND.format(Emoji.WARNING), disable_web_page_preview=True)