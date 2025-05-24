from pyrogram import Client, filters
import random, string, os, threading
from flask import Flask

# Flask server to keep bot alive
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

bot = Client("trendy_usernames_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Trending username generator like `dy3no`, `rx1zy`, etc.
def generate_trendy(count):
    usernames = []
    for _ in range(count):
        part1 = ''.join(random.choices(string.ascii_lowercase, k=2))     # e.g., dy
        part2 = ''.join(random.choices(string.digits, k=1))              # e.g., 3
        part3 = ''.join(random.choices(string.ascii_lowercase, k=2))     # e.g., no
        usernames.append(part1 + part2 + part3)
    return usernames

@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Send /get to get 50 trending-style usernames (like dy3no, rx7zy).")

@bot.on_message(filters.command("get"))
async def get(_, msg):
    names = generate_trendy(50)
    result = "\n".join([f"`{u}` - Available" for u in names])
    await msg.reply(f"Here are 50 trending-style usernames:\n\n{result}")

bot.run()
