import sys
import glob
import importlib
import logging
import asyncio
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional
from pyrogram import types
from Script import script
from datetime import date, datetime
import pytz
from aiohttp import web
from plugins import web_server
import time

from util.keepalive import ping_server
from lazybot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
LazyPrincessBot = Client("LazyPrincessBot")

async def Lazy_start():
    print('\n')
    print('Initializing Lazy Bot')

    try:
        await LazyPrincessBot.start()
        bot_info = await LazyPrincessBot.get_me()
    except pyrogram.errors.FloodWait as e:
        wait_time = e.x
        print(f"Got FloodWait error. Waiting for {wait_time} seconds.")
        time.sleep(wait_time)
        await LazyPrincessBot.start()

    LazyPrincessBot.username = bot_info.username
    await initialize_clients()

    # ... (rest of your existing code)

if __name__ == '__main__':
    try:
        asyncio.run(Lazy_start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
        
