#(©)Codexbotz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_TOKEN_2, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
        self.bot2 = Client(
            name="Bot2",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN_2
        )

    async def start(self):
        await super().start()
        await self.bot2.start()
        usr_bot_me = await self.get_me()
        usr_bot_me2 = await self.bot2.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz")
        self.LOGGER(__name__).info(f""" \n\n       
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
                                          """)
        self.username = usr_bot_me.username
        self.username2 = usr_bot_me2.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        await self.bot2.stop()
        self.LOGGER(__name__).info("Bot stopped.")

# New bot functionality
user_data = {}

tg2_bot = Client("tg2_bot", api_id=APP_ID, api_hash=API_HASH, bot_token=TG_BOT_TOKEN_2)

@tg2_bot.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text(
        "Hallo Kami Asistane Penerima Menfess",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("CW", callback_data="gender_cw"), InlineKeyboardButton("CWO", callback_data="gender_cwo")]
        ])
    )

@tg2_bot.on_callback_query(filters.regex(r"^gender_"))
async def gender_selection(client: Client, callback_query):
    gender = callback_query.data.split("_")[1]
    user_data[callback_query.from_user.id] = {"gender": gender}
    await callback_query.message.edit_text(
        "Jenis Konten",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sexual", callback_data="content_sexual"), InlineKeyboardButton("Biasa", callback_data="content_biasa")]
        ])
    )

@tg2_bot.on_callback_query(filters.regex(r"^content_"))
async def content_selection(client: Client, callback_query):
    content = callback_query.data.split("_")[1]
    user_data[callback_query.from_user.id]["content"] = content
    await callback_query.message.edit_text("Kamu Domisili mana?")

@tg2_bot.on_message(filters.private & ~filters.command("start"))
async def handle_user_input(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.reply_text("Silakan mulai dengan /start")
        return

    if "domisili" not in user_data[user_id]:
        user_data[user_id]["domisili"] = message.text
        await message.reply_text("Masukan Pesan Kamu untuk Pap kamu nanti")
    elif "pesan" not in user_data[user_id]:
        user_data[user_id]["pesan"] = message.text
        await message.reply_text("Sekarang Kirim Media yang Ingin Kamu bagikan")
    elif "media" not in user_data[user_id]:
        user_data[user_id]["media"] = message
        await send_to_channel(client, user_id)

async def send_to_channel(client: Client, user_id):
    data = user_data[user_id]
    gender = data["gender"]
    content = data["content"]
    domisili = data["domisili"]
    pesan = data["pesan"]

    text = f"Jenis Kelamin: {gender}\nJenis Konten: {content}\nDomisili: {domisili}\nPesan: {pesan}"
    await client.send_message(CHANNEL_ID, text)

    # Generate a link to the media message
    media_link = f"https://t.me/{client.username}?start=media_{data['media'].message_id}"
    await client.send_message(CHANNEL_ID, f"Media Link: {media_link}")

    del user_data[user_id]

tg2_bot.run()
