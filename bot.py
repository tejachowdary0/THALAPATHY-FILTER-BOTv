import sys
import glob
import importlib
from pathlib import Path
import logging
from pyrogram import idle
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import pytz
from aiohttp import web
from plugins import web_server
import asyncio
from pyrogram import idle

ppath = "plugins/*.py"
files = glob.glob(ppath)

api_id = 27604683  # Replace with your API ID
api_hash = "ed52a1d0803b2ed84c5cca7f20535aac"  # Replace with your API Hash

LazyPrincessBot = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token="5855385200:AAEZCFFhA502Ue2i_plNdaP8QtVEFY5GxCM"  # Replace with your bot token
)

async def Lazy_start():
    try:
        print('\n')
        print('Initializing Lazy Bot')

        await LazyPrincessBot.start()

        bot_info = await LazyPrincessBot.get_me()
        LazyPrincessBot.username = bot_info.username

        for name in files:
            with open(name) as a:
                patt = Path(a.name)
                plugin_name = patt.stem.replace(".py", "")
                plugins_dir = Path(f"plugins/{plugin_name}.py")
                import_path = "plugins.{}".format(plugin_name)
                spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules["plugins." + plugin_name] = load
                print("Lazy Imported => " + plugin_name)

        if ON_HEROKU:
            asyncio.create_task(ping_server())

        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await Media.ensure_indexes()

        me = await LazyPrincessBot.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        LazyPrincessBot.username = '@' + me.username

        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)
        logging.info(script.LOGO)

        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")

        await LazyPrincessBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))

        app = web.AppRunner(await web_server())
        await app.setup()

        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        await idle()

    except pyrogram.errors.FloodWait as e:
        # Handle FloodWait error
        wait_seconds = e.x
        logging.warning(f"FloodWait: Waiting for {wait_seconds} seconds.")
        await asyncio.sleep(wait_seconds)
        await Lazy_start()

if __name__ == '__main__':
    try:
        asyncio.run(Lazy_start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
                
