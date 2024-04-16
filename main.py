from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
import asyncio
from bot import start, message_voice, message_others, TOKEN
from typing import Union




application = ApplicationBuilder().token(TOKEN).read_timeout(30).write_timeout(30).build()

start_handler = CommandHandler("start", start)
message_voice_handler = MessageHandler(
    filters.VOICE, message_voice
)
message_others_handler = MessageHandler(~filters.VOICE, message_others)

application.add_handler(start_handler)
application.add_handler(message_voice_handler)
application.add_handler(message_others_handler)

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.run_polling())
if __name__ == "__main__":
    run_telegram_bot()

    
