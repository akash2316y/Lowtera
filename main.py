from pyrogram import Client, filters
import random, string, os, threading
from flask import Flask

# Flask for keep-alive (Koyeb etc.)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

threading.Thread(target=run_flask).start()

# Telegram bot setup
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("insta_username_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def generate_usernames(count):
    return [
        'e' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        for _ in range(count)
    ]

@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Send /get to get 50 Instagram-style usernames starting with 'e'.")

@bot.on_message(filters.command("get"))
async def get(_, msg):
    names = generate_usernames(50)
    result = "\n".join([f"`{u}` - Available" for u in names])
    await msg.reply(f"Here are 50 usernames starting with 'e':\n\n{result}")

bot.run()
