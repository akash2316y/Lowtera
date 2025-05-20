from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Start Flask in background
threading.Thread(target=run_flask).start()

API_ID = int(os.getenv("API_ID"))   
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

TERABOX_API = "https://terabox.web.id/url?url={url}&token=akash_8110231942"

@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Send Me Terabox Links.")

@bot.on_message(filters.text & ~filters.command("start"))
async def handle_terabox(client, message):
    url = message.text.strip()

    try:
        r = requests.get(TERABOX_API.format(url))
        data = r.json()

        direct_link = data.get("direct_link")
        filename = data.get("filename")
        original_link = data.get("link")
        size = data.get("size")
        thumbnail = data.get("thumbnail")

        if not direct_link:
            await message.reply_text("Kuch galti ho gayi, direct link nahi mila.")
            return

        caption = (
            f"**File:** `{filename}`\n"
            f"**Size:** `{size}`\n\n"
            f"🎬 How To Watch Video, Click here\n\n"
            f"🔗 [Original Terabox Link]({original_link})"
        )

        buttons = [
            [InlineKeyboardButton("ɴᴏʀᴍᴀʟ ᴅᴏᴡɴʟᴏᴀᴅ", url=direct_link)],
            [InlineKeyboardButton("ғᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ", url=original_link)]
        ]

        if thumbnail:
            await message.reply_photo(
                photo=thumbnail,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await message.reply_text(
                text=caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    except Exception as e:
        await message.reply_text(f"Error: {e}")

bot.run()
