from pyrogram import Client, filters
import random, string, os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("insta_username_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Welcome! Send /get to get 5-letter random Instagram usernames.")

@app.on_message(filters.command("get"))
async def get(_, msg):
    def generate():  # Generate 5-letter username
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    
    usernames = [generate() for _ in range(5)]  # Generate 5 usernames
    result = "\n".join([f"`{u}` - Available" for u in usernames])
    await msg.reply(f"Here are some Instagram-style usernames:\n\n{result}")

app.run()
