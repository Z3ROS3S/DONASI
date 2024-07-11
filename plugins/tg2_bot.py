from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import API_HASH, APP_ID, TG_BOT_TOKEN_2, CHANNEL_ID

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
