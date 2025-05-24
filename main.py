from pyrogram import Client, filters
import random, string, os, threading
from flask import Flask

# Flask App for keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

threading.Thread(target=run_flask).start()

# Telegram Bot
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("insta_username_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Welcome! Send /get to get 5-letter random Instagram usernames.")

@bot.on_message(filters.command("get"))
async def get(_, msg):
    def generate():
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    
    usernames = [generate() for _ in range(5)]
    result = "\n".join([f"`{u}` - Available" for u in usernames])
    await msg.reply(f"Here are some Instagram-style usernames:\n\n{result}")

bot.run()
