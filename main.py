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
from news_crawling import crawling_news
import schedule


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
    # 텔레그램 봇 실행
    print("Telegram bot is starting...")
    application.run_polling()
    print("Telegram bot is running...")

async def run_schedule():
    crawling_news()
    schedule.every().days.at("09:30").do(crawling_news)
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()
   
        

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run_schedule())
    asyncio.ensure_future(run_telegram_bot())
    loop.run_forever()
    loop.close()