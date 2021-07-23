from pyrogram import Client
from pyrogram import User
from pyrogram import __version__
from pyrogram.api.all import layer

from config import config

class Bot(Client):
    def __init__(self):
        super().__init__(
            config.pyrogram.session_name,
            api_id=config.pyrogram.api_id,
            api_hash=config.pyrogram.api_hash,
            bot_token=config.pyrogram.bot_token,
            workers=config.pyrogram.workers,
            plugins=dict(root='bot/plugins'),
            #workdir='.',
        )

        # noinspection PyTypeChecker
        self.me: User = None
        self.is_bot = None

    def start(self):
        super().start()

        self.me = self.get_me()
        self.is_bot = self.me.is_bot

    def stop(self):
        super().stop()
