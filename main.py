from pyrogram import Client, filters
import random, string, os, threading
import requests
from flask import Flask
import time

# Flask keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

threading.Thread(target=run_flask).start()

# Bot credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("insta_username_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Username generator: Starts with "e" + 4 random letters/digits
def generate_usernames(count):
    pool = string.ascii_lowercase + string.digits
    return ['e' + ''.join(random.choices(pool, k=4)) for _ in range(count)]

# Check Instagram username availability
def is_available_instagram(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    return response.status_code == 404  # 404 means it's available

@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Send /get to get 10 available Instagram usernames starting with 'e' (like `e1z9x`).")

@bot.on_message(filters.command("get"))
async def get(_, msg):
    await msg.reply("🔍 Checking Instagram usernames. Please wait...")

    available = []
    tries = 0

    while len(available) < 10 and tries < 50:  # Max 50 tries to find 10 available
        username = generate_usernames(1)[0]
        if is_available_instagram(username):
            available.append(username)
        tries += 1
        time.sleep(0.5)  # Add delay to avoid getting blocked

    if not available:
        await msg.reply("😔 Couldn't find any available usernames. Try again.")
        return

    result = "\n".join([f"`{u}` - ✅ Available" for u in available])
    await msg.reply(f"Here are 10 available Instagram usernames:\n\n{result}")

bot.run()
