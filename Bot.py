import os
import time
import asyncio
from pyrogram import Client, filters

# Render ke Environment Variables se details lega
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("renamer_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Progress Bar Function
async def progress_bar(current, total, message, start_time):
    now = time.time()
    diff = now - start_time
    if round(diff % 4.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff if diff > 0 else 0
        
        progress = "[{0}{1}] \n**Progress:** {2}%".format(
            ''.join(["●" for i in range(int(percentage / 10))]),
            ''.join(["○" for i in range(10 - int(percentage / 10))]),
            round(percentage, 2)
        )
        
        try:
            await message.edit(text=f"{progress}\n**Speed:** {round(speed / 1024, 2)} KB/s")
        except:
            pass

@app.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def get_file(client, message):
    await message.reply_text(
        "**File Mil Gayi!** ✅\n\nAb is message ka **Reply** karein naye naam ke saath.\n(Example: `my_movie.mp4`)",
        reply_to_message_id=message.id
    )

@app.on_message(filters.private & filters.text & filters.reply)
async def rename_now(client, message):
    if message.reply_to_message.document or message.reply_to_message.video or message.reply_to_message.audio:
        new_name = message.text
        status = await message.reply_text("📥 **Downloading...**")
        start_time = time.time()

        try:
            # Download
            path = await message.reply_to_message.download(
                file_name=new_name,
                progress=progress_bar,
                progress_args=(status, start_time)
            )

            await status.edit("📤 **Uploading...**")
            
            # Upload
            await message.reply_document(
                document=path,
                caption=f"**Renamed By:** @{app.me.username}",
                progress=progress_bar,
                progress_args=(status, start_time)
            )

            # Cleanup
            if os.path.exists(path):
                os.remove(path)
            await status.delete()
            
        except Exception as e:
            await status.edit(f"**Error:** `{e}`")

print("Bot Start Ho Gaya!")
app.run()
      
