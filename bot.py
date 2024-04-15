"""
We need two pakages for using this bot:

1) python-dotenv
pip install python-dotenv

2) python-telegram-bot v21.1
https://python-telegram-bot.org/
https://docs.python-telegram-bot.org/en/stable/index.html
https://docs.python-telegram-bot.org/en/stable/examples.conversationbot.html

PTB can be installed with optional dependencies:
pip install "python-telegram-bot[all]"
"""

from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from stt import whisper_result

load_dotenv(verbose=True)
TOKEN = os.environ.get("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=open("bot.jpg", "rb")
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm the Magic Conch. "
        + "\nWhat can I assist you with today? "
        + "\nJust a heads-up, I might not have answers to everything, "
        + "but I'm certainly able to provide time or weather updates for your desired city "
        + "or share the latest IT news!"
        + "\nWould you mind sharing your voice with me? "
        + "Oh, Of course in Korean. :-)",
    )


async def message_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await update.message.effective_attachment.get_file()
    await voice_file.download_to_drive("output.wav")
    # voice_file = await update.message.voice.get_file()
    # await voice_file.download_to_drive("output.wav")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Okay, Just a moment. \nIt takes a little time.",
    )

    whisper_result()


async def message_others(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Oops, I cannot understand you. \nCould you please share your voice with me?",
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    message_voice_handler = MessageHandler(
        filters.VOICE | filters.VIDEO_NOTE, message_voice
    )
    message_others_handler = MessageHandler(~filters.VOICE, message_others)

    application.add_handler(start_handler)
    application.add_handler(message_voice_handler)
    application.add_handler(message_others_handler)

    application.run_polling()
