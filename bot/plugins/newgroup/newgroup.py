
from pyrogram import Client
from pyrogram import Message
from pyrogram import Filters
from pyrogram import InlineKeyboardMarkup
from pyrogram import InlineKeyboardButton
from pyrogram import Emoji

from bot import bot
from bot.utils import utils
from config import config

__plugin__ = utils.plugin(__name__)

NEW_CHAT_MESSAGE = """Hi! I am a bot that matches people in the group randomly for a gift exchange! {cool}{confetti}{gift} 
To participate, everyone must <b>start the bot in private message</b> first. 
After all participants have started the bot, send "/match" here to start the draw.
"""


def bot_added(_, message: Message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.is_self:
                return True


bot_added_filter = Filters.create(bot_added)


@Client.on_message(bot_added_filter)
def on_new_group(client: Client, message: Message):

    client.send_message(message.chat.id, NEW_CHAT_MESSAGE.format(
        cool=Emoji.SMILING_FACE_WITH_SUNGLASSES,
        confetti=Emoji.PARTY_POPPER,
        gift=Emoji.WRAPPED_GIFT
    ))