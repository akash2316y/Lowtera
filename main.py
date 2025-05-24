from pyrogram import Client, filters
import random, string, os, threading
from flask import Flask

# Flask keep-alive server
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

bot = Client("insta_3char_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Generate 3-letter usernames
def generate_usernames(count):
    return [
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
        for _ in range(count)
    ]

@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Send /get to receive 3-letter Instagram-style usernames.")

@bot.on_message(filters.command("get"))
async def get(_, msg):
    names = generate_usernames(30)  # Generate 30 usernames
    result = "\n".join([f"`{u}` - Available" for u in names])
    await msg.reply(f"Here are 3-letter usernames:\n\n{result}")

bot.run()
