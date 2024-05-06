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
from get_commands import InputFromUser
from global_city_search import get_global_city
import threading
from uuid import uuid4
load_dotenv(verbose=True)
TOKEN = os.environ.get("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=open("rss/bot.jpg", "rb")
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
    filenmame = f"output/{str(uuid4)}.wav"

    await voice_file.download_to_drive(filenmame)
    # voice_file = await update.message.voice.get_file()
    # await voice_file.download_to_drive("output.wav")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Okay, Just a moment. \nIt takes a little time.",
    )

    with InputFromUser(filenmame) as input:
        result = input

    try:
        if result["error"] != -1:
            raise Exception(result["error"])
        else:
            #{"result": {"city": city_result, "command": command_result}}
            crawling_result  = await get_global_city(result["result"]["city"][0], result["result"]["command"])

            # 뉴스 -> csv / 요약: text, img
            if 'text' in crawling_result.keys():
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=crawling_result['text']
                )
                if 'command_type' in crawling_result.keys():
                    await context.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=open("output/wordcloud_new.png", "rb")
                    )
            else:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,document='output/news.csv'
                )
               
            
    except Exception as e:
        print(result)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=result["error"]
        )
        

async def message_others(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Oops, I cannot understand you. \nCould you please share your voice with me?",
        )



    
   
        

