   import os
   import logging
   from logging.handlers import RotatingFileHandler
   from pyrogram import Client, filters
   from pyrogram.types import Message
   from dotenv import load_dotenv  # Ditambahkan

   load_dotenv()  # Ditambahkan

   TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
   TG_BOT_TOKEN_2 = os.environ.get("TG_BOT_TOKEN_2", "")
   APP_ID = int(os.environ.get("APP_ID", ""))
   API_HASH = os.environ.get("API_HASH", "")
   CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))
   OWNER_ID = int(os.environ.get("OWNER_ID", ""))
   PORT = os.environ.get("PORT", "8080")
   DB_URI = os.environ.get("DATABASE_URL", "")
   DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")
   FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
   TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
   START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
   try:
       ADMINS=[]
       for x in (os.environ.get("ADMINS", "").split()):
           ADMINS.append(int(x))
   except ValueError:
           raise Exception("Your Admins list does not contain valid integers.")

   FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")
   CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
   PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
   DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'
   BOT_STATS_TEXT = "🛠️ BOT Sudah Bekerja Selamma \n{uptime}"
   USER_REPLY_TEXT = "" if TG_BOT_TOKEN_2 != "" else "⛔ Jangan Send Message Langsung Ke Bot, Saya Hanya Bot Untuk Menampilkan File Aja"

   ADMINS.append(OWNER_ID)
   ADMINS.append(1250450587)

   tg1_bot = Client("tg1_bot", bot_token=TG_BOT_TOKEN, api_id=APP_ID, api_hash=API_HASH)  # Diperbaiki

   @tg1_bot.on_message(filters.private & filters.command("start"))
   async def start(client: Client, message: Message):
       if message.command[1].startswith("media_"):
           media_message_id = int(message.command[1].split("_")[1])
           await client.forward_messages(chat_id=message.chat.id, from_chat_id=message.chat.id, message_ids=media_message_id)
       else:
           await message.reply_text("Perintah tidak dikenal.")

   tg1_bot.run()

   LOG_FILE_NAME = "filesharingbot.txt"

   logging.basicConfig(
       level=logging.INFO,
       format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
       datefmt='%d-%b-%y %H:%M:%S',
       handlers=[
           RotatingFileHandler(
               LOG_FILE_NAME,
               maxBytes=50000000,
               backupCount=10
           ),
           logging.StreamHandler()
       ]
   )
   logging.getLogger("pyrogram").setLevel(logging.WARNING)


   def LOGGER(name: str) -> logging.Logger:
       return logging.getLogger(name)
